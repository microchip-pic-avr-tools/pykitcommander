"""
A collection of firmware Serial-port-based communication drivers

Python-side clients that need to request services from firmware running on an embedded device
use these drivers to send commands and receive responses over a standard serial port.

Good practise is to follow this kind of pattern, which ensures port closure after use:

.. code-block:: python

    # Open a serial connection with given attributes
    with Serial(port, baud, timeout, stopbits) as serial_connection:
        # Instantiate a driver to handle communications
        firmware_driver = ProvisioningFirmwareDriver (serial_connection)
        # Send firmware command to turn on LED
        firmware_driver.firmware_command("MC+SETLED", ["conn","on"])

"""

from time import sleep
from logging import getLogger
from .kitcommandererrors import PortError, KitCommunicationError

class ProvisioningFirmwareDriver:
    """
    Firmware driver for communicating with "version 2" provisioning firmware
    Commands and responses are strings as described here:
    - Commands are terminated with \\r (\\r\\n and \\n are also accepted)
    - Command syntax: <cmd>=[<arg>[,<arg>...]\\r\\n [blob \\r\\n]]
    - Response:  [<blob> \\r\\n] "OK\\r\\n" | "ERROR:"<xxxx>\\r\\n
    - <hex> is hex-encoded blob, <xxxx> 16-bit hex error code

    :param serial_port: Serial-port object to use, must be opened by the caller
    :type serial_connection: object (Serial)
    :param encoding: Encoding format to use
    :type encoding: str
    """
    # Sources of error codes
    STATUS_SOURCE_COMMAND_HANDLER = 0
    STATUS_SOURCE_CRYPTOAUTHLIB = 1
    STATUS_SOURCE_WINC = 2

    # Command handler status codes
    MC_STATUS_OK = 0
    MC_STATUS_BAD_COMMAND = 1
    MC_STATUS_BUFFER_OVERRUN = 2
    MC_STATUS_BAD_ARGUMENT_COUNT = 3
    MC_STATUS_BAD_BLOB = 4
    MC_STATUS_BAD_ARGUMENT_VALUE = 5

    def __init__(self, serial_connection, encoding="UTF-8"):
        if not serial_connection.isOpen():
            raise PortError("Port not open!")
        self.serial_connection = serial_connection
        self.encoding = encoding
        self.logger = getLogger(__name__)
        self.sequence_number = 0
        # Synchronizing will work without the below, but will take a communication
        # timeout longer because target will not be ready when initial ping
        # is sent, causing it to time out due to lack of response. See
        # synchronize() below.
        # On the other hand, if the target was not reset prior to getting here,
        # the below will have a timeout penalty instead. However that is a less
        # likely use case.
        self.wait_for_reset()

    def synchronize(self):
        """
        Synchronize with firmware CLI using the ping command and unique sequence number
        """
        self.sequence_number += 1
        timeout = self.serial_connection.timeout
        self.serial_connection.timeout = 1
        # Flush input buffer
        garbage = self.serial_connection.read(self.serial_connection.in_waiting)
        if garbage:
            self.logger.debug("Garbage: %s", self._tostr(garbage))

        # Send ping command with unique sequence number
        cmd = f"MC+PING={self.sequence_number:06}".encode(self.encoding)
        # Avoid decoration of firmware_command(), so write directly to serial port here.
        self.serial_connection.write(cmd + b'\n')
        self.logger.debug("Sent sync command: %s", cmd)

        # Read responses until no more input, look for pong response
        retries = 0
        while True:
            response = self.read_response()
            self.logger.debug("Response received: '%s'", response)
            if response[-1] != "OK":
                if response[-1] == "ERROR: Timeout" and not self.serial_connection.in_waiting:
                    # Timeout caused by sending ping command before target is ready after reset,
                    # avoided by doing wait_for_reset() in __init__() but keep this here for safety:
                    # Send new ping command with new sequence number
                    self.sequence_number += 1
                    retries += 1
                    self.serial_connection.timeout += 1      # Try longer timeout next time
                    if retries > 3:
                        self.serial_connection.timeout = timeout
                        self.logger.debug("Too many retries, giving up")
                        break
                    cmd = f"MC+PING={self.sequence_number:06}".encode(self.encoding)
                    self.serial_connection.write(cmd + b'\n')
                    self.logger.debug("Timed out and no more response, re-sending %s, retries = %d", cmd, retries)
                else:
                    self.logger.debug("Unexpected potential garbage response: %s", response[-1])
                continue
            pong = None
            if len(response) > 1:
                for pong in response[:-1]:
                    if pong.startswith("MC+PONG="):
                        break
            if pong:
                sequence_number = int(pong[pong.find('=') + 1:], base=10)
                if sequence_number == self.sequence_number:
                    self.serial_connection.timeout = timeout
                    return
                # pong response with wrong sequence number may theoretically
                # be from a previous invocation, so give it the benefit of doubt
                # if there is more input.
            if not self.serial_connection.in_waiting:
                self.logger.debug("Failed, retries = %d", retries)
                break

        # If we get here, expected pong response has not been received
        self.serial_connection.timeout = timeout
        raise KitCommunicationError(
            f"Synchronization with target CLI failed: "
            f"retries: {retries} last response: {response}")

    def firmware_command(self, command, args=None, payload_blob=None):
        """
        Send a command to the firmware and receive a response

        :param command: Command string to send to firmware
        :type command: str
        :param args: Argument list
        :type args: list of str
        :param payload_blob: Binary data to send (normally hex-encoded)
        :type payload_blob: str
        :returns: Response
        :rtype: str
        """
        if self.serial_connection is None:
            raise PortError("Port not open.")

        # Generate command string with arguments
        args = args or []
        if args:
            fwcmd = "{}={}".format(command, ",".join(map(self._tostr, args)))
        else:
            fwcmd = command

        if payload_blob is None:
            self.logger.debug("FW command: %s", fwcmd)
            self.serial_connection.write((fwcmd + "\r\n").encode(self.encoding))
        else:
            sep = "," if "=" in fwcmd else "="
            fwcmd += "{}{}".format(sep, len(payload_blob))
            self.logger.debug("FW command: %s", fwcmd)
            self.serial_connection.write((fwcmd + "\r\n").encode(self.encoding))
            if len(payload_blob) > 0:
                self.serial_connection.read_until(b'>')
                self.logger.debug("Payload blob length: %d bytes", len(payload_blob))
                self.serial_connection.write(self._tobytes(payload_blob) + b'\r\n')

        # Read response from firmware
        response = self.read_response()
        self.logger.debug("Response received: '%s'", response)

        if response[-1].startswith("ERROR"):
            error_msg = self.parse_error_code(response[-1])
            raise KitCommunicationError("Command '{}' failed! '{}'"
                                        .format(fwcmd, error_msg))
        # We should return a list here but too many applications expect a string.
        return "" if len(response) < 2 else "\n".join(response[:-1])

    def read_response(self):
        """
        Read response from kit. Response can be multiple lines either
        terminated with "OK\\r\\n", "ERROR\\r\\n", or '>' so a simple read_until
        won't do.

        :returns: Response lines (blank lines and CR-LF stripped)
        :rtype: list of str
        """
        lines = []
        while True:
            line = self.serial_connection.read_until(b'\r\n')
            # Timeout reading results in an empty response
            if not line:
                lines.append("ERROR: Timeout")
                return lines
            # Content returned?
            if line != b'\r\n':
                lines.append(line[0:-2].decode(self.encoding, "ignore"))
                if line[0:2] == b"OK" or b"ERROR" in line:
                    # Done receiving
                    return lines

    def parse_error_code(self, errorline):
        """
        Parse a line containing error code
        The error code will be parsed and a more informative error message will be logged

        :param errorline: String from target containing error code
        :type errorline: str
        :return: User friendly error message
        :rtype: str
        """
        if not "ERROR:" in errorline.upper():
            # This line did not contain any error code, just skip further parsing
            return ""

        self.logger.debug("Parsing error line: %s", errorline)

        errorcode_string = errorline.split(":")[1].strip()

        source_module = "Unknown module"
        error_msg = "Unknown error"

        try:
            errorcode = int(errorcode_string, 0)
            errorsource = (errorcode & 0xFF00) / 256
            errorbyte = errorcode & 0xFF

            error_msg = "Errorcode: 0x{:02X}".format(errorbyte)
            if errorsource == self.STATUS_SOURCE_COMMAND_HANDLER:
                source_module = "Command Handler"
                if errorcode == self.MC_STATUS_BAD_ARGUMENT_COUNT:
                    error_msg = "Incorrect number of arguments"
                if errorcode == self.MC_STATUS_BAD_ARGUMENT_VALUE:
                    error_msg = "Invalid argument value"
                elif errorcode == self.MC_STATUS_BAD_BLOB:
                    error_msg = "Invalid data blob"
                elif errorcode == self.MC_STATUS_BAD_COMMAND:
                    error_msg = "Invalid command"
                elif errorcode == self.MC_STATUS_BUFFER_OVERRUN:
                    error_msg = "Buffer overrun"
            elif errorsource == self.STATUS_SOURCE_CRYPTOAUTHLIB:
                source_module = "Crypto Auth Lib"
            elif errorsource == self.STATUS_SOURCE_WINC:
                source_module = "WINC Library"
        except ValueError:
            # Error code was not parseable as integer, use it as a string
            if errorcode_string:
                error_msg = str(errorcode_string)
        finally:
            return "{} reported: {}".format(source_module, error_msg)

    def wait_for_reset(self):
        """
        Wait for 'READY' prompt to be received after restart of application,
        indicating firmware is ready to accept commands.
        This method will time out without raising if READY is not received,
        meaning target was not reset prior to this command,
        :return: Welcome banner + "READY" if it was reset, else empty string or garbage.
        """
        self.logger.debug("Wait for reset...")
        timeout = self.serial_connection.timeout
        self.serial_connection.timeout = 3
        response = self.serial_connection.read_until(b'READY\r\n')
        self.logger.debug("Response: %s", response)
        if not response:
            self.logger.debug("Wait for reset timed out")
        self.serial_connection.timeout = timeout
        return response

    # Helper functions
    # Takes int, str, or bytes argument and converts it appropriately
    # Use these functions when you know what you want but not what you have.
    def _tostr(self, arg):
        """
        Helper function to deal with arg that can be either int, str or bytes

        :param arg: Either int, bytes or str to be converted
        :return: str representation of s
        """
        if isinstance(arg, int):
            return str(arg)
        return arg if isinstance(arg, str) else arg.decode(self.encoding)

    def _tobytes(self, arg):
        """
        Helper function to deal with input that can be either int, str or bytes

        :param arg: Either int, bytes or str to be converted
        :return: bytes representation of s
        """
        if isinstance(arg, int):
            return bytes(str(arg), self.encoding)
        return arg if isinstance(arg, bytes) else arg.encode(self.encoding)


class IoTWxDemoFirmwareDriver:
    """
    Interface to demo firmware on WiFi boards (AVR-IoT-Wx/PIC-IoT-Wx)

    :param serial_connection: Serial-port object to use, must be opened by the caller
    :type serial_connection: object (Serial)
    """
    def __init__(self, serial_connection):
        self.serial_connection = serial_connection
        self.logger = getLogger(__name__)

    # pylint: disable=dangerous-default-value
    def demo_firmware_command(self, cmd, args=[]):
        """
        Send a request to demo FW CLI, return response.

        :param cmd: Command to send
        :type cmd: str
        :param args: Argument list
        :type args: list of str
        :return: response from firmware
        :rtype: str
        """
        if self.serial_connection is None:
            raise PortError("Port not open.")

        #TODO: refactor
        end_of_transmission = b'\\04'  # end of transmission from target
        buffer = ("{} {}\n").format(cmd, ",".join(args)).encode()
        sleep(0.1)     # Mystery delay between requests seems to avoid mixed-up responses
        # Experimental: Try to send a single character at a time to solve instability
        for c in buffer:
            buf = [c]
            self.serial_connection.write(buf)
            self.serial_connection.flush()
        response = self.serial_connection.read_until(end_of_transmission)[:-1].decode("utf-8", errors="ignore")
        return response
