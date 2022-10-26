"""
pykitcommander - Python Kit Commander
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

pykitcommander manages interaction with Microchip development kits based on
PKOB nano on-board debugger

In many situations interaction with peripheral hardware components on a
development kit is done via a "bridge" application running on the MCU on that
kit.  To achieve this, the bridge firmware must be programmed onto that MCU,
and then communications over a given channel and protocol can logically link
the host computer to the peripheral components.

pykitcommander manages some aspects of this interaction by:

- Containing a registry of application hex files for various applications on various kits
- Programming the application onto the kit
- Providing a most-probable serial-port connection string for that kit
- Providing an indication of what protocol format is in use on the application
- Supporting common protocol framing formats being used

Supported kits are:
    * AVR-IoT WG and WA
    * PIC-IoT WG and WA
    * AVR-IoT Cellular Mini
    * SAM-IoT WG
    * CryptoAuth Trust Platform Development Kit    

Overview
~~~~~~~~

pykitcommander is available:
    * install using pip from pypi: https://pypi.org/project/pykitcommander
    * browse source code on github: https://github.com/microchip-pic-avr-tools/pykitcommander
    * read API documentation on github: https://microchip-pic-avr-tools.github.io/pykitcommander
    * read the changelog on github: https://github.com/microchip-pic-avr-tools/pykitcommander/blob/main/CHANGELOG.md

Usage example
~~~~~~~~~~~~~
Usage in AVR-IoT and PIC-IoT kits:

.. code-block:: python

    from pykitcommander.kitprotocols import setup_kit

    # Request iotprovision protocol to be set up on a connected kit
    info = setup_kit("iotprovision")

    # Create a serial connection to communicate with the firmware
    # Note: SerialCDC class wraps pyserial Serial class
    from pyedbglib.serialport.serialcdc import SerialCDC
    with SerialCDC(info['port'], info['protocol_baud'], timeout=10, stopbits=2) as serial_connection:
        # The firmware driver wraps this serial connection which enables a simple command-response transaction
        # This is defined in pykitcommander
        from pykitcommander.firmwareinterface import ProvisioningFirmwareDriver
        firmware_driver = ProvisioningFirmwareDriver(serial_connection)

        # Send firmware command to turn LED on
        firmware_driver.firmware_command("MC+SETLED", ["conn","on"])

        # Send firmware command to read the ECC serial number
        ecc_serial_number = firmware_driver.firmware_command("MC+ECC+SERIAL")
        print("ECC serial number read out: '{}'".format(ecc_serial_number))

        # Send firmware command to turn LED off
        firmware_driver.firmware_command("MC+SETLED", ["conn","off"])


Notes for Linux® systems
~~~~~~~~~~~~~~~~~~~~~~~~
This package uses pyedbglib and other libraries for USB transport and some udev rules are required.
For details see the pyedbglib package: https://pypi.org/project/pyedbglib
"""
import logging
logging.getLogger(__name__).addHandler(logging.NullHandler())
