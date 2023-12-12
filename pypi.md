# pykitcommander
pykitcommander manages interaction with Microchip development kits based on PKOB nano on-board debugger

![PyPI - Format](https://img.shields.io/pypi/format/pykitcommander)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pykitcommander)
![PyPI - License](https://img.shields.io/pypi/l/pykitcommander)

## Overview
pykitcommander is available:

* install using pip from pypi: https://pypi.org/project/pykitcommander
* browse source code on github: https://github.com/microchip-pic-avr-tools/pykitcommander
* read API documentation on github: https://microchip-pic-avr-tools.github.io/pykitcommander

## Background
In many situations interaction with peripheral hardware components on a development kit is done via a "bridge" application running on the MCU on that kit.  To achieve this, the bridge firmware must be programmed onto that MCU, and then communications over a given channel and protocol can logically link the host computer to the peripheral components.

pykitcommander manages some aspects of this interaction by:
- Containing a registry of application hex files for various applications on various kits
- Programming the application onto the kit
- Providing a most-probable serial-port connection string for that kit
- Providing an indication of what protocol format is in use on the application
- Supporting common protocol framing formats being used

## Usage
pykitcommander is intended to be used as a library.
Its primary consumers are:
- pytrustplatform (www.pypi.org/project/pytrustplatform)
- iotprovision (www.pypi.org/project/iotprovision)

Supported kits are:
- AVR-IoT WG and WA
- PIC-IoT WG and WA
- AVR-IoT Cellular Mini
- SAM-IoT WG
- SAM-IoT Wx V2
- CryptoAuth Trust Platform Development Kit

## Simple example
This example shows how pykitcommander can be used to read the serial number from an ECC608 device.  This device is connected to the MCU on the board (either PIC or AVR depending on the variant).  The MCU is connected to the host computer via a virtual serial port provided by the on-board debugger.

This example uses the 'setup_kit("iotprovision")' helper function to achieve this very simply.
```python
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

    # Read out firmware version
    version = firmware_driver.firmware_command("MC+VERSION=FIRMWARE")

    # Send firmware command to turn LED on
    firmware_driver.firmware_command("MC+SETLED", ["conn","on"])

    # Send firmware command to read the ECC serial number
    ecc_serial_number = firmware_driver.firmware_command("MC+ECC+SERIAL")
    print("ECC serial number read out: '{}'".format(ecc_serial_number))

    # Send firmware command to turn LED off
    firmware_driver.firmware_command("MC+SETLED", ["conn","off"])
```

## DIY example
This example shows how pykitcommander can be used to read the serial number from an ECC608 device.  In this case, the firmware you use is your own, but complies to the same protocol as the standard provisioning firmware. The MCU is connected to the host computer via a virtual serial port provided by the on-board debugger.  In this example the serial port and baud rate are also specified explicitly.

```python

# Program firmware onto the kit
from pykitcommander.kitmanager import KitProgrammer

programmer = KitProgrammer()
programmer.program_application("my_firmware.hex")

# Create a serial connection to communicate with the firmware
# Note: SerialCDC class wraps pyserial Serial class
from pyedbglib.serialport.serialcdc import SerialCDC
with SerialCDC("COM3", 115200, timeout=10, stopbits=2) as serial_connection:
    # The firmware driver wraps this serial connection which enables a simple command-response transaction
    # This is defined in pykitcommander
    from pykitcommander.firmwareinterface import ProvisioningFirmwareDriver
    firmware_driver = ProvisioningFirmwareDriver(serial_connection)

    # Read out firmware version
    version = firmware_driver.firmware_command("MC+VERSION=FIRMWARE")

    # Send firmware command to turn LED on
    firmware_driver.firmware_command("MC+SETLED", ["conn","on"])

    # Send firmware command to read the ECC serial number
    ecc_serial_number = firmware_driver.firmware_command("MC+ECC+SERIAL")
    print("ECC serial number read out: '{}'".format(ecc_serial_number))

    # Send firmware command to turn LED off
    firmware_driver.firmware_command("MC+SETLED", ["conn","off"])
```

## Logging
This package uses the Python logging module for publishing log messages to library users.
A basic configuration can be used (see example below), but for best results a more thorough configuration is
recommended in order to control the verbosity of output from dependencies in the stack which also use logging.

```python
# pykitcommander uses the Python logging module
import logging
logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.WARNING)
```

## Notes for Linux® systems
This package uses pyedbglib and other libraries for USB transport and some udev rules are required. For details see the pyedbglib package: https://pypi.org/project/pyedbglib