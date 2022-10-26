"""
Implements EDBG Protocol, a sub-protocol in the JTAGICE3 family of protocols.
"""
import logging
from .jtagice3protocol import Jtagice3Protocol


class EdbgProtocol(Jtagice3Protocol):
    """
    Implements EDBG protocol functionality on the JTAGICE3 protocol family
    """

    CMD_EDBG_QUERY = 0x00  # //! Capability discovery
    CMD_EDBG_SET = 0x01  # //! Set parameters
    CMD_EDBG_GET = 0x02  # //! Get parameters

    CMD_EDBG_PROGRAM_ID_CHIP = 0x50  # //! ID Chip commands
    CMD_EDBG_REFRESH_ID_CHIP = 0x51  # //! ID Chip commands
    CMD_EDBG_READ_ID_CHIP = 0x7E     # //! ID Chip commands

    RSP_EDBG_OK = 0x80  # //! All OK
    RSP_EDBG_LIST = 0x81  # //! List of items returned
    RSP_EDBG_DATA = 0x84  # //! Data returned
    RSP_EDBG_FAILED = 0xA0  # //! Command failed to execute

    EDBG_QUERY_COMMANDS = 0x00

    EDBG_CTXT_CONTROL = 0x00  # //! Control
    EDBG_CONTROL_LED_USAGE = 0x00
    EDBG_CONTROL_EXT_PROG = 0x01
    EDBG_CONTROL_TARGET_POWER = 0x10

    """
    Mapping EDBG error codes to more human friendly strings
    """
    EDBG_ERRORS = {0: 'SUCCESS'}

    """
    Mapping SHA204 response codes to more human friendly strings
    """
    RESPONSE_CODE = {0x00: 'SHA204_SUCCESS',
                     0xD2: 'SHA204_PARSE_ERROR',
                     0xD3: 'SHA204_CMD_FAIL',
                     0xD4: 'SHA204_STATUS_CRC',
                     0xE0: 'SHA204_FUNC_FAIL',
                     0xE2: 'SHA204_BAD_PARAM',
                     0xE4: 'SHA204_INVALID_SIZE',
                     0xE5: 'SHA204_BAD_CRC',
                     0xE6: 'SHA204_RX_FAIL',
                     0xE7: 'SHA204_RX_NO_RESPONSE',
                     0xE8: 'SHA204_RESYNC_WITH_WAKEUP',
                     0xF0: 'SHA204_COMM_FAIL',
                     0xF1: 'SHA204_TIMEOUT',
                     0xFA: 'ID_DATA_LOCKED',
                     0xFB: 'ID_CONFIG_LOCKED',
                     0xFC: 'ID_INVALID_SLOT',
                     0xFD: 'ID_DATA_PARSING_ERROR',
                     0xFE: 'ID_DATA_NOT_EQUAL'}

    def __init__(self, transport):
        self.logger = logging.getLogger(__name__)
        super(EdbgProtocol, self).__init__(
            transport, Jtagice3Protocol.HANDLER_EDBG)

    def check_command_exists(self, command):
        """
        Runs a query to the tool to get a list of supported commands, then looks for
        the input command in the list. If not supported, it raises NotImplementedError.
        :param command: The command to test.
        :return: None
        """
        commands_supported = self.query(self.EDBG_QUERY_COMMANDS)
        if command not in commands_supported:
            raise NotImplementedError("Invalid command: 0x{:02X}".format(command))

    def error_as_string(self, code):
        """
        Get the response error as a string (error code translated to descriptive string)
        :param code: error code
        :return: error code as descriptive string
        """
        try:
            return self.EDBG_ERRORS[code]
        except KeyError:
            return "Unknown error!"

    def response_as_string(self, code):
        """
        Get the response code as a string (response code translated to descriptive string)
        :param code: response code
        :return: error code as descriptive string
        """
        try:
            return self.RESPONSE_CODE[code]
        except KeyError:
            return "Unknown response!"

    def program_id_chip(self, id_number, data):
        """
        Program the connected ID device located at the id_number with data.
        :param id_number: Extension header ID number (Range 1 - 16)
        :param data: A 64-byte data array to be programmed
        :return: Response status from the programming
        """
        self.logger.info("Programming ID chip...")
        try:
            self.check_command_exists(self.CMD_EDBG_PROGRAM_ID_CHIP)
        except NotImplementedError as err:
            self.logger.warning("Non-compliant command: %s", err)

            # Old EDBG implementations contained a non-compliant version of this command
            # Version 0 command
            packet = bytearray([self.CMD_EDBG_PROGRAM_ID_CHIP, self.CMD_VERSION0, id_number - 1] + data)
            resp = self.jtagice3_command_response_raw(packet)
            self.logger.debug("Program ID response: %s", self.response_as_string(resp[3]))
            return resp[3]
        else:
            # Version 1 command
            packet = bytearray([self.CMD_EDBG_PROGRAM_ID_CHIP, self.CMD_VERSION1, id_number] + data)
            status = self.check_response(self.jtagice3_command_response(packet))
            self.logger.debug("Program ID response: %s", self.response_as_string(status[0]))
            return status[0]

    def refresh_id_chip(self):
        """
        Forces a refresh of the list of connected ID devices.
        :return: None
        """
        self.logger.info("Refreshing ID chip...")
        try:
            self.check_command_exists(self.CMD_EDBG_REFRESH_ID_CHIP)
        except NotImplementedError as err:
            self.logger.warning("Non-compliant command: %s", err)

            # Old EDBG implementations contained a non-compliant version of this command
            # Version 0 command
            packet = bytearray([self.CMD_EDBG_REFRESH_ID_CHIP, self.CMD_VERSION0])
            resp = self.jtagice3_command_response_raw(packet)
            if not resp[3] == self.RSP_EDBG_OK:
                raise IOError("Invalid response from CMD_EDBG_REFRESH_ID_CHIP")
        else:
            # Version 1 command
            packet = bytearray([self.CMD_EDBG_REFRESH_ID_CHIP, self.CMD_VERSION1])
            self.check_response(self.jtagice3_command_response(packet))

    def read_id_chip(self, id_number):
        """
        Reads the ID information from the ID chip connected at id_number
        :param id_number: Extension header ID number (Range 1 - 16)
        :return: A 64-byte data array
        """
        self.logger.info("Reading ID chip...")
        try:
            self.check_command_exists(self.CMD_EDBG_READ_ID_CHIP)
        except NotImplementedError as err:
            self.logger.warning("Non-compliant command: %s", err)

            # Old EDBG implementations contained a non-compliant version of this command
            # Version 0 command
            packet = bytearray([self.CMD_EDBG_READ_ID_CHIP, self.CMD_VERSION0, id_number-1])
            resp = self.jtagice3_command_response_raw(packet)
            if resp[4] == self.RSP_EDBG_DATA:
                return resp[6:]
            return False
        else:
            # Version 1 command
            packet = bytearray([self.CMD_EDBG_READ_ID_CHIP, self.CMD_VERSION1, id_number])
            data = self.check_response(self.jtagice3_command_response(packet))
            return data
