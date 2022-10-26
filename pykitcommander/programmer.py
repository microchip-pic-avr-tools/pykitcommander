"""
Programming related functions, using pymcuprog backend API.
"""
import os
from logging import getLogger, ERROR
from time import sleep

from pymcuprog.backend import Backend, SessionConfig
from pymcuprog.toolconnection import ToolUsbHidConnection
from pymcuprog.deviceinfo.memorynames import MemoryNames
from pydebuggerconfig.backend import board_config_manager

class Programmer():
    """
    Class to program applications

    :param serialnumber: Serial number of programmer
    :type serialnumber: str
    """
    def __init__(self, serialnumber=None):
        self.logger = getLogger(__name__)

    def erase_target_device(self):
        """
        Erases target device
        Useful to clean up after provisioning etc when no application is available.
        """
        pass

    def program_hexfile(self, filename, memory=MemoryNames.FLASH, erase=True, verify=False):
        """
        Program target with hex file. Returns: True if OK

        :param filename: Full path to file to program
        :type str:
        :param memory: Memory type to program
        :type memory: str
        :param erase: True to erase before programming
        :type erase: boolean
        :param verify: True to verify after programming
        :type verify: boolean
        :returns: True if programming succeeded
        :rtype: boolean
        """
        pass

    def program_data(self, data, memory=MemoryNames.FLASH, offset=0, erase=True, verify=False):
        """
        Program target with memory data, assumed to be a byte array. Returns: True if OK

        :param data: Raw data bytes to program
        :type data: bytearray
        :param memory: Memory type to program
        :type memory: str
        :param offset: First address to program
        :type offset: int
        :param erase: True to erase before programming
        :type erase: boolean
        :param verify: True to verify after programming
        :type verify: boolean
        :returns: True if programming succeeded
        :rtype: boolean
        """
        pass

    def read_data(self, memory=MemoryNames.FLASH, offset=0, size=0):
        """
        Read data from device memory. This function only supports reading a
        single memory, and returns a single bytearray. size=0 means read
        the whole memory.

        :param memory: Memory type to read
        :type memory: str
        :param offset: First address to read
        :type offset: int
        :param size: Number of bytes to read
        :type size: int
        """
        pass

    def reboot(self):
        """
        Reboot debugger. Note that for IOT kits, this only reboots the debugger, not the target.
        Purpose is to invalidate the cache after the click-me file has been updated.
        """
        pass

    def reset_target(self, delay=0.0):
        """
        Resets the target device

        :param delay: Number of seconds to delay after reset
        :type delay: float, optional, defaults to 0.5s
        """
        pass


class PymcuprogProgrammer(Programmer):
    """
    Class to interface pymcuprog backend.

    :param serialnumber: Serial number of programmer
    :type serialnumber: str
    :param dfp_path: Path to device family pack (for PIC programming only)
    :type dfp_path: str
    """
    def __init__(self, serialnumber=None, dfp_path="."):
        super().__init__(serialnumber=serialnumber)
        self.logger = getLogger(__name__)
        # Suppress warnings from below
        getLogger("pydebuggerconfig").setLevel(ERROR)
        self.serialnumber = serialnumber
        self.backend = Backend()
        self.kits = []
        self.tool = None
        self.packpath = None
        #TODO - make use of in_session guards if needed
        self.in_session = False

        tools = self.backend.get_available_hid_tools(serialnumber, 'nedbg')

        # Need to read info from each tool in order to get device name etc.
        for tool in tools:
            try:
                self.backend.connect_to_tool(ToolUsbHidConnection(serialnumber=tool.serial_number))
                self.kits.append(self.backend.read_tool_info())
            except Exception as e:
                # If we get here the tool is definitely unsuitable, log error and ignore it.
                self.logger.error("Error '%s' connecting to '%s'", str(e), tool.product_string)
            finally:
                self.backend.disconnect_from_tool()

            if len(self.kits) == 1:
                self.tool = self.kits[0]
                dev = self.tool["device_name"].lower()
                self.packpath = os.path.join(dfp_path, dev)


    def get_usable_kits(self):
        """
        Get a list of usable kits. Programming methods below will only
        work if there is exactly one usable kit in the list.

        :returns: Usable kits connected
        :rtype: list of dict
        """
        return self.kits

    def read_kit_info(self, register):
        """
        Reads a single kit info register (that is not in the CMSIS-DAP info struct from config)

        :param register: Name of register to read
        :type register: str
        """
        with board_config_manager(serialnumber_substring=self.serialnumber) as boardconfig:
            boardconfig.config_read_from_board()
            return boardconfig.register_get(register)

    def _setup_session(self):
        # Set up session
        self.backend.connect_to_tool(ToolUsbHidConnection(serialnumber=self.tool["serialnumber"]))
        sessionconfig = SessionConfig(self.tool["device_name"])
        sessionconfig.packpath = self.packpath
        self.backend.start_session(sessionconfig)
        self.in_session = True


    def _teardown_session(self):
        # Clean up session
        self.backend.end_session()
        self.backend.disconnect_from_tool()
        self.in_session = False


    def erase_target_device(self):
        """
        Erases target device
        Useful to clean up after provisioning etc when no application is available.
        """
        self.logger.info("Erasing target...")
        try:
            self._setup_session()
            self.backend.erase()
        finally:
            self._teardown_session()

    def program_hexfile(self, filename, memory=MemoryNames.FLASH, erase=True, verify=False):
        """
        Program target with hex file.

        :param filename: Full path to file to program
        :type str:
        :param memory: Memory type to program
        :type memory: str
        :param erase: True to erase before programming
        :type erase: boolean
        :param verify: True to verify after programming
        :type verify: boolean
        :returns: True if programming succeeded
        :rtype: boolean
        """
        self.logger.info("Program hexfile to target:")
        try:
            self._setup_session()
            if erase and memory in [MemoryNames.FLASH]:
                self.logger.info("Erasing %s...", memory)
                self.backend.erase()
            self.logger.info("Programming %s...", memory)
            self.backend.write_hex_to_target(filename)
            if verify:
                self.logger.info("Verifying %s...", memory)
                return self.backend.verify_hex(filename)
            return True

        finally:
            self._teardown_session()

    def program_data(self, data, memory=MemoryNames.FLASH, offset=0, erase=True, verify=False):
        """
        Program target with memory data, assumed to be a byte array.

        :param data: Raw data bytes to program
        :type data: bytearray
        :param memory: Memory type to program
        :type memory: str
        :param offset: First address to program
        :type offset: int
        :param erase: True to erase before programming
        :type erase: boolean
        :param verify: True to verify after programming
        :type verify: boolean
        :returns: True if programming succeeded
        :rtype: boolean
        """
        self.logger.info("Program data to target:")
        try:
            self._setup_session()
            # Attempting to erase other memory types may have unexpected side effects.
            # See also DSG-1408
            if erase and memory in [MemoryNames.FLASH]:
                self.logger.info("Erasing %s...", memory)
                self.backend.erase()
            self.logger.info("Programming %s...", memory)
            self.backend.write_memory(data, memory, offset_byte=offset)
            if verify:
                self.logger.info("Verifying %s...", memory)
                return self.backend.verify_memory(data, memory, offset_byte=offset)
            return True
        finally:
            self._teardown_session()


    def read_data(self, memory=MemoryNames.FLASH, offset=0, size=0):
        """
        Read data from device memory. This function only supports reading a
        single memory, and returns a single bytearray. size=0 means read
        the whole memory.

        :param memory: Memory type to read
        :type memory: str
        :param offset: First address to read
        :type offset: int
        :param size: Number of bytes to read
        :type size: int
        """
        self.logger.info("Read data from target")
        try:
            self._setup_session()
            memories = self.backend.read_memory(memory, offset_byte=offset, numbytes=size)
            return memories[0].data

        finally:
            self._teardown_session()


    def reboot(self):
        """
        Reboot debugger. Note that for IOT kits, this only reboots the debugger, not the target.
        Purpose is to invalidate the cache after the click-me file has been updated.
        """
        # Tool must be connected for reboot to work
        self.backend.connect_to_tool(ToolUsbHidConnection(serialnumber=self.tool["serialnumber"]))
        self.backend.reboot_tool()
        # Disconnect after reboot (not sure if this is required)
        sleep(2)
        self.backend.disconnect_from_tool()

    def reset_target(self, delay=0.0):
        """
        Resets the target device

        :param delay: Number of seconds to delay after reset
        :type delay: float, optional, defaults to 0.5s
        """
        self.logger.info("Reseting target device")
        try:
            self._setup_session()
            # Toggle reset
            self.backend.hold_in_reset()
            sleep(0.1)
            self.backend.release_from_reset()
            sleep(delay)

        finally:
            self._teardown_session()
