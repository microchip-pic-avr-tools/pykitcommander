"""
Definition for programming PIC24 device on 5G FW tool using GEN4 scripts

Note: the GEN4 script engine operates on pre-generated byte-code shipped with MPLAB.
The byte-code arrays here are extracted from the XML source.  They should ideally be identical to the originals,
but may be modified to work via the CMSIS-DAP interface, inside or outside of MPLAB.
"""
from common.gen4scriptwrapper import pic24_pack_params

# Import PIC device class and its stack
from common.picdevice import *


class DeviceDefinition(PicDevice):
    """
    PIC Device definition
    """

    # Debugger model specifies how the Python stack interacts with the debugger over USB
    DEBUGGER_MODEL = Gen4WrapperDebugger
    # Programming interface specifies how the debugger tool interacts with the target device
    PROGRAMMING_INTERFACE = ProgInterfaceGen4
    # Debugging interface specifies how the debugger tool interacts with the debug executive
    DEBUGGING_INTERFACE = DebugExecApiPic24Vx

    # Programming executive Inteface specifies how the debugger tool interacts with the programming executive
    PROGRAMMING_EXECUTIVE_INTERFACE = ProgExecInterfacePic24

    DEFAULT_ADDRESS_FOR_BULK_ERASE_B = 0x0000

    # Flash properties for this device
    FLASH_WRITE_BYTES_PER_PAGE = 512

    # For PIC24 config words are implemented as another flash page, so we need to know where the boundary
    # between programming memory and config words are
    CONFIG_START_ADDRESS_BYTE = 0x2BE00

    def __init__(self):
        PicDevice.__init__(self)

    def enter_tmod(self):
        """
        Enter TMOD.
        Puts the PIC device into its "Programming mode"
        """
        # No parameters for this script
        params = []
        # Options
        options = {}
        # Bytecode content
        content = [0xB1, 0xB2, 0x00, 0xA0, 0x01, 0x00, 0xB0, 0xA0, 0x0A, 0x00, 0xB1, 0xA0, 0xE8, 0x03, 0xB4, 0xB2, 0xC2,
                   0x12, 0x8A, 0xA0, 0xF6, 0x09, 0xB0, 0xA0, 0x50, 0xC3, 0xB5, 0x05, 0x00, 0x00, 0x00, 0x00]
        return params, content, options

    def set_speed(self):
        """
        Set speed for normal ICSP mode.
        Sets the ICSP clock period to 200 nanoseconds
        """
        # No parameters for this script
        params = []
        # Options
        options = {}
        # Bytecode content
        content = [0xEC, 0xC8, 0x00, 0x00, 0x00]
        return params, content, options

    def set_speed_pe(self):
        """
        Set speed for eICSP mode (PE mode).
        Sets the ICSP clock period to 500 nanoseconds
        """
        # No parameters for this script
        params = []
        # Options
        options = {}
        # Bytecode content
        content = [0xEC, 0xF4, 0x01, 0x00, 0x00]
        return params, content, options

    def exit_tmod(self):
        """
        Exit programming mode
        """
        # No parameters for this script
        params = []
        # Options
        options = {}
        # Bytecode content
        content = [0xB2, 0x03, 0xB1, 0x94, 0x64, 0x00, 0xA0, 0x0A, 0x00, 0xB0]
        return params, content, options

    def read_id(self):
        """
        Read the device ID from the PIC
        """
        # No parameters for this script
        params = []
        # Options
        options = {}
        # Bytecode content
        content = [0xE0, 0x00, 0x02, 0x04, 0xE0, 0x00, 0x02, 0x04, 0xE1, 0x95, 0x90, 0x0A, 0x02, 0x00, 0xFF, 0x00, 0xE4,
                   0x0A, 0x00, 0xE0, 0xA0, 0x02, 0x88, 0xE5, 0x0A, 0x06, 0xE0, 0x47, 0x78, 0x20, 0xE0, 0xB6, 0x0B, 0xBA,
                   0xE1, 0xE1, 0xE2, 0x90, 0x0A, 0x00, 0x00, 0xFF, 0x00, 0xE4, 0x0A, 0x00, 0xE0, 0xA0, 0x02, 0x88, 0xE5,
                   0x0A, 0x06, 0xE0, 0x47, 0x78, 0x20, 0xE0, 0xB6, 0x0B, 0xBA, 0xE1, 0xE1, 0xE2]

        return params, content, options

    def read_flash(self, byte_address, numbytes):
        """
        Read flash from device
        """
        # This script expects two parameters:
        #   - parameter0: word address
        #   - parameter1: number of bytes
        params = []
        # GEN4 script is word addressed
        params.append(byte_address // 2)
        # GEN4 script will generate "packed" format: eg 512b means 384b
        numbytes = (numbytes * 3) // 4
        # Only multiple of 2 words (12 bytes) can be read so we might have to read slightly more than requested
        extra_bytes = 0
        if (numbytes % 12) > 0:
            extra_bytes = 12 - (numbytes % 12)
        numbytes += extra_bytes
        params.append(numbytes)
        packed_params = pic24_pack_params(params)
        # Options
        options = {'packed_data_count' : numbytes}
        # Bytecode content
        content = [0x91, 0x00, 0x91, 0x01, 0x93, 0x01, 0x0C, 0x00, 0xE0, 0x00, 0x02, 0x04, 0xE0, 0x00, 0x02, 0x04, 0xE1,
                   0xE0, 0x47, 0x78, 0x20,
                   0x95, 0xAD, 0x01, 0xE4, 0x00, 0x00, 0xE0, 0xA0, 0x02, 0x88, 0xE5, 0x00, 0x06, 0xE0, 0x80, 0x03, 0xEB,
                   0xE0, 0x96, 0x1B, 0xBA, 0xE1, 0xE1, 0xE0, 0xB6, 0xDB, 0xBA, 0xE1, 0xE1, 0xE0, 0xD6, 0xDB, 0xBA, 0xE1,
                   0xE1, 0xE0, 0xB6, 0x1B, 0xBA, 0xE1, 0xE1, 0xE0, 0x96, 0x1B, 0xBA, 0xE1, 0xE1, 0xE0, 0xB6, 0xDB, 0xBA,
                   0xE1, 0xE1, 0xE0, 0xD6, 0xDB, 0xBA, 0xE1, 0xE1, 0xE0, 0xB6, 0x1B, 0xBA, 0xE1, 0xE1, 0xE0, 0x20, 0x3C,
                   0x88, 0xE1, 0xE2, 0xE0, 0x21, 0x3C, 0x88, 0xE1, 0xE2, 0xE0, 0x22, 0x3C, 0x88, 0xE1, 0xE2, 0xE0, 0x23,
                   0x3C, 0x88, 0xE1, 0xE2, 0xE0, 0x24, 0x3C, 0x88, 0xE1, 0xE2, 0xE0, 0x25, 0x3C, 0x88, 0xE1, 0xE2, 0xE0,
                   0x00, 0x02, 0x04, 0xE0, 0x00, 0x02, 0x04, 0xE1, 0x92, 0x00, 0x08, 0x00, 0x00, 0x00, 0xAE]

        return packed_params, content, options

    def bulk_erase(self, byte_address=None):
        """
        Erase the entire flash area
        """
        # This script expects one parameter:
        #   - parameter0: byte_address
        if byte_address is None:
            byte_address=self.DEFAULT_ADDRESS_FOR_BULK_ERASE_B
        params = []
        params.append(byte_address)
        packed_params = pic24_pack_params(params)
        # Options
        options = {}
        # Bytecode content
        content = [0x91, 0x0A, 0x90, 0x00, 0x0E, 0x40, 0x00, 0x00, 0x90, 0x01, 0x0E, 0x40, 0x00, 0x00, 0x90, 0x02, 0x6E,
                   0x40, 0x00, 0x00, 0x90, 0x03, 0x5E, 0x40, 0x00, 0x00, 0x90, 0x04, 0x4E, 0x40, 0x00, 0x00, 0x90, 0x05,
                   0x66, 0x40, 0x00, 0x00, 0x90, 0x06, 0x56, 0x40, 0x00, 0x00, 0x90, 0x07, 0x46, 0x40, 0x00, 0x00, 0x6D,
                   0x0B, 0x0A, 0xE0, 0x00, 0x02, 0x04, 0xE0, 0x00, 0x02, 0x04, 0xE1, 0xE5, 0x0B, 0x0A, 0xE0, 0x0A, 0x3B,
                   0x88, 0xE0, 0x58, 0x05, 0x20, 0xE0, 0x38, 0x3B, 0x88, 0xE0, 0xA9, 0x0A, 0x20, 0xE0, 0x39, 0x3B, 0x88,
                   0xE0, 0x61, 0xE7, 0xA8, 0xE1, 0xE1, 0xE1, 0xE1, 0xA0, 0x78, 0x69, 0x90, 0x0A, 0x60, 0x07, 0x00, 0x00,
                   0xA2, 0xE0, 0x00, 0x02, 0x04, 0xE1, 0xE0, 0x41, 0x78, 0x20, 0xE5, 0x0A, 0x02, 0xE1, 0xE0, 0x92, 0x08,
                   0x78, 0xE1, 0xE2, 0xA5, 0x00, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0xE1, 0xE1]

        return packed_params, content, options

    def write_flash_page(self, byte_address, numbytes):
        """
        Write complete flash pages to the device
        """
        # This script expects two parameters:
        #   - parameter0: word address
        #   - parameter1: number of bytes
        params = []
        # GEN4 script is word addressed
        params.append(byte_address // 2)
        # GEN4 script will consume "packed" format: eg 512b means 384b
        numbytes = (numbytes * 3) // 4
        params.append(numbytes)
        packed_params = pic24_pack_params(params)
        # Options
        options = {'packed_data_count' : numbytes}
        # Bytecode content
        content = [0x91, 0x00, 0x91, 0x01, 0x93, 0x01, 0x80, 0x01, 0xAD, 0x01, 0xE0, 0x00, 0x02, 0x04, 0xE0, 0x00, 0x02,
                   0x04, 0xE1, 0xE0, 0x2A, 0x00, 0x24, 0xE0, 0x0A, 0x3B, 0x88, 0xE0, 0xA0, 0x0F, 0x20, 0xE0, 0xA0, 0x02,
                   0x88, 0xE4, 0x00, 0x00, 0xE0, 0x20, 0x3B, 0x88, 0xE5, 0x00, 0x00, 0xE0, 0x10, 0x3B, 0x88, 0xE0, 0x80,
                   0x03, 0xEB, 0xAC, 0x20, 0x00, 0xE6, 0x00, 0xE6, 0x01, 0xE6, 0x02, 0xE6, 0x03, 0xE6, 0x04, 0xE6, 0x05,
                   0xE0, 0x00, 0x03, 0xEB, 0xE1, 0xE0, 0xB6, 0x0B, 0xBB, 0xE1, 0xE1, 0xE0, 0xB6, 0xDB, 0xBB, 0xE1, 0xE1,
                   0xE0, 0xB6, 0xEB, 0xBB, 0xE1, 0xE1, 0xE0, 0xB6, 0x1B, 0xBB, 0xE1, 0xE1, 0xE0, 0xB6, 0x0B, 0xBB, 0xE1,
                   0xE1, 0xE0, 0xB6, 0xDB, 0xBB, 0xE1, 0xE1, 0xE0, 0xB6, 0xEB, 0xBB, 0xE1, 0xE1, 0xE0, 0xB6, 0x1B, 0xBB,
                   0xE1, 0xE1, 0xA4, 0xE0, 0x58, 0x05, 0x20, 0xE0, 0x38, 0x3B, 0x88, 0xE0, 0xA9, 0x0A, 0x20, 0xE0, 0x39,
                   0x3B, 0x88, 0xE0, 0x61, 0xE7, 0xA8, 0xE1, 0xE1, 0xE1, 0xE1, 0xA0, 0xD0, 0x07, 0x90, 0x0A, 0x60, 0x07,
                   0x00, 0x00, 0xA2, 0xE0, 0x00, 0x02, 0x04, 0xE1, 0xE0, 0x41, 0x78, 0x20, 0xE5, 0x0A, 0x02, 0xE1, 0xE0,
                   0x92, 0x08, 0x78, 0xE1, 0xE2, 0xA5, 0x00, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0x92,
                   0x00, 0x00, 0x01, 0x00, 0x00, 0xAE]

        return packed_params, content, options

    def release_from_reset(self):
        """
        Release the part from reset and let it run
        """
        # This script takes no parameters
        params = []
        # Options
        options = {}
        # Bytecode content
        # 0xB0 will set MCLR high
        content = [0xB0]
        return params, content, options

    def hold_in_reset(self):
        """
        Hold the part in reset and prevent it from running
        """
        # This script takes no parameters
        params = []
        # Options
        options = {}
        # Bytecode content
        # 0xB1 will set MCLR low
        content = [0xB1]
        return params, content, options

    def erase_testmem_range(self, byte_address, numbytes):
        """
        Erase the DE
        :param byte_address: address
        :param numbytes: number of bytes
        """
        # This script expects two parameters:
        #   - parameter0: word address
        #   - parameter1: number of bytes
        params = []
        # GEN4 script is word addressed
        params.append(byte_address // 2)
        params.append(numbytes)
        packed_params = pic24_pack_params(params)
        # Options
        options = {}
        content = [0x91, 0x00, 0x91, 0x01, 0xF5, 0x01, 0x00, 0x0C, 0xAD, 0x01, 0xE0, 0x00, 0x02, 0x04, 0xE0, 0x00, 0x02,
                   0x04, 0xE1, 0xE0, 0x3A, 0x00, 0x24, 0xE0, 0x0A, 0x3B, 0x88, 0xE4, 0x00, 0x00, 0xE0, 0x20, 0x3B, 0x88,
                   0xE5, 0x00, 0x00, 0xE0, 0x10, 0x3B, 0x88, 0xE0, 0x58, 0x05, 0x20, 0xE0, 0x38, 0x3B, 0x88, 0xE0, 0xA9,
                   0x0A, 0x20, 0xE0, 0x39, 0x3B, 0x88, 0xE0, 0x61, 0xE7, 0xA8, 0xE1, 0xE1, 0xE1, 0xE1, 0xA0, 0x78, 0x69,
                   0x90, 0x0A, 0x60, 0x07, 0x00, 0x00, 0xA2, 0xE0, 0x00, 0x02, 0x04, 0xE1, 0xE0, 0x41, 0x78, 0x20, 0xE5,
                   0x0A, 0x02, 0xE1, 0xE0, 0x92, 0x08, 0x78, 0xE1, 0xE2, 0xA5, 0x00, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00,
                   0x00, 0x00, 0x02, 0x92, 0x00, 0x00, 0x08, 0x00, 0x00, 0xAE]
        return packed_params, content, options

    def enter_debug(self):
        """
        Enter debug mode
        """
        # This script takes no parameters
        params = []
        # Options
        options = {}
        content = [0xB2, 0x00, 0xB1, 0x94, 0x64, 0x00, 0xA0, 0x10, 0x27, 0xB0, 0x94, 0x64, 0x00, 0xA0, 0x98, 0x3A, 0xB1,
                   0x94, 0x64, 0x00, 0xA0, 0x10, 0x27, 0xB0, 0x94, 0x64, 0x00, 0xB6, 0xA0, 0x50, 0xC3, 0x30, 0xB6]
        return params, content, options

    def enter_tmod_pe(self):
        """
        Enter TMOD using Programming Executive.
        Puts the PIC device into its "Programming mode" using the devices Programming Executive
        """
        # No parameters for this script
        params = []
        # Options
        options = {}
        # Bytecode content
        content = [0xB1, 0xB2, 0x00, 0xB0, 0xA0, 0x50, 0xC3, 0xB1, 0xA0, 0xE8, 0x03, 0xB4, 0xB2, 0xC2, 0x12, 0x0A, 0xA0,
                   0xF6, 0x09, 0xB2, 0x03, 0xB0, 0xA0, 0x50, 0xC3, 0xB2, 0x00]
        return params, content, options

    def get_config_start_address_byte(self):
        """
        Returns the first address of configuration memory for the device
        """
        return self.CONFIG_START_ADDRESS_BYTE