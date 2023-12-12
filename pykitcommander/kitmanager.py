"""
Kit state management functions
"""

import os
from logging import getLogger
from pyedbglib.serialport.serialportmap import SerialPortMap
from pyedbglib.serialport.serialportcheck import check_access
from .programmer import PymcuprogProgrammer
from .kitcommandererrors import KitConnectionError
from .firmwareinterface import ProvisioningFirmwareDriver
from .firmwareinterface import  IoTWxDemoFirmwareDriver

# InstallDir gives access to bundled FW hexfiles
INSTALLDIR = os.path.abspath(os.path.dirname(__file__))

## LED definitions
## These are used when accessing LEDs through the MC+SETLED and MC+GETLED commands
class KitLeds():
    """
    Base class for LED name definitions on IoT kits
    """
    WIRELESS_LED = None
    CONNECTION_LED = None
    DATA_LED = None
    ERROR_LED = None
    USER_LED = None

class WifiKitLeds(KitLeds):
    """
    Definition of LED names on WIFI IoT kits
    """
    WIRELESS_LED = "WIFI"
    CONNECTION_LED = "CONN"
    DATA_LED = "DATA"
    ERROR_LED = "ERROR"

class CellularKitLeds(KitLeds):
    """
    Definition of LED names on Cellular IoT kits
    """
    WIRELESS_LED = "CELL"
    CONNECTION_LED = "CONN"
    DATA_LED = "DATA"
    ERROR_LED = "ERR"
    USER_LED = "USER"

class CellularMiniKitLeds(KitLeds):
    """
    Definition of LED names on Cellular Mini IoT kits
    """
    WIRELESS_LED = "CELL"
    CONNECTION_LED = "CONN"
    DATA_LED = "DATA"
    ERROR_LED = "ERROR"
    USER_LED = "USER"

class TrustplatformKitLeds(KitLeds):
    """
    Definition of LED names on CryptoAuth Trust Platform kits
    """
    # Only one LED on this kit. On the PCB it is called STATUS,
    # but most useful as ERROR LED to indicate any problems during operation.
    ERROR_LED = "STATUS"


# Firmware bundled/pointers
AVRIOT_PROVISION_FW = {
    'description' : "Provisioning firmware for AVR-IoT",
    'bundled_firmware' : "fw/avr/atmega4808-iot-provision-v2.hex",
    # Version fetched by command MC+VERSION=FIRMWARE
    'bundled_firmware_version': "0.4.9",
    'internal_firmware_repo' : None,
    'public_firmware_repo' : None,
    'protocol_baud' : 115200,
    'protocol_id' : 'ProvisioningV2',
    'protocol_class' : ProvisioningFirmwareDriver,
    "startup_delay": 0,
}

AVRIOT_CELLULAR_PROVISION_FW = {
    'description' : "Provisioning firmware for AVR-IoT Cellular",
    'bundled_firmware' : "fw/avr/avr128db64-iot-cellular-provision.hex",
    # Version fetched by command MC+VERSION=FIRMWARE
    'bundled_firmware_version': "0.3.1",
    'internal_firmware_repo' : None,
    'public_firmware_repo' : None,
    'protocol_baud' : 115200,
    'protocol_id' : 'ProvisioningV2',
    'protocol_class' : ProvisioningFirmwareDriver,
    "startup_delay": 0,
}

AVRIOT_CELLULARMINI_PROVISION_FW = {
    'description' : "Provisioning firmware for AVR-IoT Cellular Mini",
    'bundled_firmware' : "fw/avr/avr128db48-iot-cellular-mini-provisioning.hex",
    # Version fetched by command MC+VERSION=FIRMWARE
    'bundled_firmware_version': "1.1.8",
    'internal_firmware_repo' : None,
    'public_firmware_repo' : None,
    'protocol_baud' : 115200,
    'protocol_id' : 'ProvisioningV2',
    'protocol_class' : ProvisioningFirmwareDriver,
    "startup_delay": 0,
}

AVRIOT_CELLULARMINI_AWS_DEMO_FW = {
    'description' : "Arduino-based demo application for AWS connectivity using AVR-IoT Cellular Mini",
    'bundled_firmware' : "fw/avr/avr128db48-iot-cellular-mini-arduino-demo.hex",
    'bundled_firmware_version': "1.3.9",
    'internal_firmware_repo' : None,
    'public_firmware_repo' : "https://api.github.com/repos/microchip-pic-avr-solutions/avr-iot-cellular-arduino-library/releases/latest/",
    'protocol_baud' : None,
    'protocol_id' : None,
    'protocol_class' : None,
    "startup_delay": 0,
}

PICIOT_PROVISION_FW = {
    'description' : "Provisioning firmware for PIC-IoT",
    'bundled_firmware' : "fw/pic/pic24fj128ga705-iot-provision-v2.hex",
    # Version fetched by command MC+VERSION=FIRMWARE
    'bundled_firmware_version': "0.4.7",
    'internal_firmware_repo' : None,
    'public_firmware_repo' : None,
    'protocol_baud' : 115200,
    'protocol_id' : 'ProvisioningV2',
    'protocol_class' : ProvisioningFirmwareDriver,
    "startup_delay": 0,
}

SAMIOT_PROVISION_FW = {
    'description' : "Provisioning firmware for SAM-IoT",
    'bundled_firmware' : "fw/sam/samd21g18a-iot-provision.hex",
    # Version fetched by command MC+VERSION=FIRMWARE
    'bundled_firmware_version': "1.0.1",
    'internal_firmware_repo' : None,
    'public_firmware_repo' : None,
    'protocol_baud' : 115200,
    'protocol_id' : 'ProvisioningV2',
    'protocol_class' : ProvisioningFirmwareDriver,
    "startup_delay": 0,
}

SAMIOT_WX_PROVISION_FW = {
    'description' : "Provisioning firmware for SAM-IoT Wx",
    'bundled_firmware' : "fw/sam/samd21g18a-iot-wx-provision.hex",
    # Version fetched by command MC+VERSION=FIRMWARE
    'bundled_firmware_version': "1.0.0",
    'internal_firmware_repo' : None,
    'public_firmware_repo' : None,
    'protocol_baud' : 115200,
    'protocol_id' : 'ProvisioningV2',
    'protocol_class' : ProvisioningFirmwareDriver,
    "startup_delay": 0,
}

TRUSTPLATFORM_PROVISION_FW = {
    'description' : "Provisioning firmware for CryptoAuth Trust Platform kit",
    'bundled_firmware' : "fw/sam/samd21e18a-trustplatform-provision.hex",
    # Version fetched by command MC+VERSION=FIRMWARE
    'bundled_firmware_version': "1.1.0",
    'internal_firmware_repo' : None,
    'public_firmware_repo' : None,
    'protocol_baud' : 115200,
    'protocol_id' : 'ProvisioningV2',
    'protocol_class' : ProvisioningFirmwareDriver,
    "startup_delay": 0,
}

AVRIOT_AWS_DEMO_FW = {
    'description' : "Demo application for AWS connectivity using AVR-IoT",
    'bundled_firmware' : "fw/avr/atmega4808-aws-iot-demo.hex",
    'bundled_firmware_version': "4.1.2",
    'internal_firmware_repo' : None,
    'public_firmware_repo' : "https://api.github.com/repos/microchip-pic-avr-solutions/avr-iot-aws-sensor-node-mplab/releases/latest",
    'protocol_baud' : 9600,
    'protocol_id' : 'WxDemoV1',
    'protocol_class' : IoTWxDemoFirmwareDriver,
    "startup_delay": 0,
}

AVRIOT_GOOGLE_DEMO_FW = {
    'description' : "Demo application for Google connectivity using AVR-IoT",
    'bundled_firmware' : "fw/avr/atmega4808-google-iot-demo.hex",
    'bundled_firmware_version': "4.0.0",
    'internal_firmware_repo' : None,
    'public_firmware_repo' : "https://api.github.com/repos/microchip-pic-avr-solutions/avr-iot-google-sensor-node-mplab/releases/latest",
    'protocol_baud' : 9600,
    'protocol_id' : 'WxDemoV1',
    'protocol_class' : IoTWxDemoFirmwareDriver,
    "startup_delay": 0,
}

PICIOT_AWS_DEMO_FW = {
    'description' : "Demo application for AWS connectivity using PIC-IoT",
    'bundled_firmware' : "fw/pic/pic24fj128ga705-aws-iot-demo.hex",
    'bundled_firmware_version': "4.1.3",
    'internal_firmware_repo' : None,
    'public_firmware_repo' : "https://api.github.com/repos/microchip-pic-avr-solutions/pic-iot-aws-sensor-node/releases/latest",
    'protocol_baud' : 9600,
    'protocol_id' : 'WxDemoV1',
    'protocol_class' : IoTWxDemoFirmwareDriver,
    "startup_delay": 0,
}

PICIOT_GOOGLE_DEMO_FW = {
    'description' : "Demo application for Google connectivity using PIC-IoT",
    'bundled_firmware' : "fw/pic/pic24fj128ga705-google-iot-demo.hex",
    'bundled_firmware_version': "1.1.1",
    'internal_firmware_repo' : None,
    'public_firmware_repo' : None,
    'protocol_baud' : 9600,
    'protocol_id' : 'WxDemoV1',
    'protocol_class' : IoTWxDemoFirmwareDriver,
    "startup_delay": 0,
}

PICIOT_AZURE_DEMO_FW = {
    'description' : "Demo application for Azure connectivity using PIC-IoT",
    # Source: https://github.com/Azure-Samples/Microchip-PIC-IoT-Wx/blob/main/AzureIotPnpDps.X/dist/default/production/AzureIotPnpDps.X.production.hex
    # Exported 2023.11.30
    # Version number seems to be the same as the previous release but this hex file came from this github commit:
    # https://github.com/Azure-Samples/Microchip-PIC-IoT-Wx/commit/c3a034b74d9ff9d4f3bee6b89416ae2c99f3e5f4
    # Published on github 2022.05.12
    'bundled_firmware' : "fw/pic/AzureIotPnpDps.X.production.hex",
    'bundled_firmware_version': "1.1.1",
    'internal_firmware_repo' : None,
    'public_firmware_repo' : None,
    'protocol_baud' : 9600,
    'protocol_id' : 'WxDemoV1',
    'protocol_class' : IoTWxDemoFirmwareDriver,
    "startup_delay": 0,
}

SAMIOT_AZURE_DEMO_FW = {
    'description' : "Demo application for Azure connectivity using SAM-IoT",
    # Source: https://github.com/Azure-Samples/Microchip-SAM-IoT-Wx/blob/main/firmware/AzureIotPnpDps.X/dist/SAMD21_WG_IOT/production/AzureIotPnpDps.X.production.hex
    # Exported 2022.10.12
    # Version number seems to be the same as the previous release but this hex file came from this github commit:
    # https://github.com/Azure-Samples/Microchip-SAM-IoT-Wx/commit/9c568697ff0a37b7b64f39436c5865ed745b5d8e
    # Published on github 2022.05.17
    'bundled_firmware' : "fw/sam/AzureIotPnpDps.X.production.hex",
    'bundled_firmware_version': "2.0.0",
    'internal_firmware_repo' : None,
    'public_firmware_repo' : None,
    'protocol_baud' : 9600,
    'protocol_id' : 'WxDemoV1',
    'protocol_class' : IoTWxDemoFirmwareDriver,
    "startup_delay": 0,
}

SAMIOT_GOOGLE_DEMO_FW = {
    'description' : "Demo application for Google connectivity using SAM-IoT",
    # Source: https://github.com/Microchip-MPLAB-Harmony/reference_apps/releases/download/v1.4.0/google_cloud_iot_core.zip
    # Exported 2022.03.24
    'bundled_firmware' : "fw/sam/sam_d21_iot_wg.X.production.hex",
    'bundled_firmware_version': "1.4.0",
    'internal_firmware_repo' : None,
    'public_firmware_repo' : None,
    'protocol_baud' : 9600,
    'protocol_id' : 'WxDemoV1',
    'protocol_class' : IoTWxDemoFirmwareDriver,
    "startup_delay": 0,
}

AVRIOT_WINCUPGRADE_FW = {
    'description' : "WINC upgrade bridge firmware for AVR-IoT",
    'bundled_firmware' : "fw/avr/atmega4808-iot-winc-upgrade.hex",
    'bundled_firmware_version': "unknown",
    'internal_firmware_repo' : None,
    'public_firmware_repo' : None,
    'protocol_baud' : 115200,
    'protocol_id' : 'WincUpgradeV1',
    'protocol_class' : None,
    "startup_delay": 0.5,
}

PICIOT_WINCUPGRADE_FW = {
    'description' : "WINC upgrade bridge firmware for PIC-IoT",
    'bundled_firmware' : "fw/pic/pic24fj128ga705-iot-winc-upgrade.hex",
    'bundled_firmware_version': "unknown",
    'internal_firmware_repo' : None,
    'public_firmware_repo' : None,
    'protocol_baud' : 115200,
    'protocol_id' : 'WincUpgradeV1',
    'protocol_class' : None,
    "startup_delay": 0.1,
}

SAMIOT_WINCUPGRADE_FW = {
    'description' : "WINC upgrade bridge firmware for SAM-IoT",
    'bundled_firmware' : "fw/sam/samd21g18a-iot-winc-upgrade.hex",
    'bundled_firmware_version': "unknown",
    'internal_firmware_repo' : None,
    'public_firmware_repo' : None,
    'protocol_baud' : 115200,
    'protocol_id' : 'WincUpgradeV1',
    'protocol_class' : None,
    "startup_delay": 0.1,
}

SAMIOT_WX_WINCUPGRADE_FW = {
    'description' : "WINC upgrade bridge firmware for SAM-IoT",
    'bundled_firmware' : "fw/sam/samd21g18a-iot-wx-winc-upgrade.hex",
    'bundled_firmware_version': "unknown",
    'internal_firmware_repo' : None,
    'public_firmware_repo' : None,
    'protocol_baud' : 115200,
    'protocol_id' : 'WincUpgradeV1',
    'protocol_class' : None,
    "startup_delay": 0.1,
}

AVRIOT_FW_FUNCTIONS = {
    'iotprovision' : AVRIOT_PROVISION_FW,
    'iotprovision-aws' : AVRIOT_PROVISION_FW,
    'iotprovision-google' : AVRIOT_PROVISION_FW,
    'iotprovision-azure' : AVRIOT_PROVISION_FW,
    'eccprovision' : AVRIOT_PROVISION_FW,
    'wincupgrade' : AVRIOT_WINCUPGRADE_FW,
    'demo-aws' : AVRIOT_AWS_DEMO_FW,
    'demo-google' : AVRIOT_GOOGLE_DEMO_FW,
    'demo-azure' : None,
}

AVRIOT_CELLULAR_FW_FUNCTIONS = {
    'iotprovision' : AVRIOT_CELLULAR_PROVISION_FW,
    'iotprovision-aws' : AVRIOT_CELLULAR_PROVISION_FW,
    'iotprovision-google' : AVRIOT_CELLULAR_PROVISION_FW,
    'iotprovision-azure' : AVRIOT_CELLULAR_PROVISION_FW,
    'eccprovision' : AVRIOT_CELLULAR_PROVISION_FW,
    'wincupgrade' : None,
    'demo-aws' : None,
    'demo-google' : None,
    'demo-azure' : None,
}

AVRIOT_CELLULARMINI_FW_FUNCTIONS = {
    'iotprovision' : AVRIOT_CELLULARMINI_PROVISION_FW,
    'iotprovision-aws' : AVRIOT_CELLULARMINI_PROVISION_FW,
    'iotprovision-google' : AVRIOT_CELLULARMINI_PROVISION_FW,
    'iotprovision-azure' : AVRIOT_CELLULARMINI_PROVISION_FW,
    'eccprovision' : AVRIOT_CELLULARMINI_PROVISION_FW,
    'wincupgrade' : None,
    'demo-aws' : AVRIOT_CELLULARMINI_AWS_DEMO_FW,
    'demo-google' : None,
    'demo-azure' : None,
}

PICIOT_FW_FUNCTIONS = {
    'iotprovision' : PICIOT_PROVISION_FW,
    'iotprovision-aws' : PICIOT_PROVISION_FW,
    'iotprovision-google' : PICIOT_PROVISION_FW,
    'iotprovision-azure' : PICIOT_PROVISION_FW,
    'eccprovision' : PICIOT_PROVISION_FW,
    'wincupgrade' : PICIOT_WINCUPGRADE_FW,
    'demo-aws' : PICIOT_AWS_DEMO_FW,
    'demo-google' : PICIOT_GOOGLE_DEMO_FW,
    'demo-azure' : PICIOT_AZURE_DEMO_FW,
}

SAMIOT_FW_FUNCTIONS = {
    'iotprovision' : SAMIOT_PROVISION_FW,
    'iotprovision-aws' : SAMIOT_PROVISION_FW,
    'iotprovision-google' : SAMIOT_PROVISION_FW,
    'iotprovision-azure' : SAMIOT_PROVISION_FW,
    'eccprovision' : SAMIOT_PROVISION_FW,
    'wincupgrade' : SAMIOT_WINCUPGRADE_FW,
    'demo-aws' : None,
    'demo-google' : SAMIOT_GOOGLE_DEMO_FW,
    'demo-azure' : SAMIOT_AZURE_DEMO_FW,
}

SAMIOT_WX_FW_FUNCTIONS = {
    'iotprovision' : SAMIOT_WX_PROVISION_FW,
    'iotprovision-aws' : SAMIOT_WX_PROVISION_FW,
    'iotprovision-google' : SAMIOT_WX_PROVISION_FW,
    'iotprovision-azure' : SAMIOT_WX_PROVISION_FW,
    'eccprovision' : SAMIOT_WX_PROVISION_FW,
    'wincupgrade' : SAMIOT_WX_WINCUPGRADE_FW,
    'demo-aws' : None,
    'demo-google' : None,
    'demo-azure' : None,
}

TRUSTPLATFORM_FW_FUNCTIONS = {
    'iotprovision' : None,
    'iotprovision-aws' : None,
    'iotprovision-google' : None,
    'iotprovision-azure' : None,
    'eccprovision' : TRUSTPLATFORM_PROVISION_FW,
    'wincupgrade' : None,
    'demo-aws' : None,
    'demo-google' : None,
    'demo-azure' : None,
}

AVR_IOT_KIT = {
    'kit_names' : ['avr-iot wg', 'avr-iot wa'],
    'firmware' : AVRIOT_FW_FUNCTIONS,
    'firmware_variants' : ['aws', 'google', 'azure'],
    'architecture' : 'avr',
    'device' : 'atmega4808',
    'programmer' : 'nedbg',
    'programmer_stack' : 'pymcuprog',
    'leds' : WifiKitLeds()
}

PIC_IOT_KIT = {
    'kit_names' : ['pic-iot wg', 'pic-iot wa'],
    'firmware' : PICIOT_FW_FUNCTIONS,
    'firmware_variants' : ['aws', 'google', 'azure'],
    'architecture' : 'pic',
    'device' : 'pic24fj128ga705',
    'programmer' : 'nedbg',
    'programmer_stack' : 'pymcuprog',
    'leds' : WifiKitLeds()
}

AVR_IOT_CELLULAR_KIT = {
    'kit_names' : ['avr-iot lte-m', 'avr-iot cellular'],
    'firmware' : AVRIOT_CELLULAR_FW_FUNCTIONS,
    'firmware_variants' : ['aws', 'google', 'azure'],
    'architecture' : 'avr',
    'device' : 'avr128db64',
    'programmer' : 'nedbg',
    'programmer_stack' : 'pymcuprog',
    'leds' : CellularKitLeds()
}

AVR_IOT_CELLULARMINI_KIT = {
    'kit_names' : ['avr-iot cellular mini'],
    'firmware' : AVRIOT_CELLULARMINI_FW_FUNCTIONS,
    'firmware_variants' : ['aws', 'google', 'azure'],
    'architecture' : 'avr',
    'device' : 'avr128db48',
    'programmer' : 'nedbg',
    'programmer_stack' : 'pymcuprog',
    'leds' : CellularMiniKitLeds()
}

SAM_IOT_WX_KIT = {
    'kit_names' : ['samd21-iot wx'],
    'firmware' : SAMIOT_WX_FW_FUNCTIONS,
    'firmware_variants' : ['aws', 'google', 'azure'],
    'architecture' : 'sam',
    'device' : 'atsamd21g18a',
    'programmer' : 'nedbg',
    'programmer_stack' : 'pymcuprog',
    'leds' : WifiKitLeds()
}

SAM_IOT_KIT = {
    'kit_names' : ['samd21-iot wg'],
    'firmware' : SAMIOT_FW_FUNCTIONS,
    'firmware_variants' : ['aws', 'google', 'azure'],
    'architecture' : 'sam',
    'device' : 'atsamd21g18a',
    'programmer' : 'nedbg',
    'programmer_stack' : 'pymcuprog',
    'leds' : WifiKitLeds()
}

TRUSTPLATFORM_KIT = {
    'kit_names' : ['cryptoauth trust platform'],
    'firmware' : TRUSTPLATFORM_FW_FUNCTIONS,
    'firmware_variants' : [],
    'architecture' : 'sam',
    'device' : 'atsamd21e18a',
    'programmer' : 'nedbg',
    'programmer_stack' : 'pymcuprog',
    'leds' : TrustplatformKitLeds()
}

SUPPORTED_KITS = [AVR_IOT_KIT, PIC_IOT_KIT, AVR_IOT_CELLULAR_KIT, AVR_IOT_CELLULARMINI_KIT, SAM_IOT_KIT, SAM_IOT_WX_KIT, TRUSTPLATFORM_KIT]

def get_supported_kits():
    """
    Simple accessor of supported kits (and variants thereof)
    """
    return SUPPORTED_KITS

# FIXME: Startup time should probably be specified per application,
# or better, readiness should be signaled by application (eg "READY" message)

class KitApplicationFirmwareProvider():
    """
    Finds applications based on required functionality, device/board and 'cloud provider'.

    Looks in:

    - bundled folders
    - internal server / artifact repo (todo)
    - external server / github (todo)

    :param kitname: Name of kit being used
    :type kitname: str
    :param hexfile_path: Path to hexfile to use
    :type hexfile_path: str, optional
    """
    def __init__(self, kitname, hexfile_path=INSTALLDIR):

        self.logger = getLogger(__name__)
        self.hexfile_path = hexfile_path
        supported_kits = []
        target_kit_name = kitname.lower()
        self.logger.info("Looking for kit matching '%s'", target_kit_name)
        for supported_kit in SUPPORTED_KITS:
            if  target_kit_name in supported_kit['kit_names']:
                supported_kits.append(supported_kit)

        # Too many matches?
        if len(supported_kits) > 1:
            raise KitConnectionError(msg="Too many compatible kits defined", value=supported_kits)

        # Too few matches?
        if len(supported_kits) == 0:
            self.logger.warning("pykitcommander has no support for '%s'", kitname)
            support_list = "Supported kits: "
            for kit in SUPPORTED_KITS:
                for name in kit['kit_names']:
                    support_list += "'{0:s}' ".format(name)
            self.logger.warning(support_list)
            raise KitConnectionError(msg="No compatible kits found", value=supported_kits)

        self.kit_firmware = supported_kits[0]

    def locate_firmware(self, firmware_identifier):
        """
        Looks up and returns firmware for a given identifier

        :param firmware_identifier: Unique ID of firmware
        :type firmware_identifier: str
        :returns: Dictionary containing information about the firmware image
        :rtype: dict
        """
        if firmware_identifier in self.kit_firmware['firmware'].keys():
            # Check that it is defined
            if self.kit_firmware['firmware'][firmware_identifier]:
                self.kit_firmware['firmware'][firmware_identifier]['bundled_firmware'] = os.path.normpath(
                    os.path.join(self.hexfile_path, self.kit_firmware['firmware'][firmware_identifier]['bundled_firmware']))
                self.logger.info("Locating firmware for '%s'", firmware_identifier)
                return self.kit_firmware['firmware'][firmware_identifier]
        self.logger.error("Unable to locate firmware for '%s'", firmware_identifier)
        return {}


class KitProgrammer():
    """
    Programming applications onto kits

    :param serialnumber: Serial number of kit/programmer to connect to
    :type serialnumber: str, optional
    """
    def __init__(self, serialnumber=None):
        self.last_used = None
        self.logger = getLogger(__name__)
        self.logger.info("Connecting to kit...")
        self.programmer = PymcuprogProgrammer(serialnumber=serialnumber, dfp_path=os.path.join(INSTALLDIR, "picpack"))
        kits = self.programmer.get_usable_kits()
        if len(kits) == 0:
            raise KitConnectionError(msg="Kit not found", value=kits)
        if len(kits) > 1:
            raise KitConnectionError(msg="Too many kits available (specific USB serial number required)", value=kits)

        # Only one at this point.
        kit = kits[0]
        serialnumber = kit['serial']
        kitname = self.programmer.read_kit_info('KITNAME').strip("\0")
        self.logger.info("Connected to kit '%s' (%s)", kitname, serialnumber)

        # Attempt to locates a serial port for the kit
        self.logger.debug("Looking for serial port for: %s", serialnumber)
        portmap = SerialPortMap()
        port = portmap.find_serial_port(serialnumber)
        self.logger.debug("Checking access to port: %s", port)
        if not check_access(port):
            self.logger.error("Port '%s' is not accessible", port)
            port = None

        # Store kit info
        self.kit_info = {
            'serialnumber': serialnumber,
            'install_dir' : INSTALLDIR,
            'device_name' : kit['device_name'].lower(),
            'programmer_name' : kit['product'],
            'programmer_id' : kit['product'].split(' ')[0].lower(),
            'kit_name' : kitname,
            'serial_port' : port
        }

    def program_application(self, hexfile, strategy='cached'):
        """
        Programs an application into the kit

        :param hexfile: Path to hex file to program
        :type hexfile: str
        :param strategy: Use caching, or other special mode
        :type strategy: str
        """
        if strategy == "cached":
            if self.last_used == hexfile:
                self.logger.info("Skipping programming as application is cached")
                return
        self.programmer.program_hexfile(filename=hexfile)

    def reset_target(self):
        """
        Resets the target
        """
        self.programmer.reset_target()

    def erase(self):
        """
        Erases the target
        """
        self.programmer.erase_target_device()
        self.last_used = None

    def reboot(self):
        """
        Reboots the debugger
        """
        self.programmer.reboot()
        # TODO - is it usable after this?

    def get_kit_info(self):
        """
        Retrieves kit info dict
        """
        return self.kit_info
