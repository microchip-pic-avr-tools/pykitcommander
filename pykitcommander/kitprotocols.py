"""
Helper functions for setting up simple applications
"""
from time import sleep
from logging import getLogger

from .kitmanager import KitApplicationFirmwareProvider
from .kitmanager import KitProgrammer
from .kitcommandererrors import ProgrammingError

def setup_kit(function, skip_programming=False, serialnumber=None, programmer=None):
    """
    Sets up a kit for communication

    :param function: Requested function of the kit
    :type function: str
    :param skip_programming: Set to true to not program the kit
    :type skip_programming: boolean
    :param serialnumber: Serial number of kit to connect to
    :type serialnumber: str
    :param programmer: Optional programmer object to use
    :type programmer: object (KitProgrammer)
    """
    logger = getLogger(__name__)

    # If programmer object is not passed in, create one here for single-use
    if not programmer:
        programmer = KitProgrammer(serialnumber=serialnumber)

    # Select application for this function on this kit
    application_provider = KitApplicationFirmwareProvider(kitname=programmer.kit_info['kit_name'])
    application = application_provider.locate_firmware(firmware_identifier=function)

    # If an application was requested, and it can't be found, an exception is raised
    if not application and not skip_programming:
        raise ProgrammingError("No application information for '{}'".format(function))

    # Locate the serial port provided by this kit
    port = programmer.kit_info['serial_port']

    kit_info = {
        'port' : port,
        'application_info' : application,
        'kit_info' : programmer.kit_info
    }
    # Add LED definitions to kit info.
    # These are used when accessing LEDs through the MC+SETLED and MC+GETLED commands
    kit_info['kit_info']['leds'] = application_provider.kit_firmware['leds']

    # Handle kit programming, if required
    if skip_programming:
        # Make sure firmware is in known state
        programmer.reset_target()
    else:
        # Show information
        logger.debug("Programming '%s' version '%s'", application['description'], application['bundled_firmware_version'])
        programmer.program_application(application['bundled_firmware'])

    if application:
        # Provide protocol info for this FW
        kit_info['protocol_baud'] = application['protocol_baud']
        kit_info['protocol_id'] = application['protocol_id']
        kit_info['protocol_class'] = application['protocol_class']
        kit_info['startup_delay'] = application['startup_delay']
        # Log attributes of the connection: port, baud, identity
        logger.info("Setup protocol '%s' on %s at %d on kit '%s'",
                    application['protocol_id'],
                    port,
                    application['protocol_baud'],
                    programmer.kit_info['kit_name'])
    else:
        # We have no protocol info, user is on their own
        kit_info['protocol_baud'] = None
        kit_info['protocol_id'] = None
        kit_info['protocol_class'] = None
        kit_info['startup_delay'] = None
        logger.warning("No protocol information available for: '%s'", function)

    # Some firmwares may require a delay after programming/reset before being ready for communication.
    if kit_info['startup_delay']:
        sleep(kit_info['startup_delay'])

    # Return info to caller
    return kit_info

def get_iot_provision_protocol(skip_programming=False, serialnumber=None):
    """
    Back compatibility API - render "not supported" message.
    """
    raise Exception("This API is no longer supported - please update your client.")

def get_protocol(protocol_name, skip_programming=False, serialnumber=None):
    """
    Back compatibility API - render "not supported" message.
    """
    raise Exception("This API is no longer supported - please update your client.")
