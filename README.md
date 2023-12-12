[![MCHP](images/microchip.png)](https://www.microchip.com)

# pykitcommander - Python Kit Commander
pykitcommander manages interaction with Microchip development kits based on PKOB nano on-board debugger

Install using pip from [pypi.org](https://pypi.org/project/pykitcommander/):
```bash
pip install pykitcommander
```

Browse source code on [github](https://github.com/microchip-pic-avr-tools/pykitcommander)

Read API documentation on [github](https://microchip-pic-avr-tools.github.io/pykitcommander)

Read the changelog on [github](https://github.com/microchip-pic-avr-tools/pykitcommander/blob/main/CHANGELOG.md)

## Background
In many situations interaction with peripheral hardware components on a development kit is done via a "bridge" application running on the MCU on that kit.  To achieve this, the bridge firmware must be programmed onto that MCU, and then communications over a given channel and protocol can logically link the host computer to the peripheral components.

pykitcommander manages all aspects of this interaction.

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

For usage examples see pypi.md.

## Notes for Linux® systems
This package uses pyedbglib and other libraries for USB transport and some udev rules are required. For details see the pyedbglib package: https://pypi.org/project/pyedbglib
