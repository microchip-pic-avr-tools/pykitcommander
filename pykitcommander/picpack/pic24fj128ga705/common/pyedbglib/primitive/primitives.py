"""
List of available primitives
"""

# Lambda construct.  Not a GEN4 primitive
LAMBDA = 0xAD

# GEN4 compatible* primitives
SET_VPP_ON = 0xB0
DELAY_US = 0xA0
DELAY_MS = 0x94
SET_ICSP_PINS = 0xB2
GET_ICSP_PINS = 0x32
SET_VPP_OFF = 0xB1
WRITE_LITERAL_32_LSB = 0xB4
WRITE_BITS_LITERAL = 0xB5
P16ENV3_WRITE_PAYLOAD_PARAM = 0x86
P16ENV3_WRITE_PAYLOAD_LITERAL = 0x87
P16ENV3_WRITE_BUFFER = 0x88
P16ENV3_WRITE_BUFFER_DFM = 0x49
P16ENV3_READ_PAYLOAD_PFM = 0x84
P16ENV3_READ_PAYLOAD_DFM = 0x48
WRITE_BITS_LITERAL_MSB = 0x83
SET_CLK_HI = 0xBA
SET_CLK_LO = 0xBB
P16F_READ_LOC_BUFFER = 0x80
P16F_WRITE_LOC_BUFFER = 0x81

DE_COMMAND = 0x31

COREINST24 = 0xE0
VISI24 = 0xE2

P24_SEND_PE_WORD = 0xE7
P24_SEND_PE_WORD_BUF = 0xE8
P24_PE_HANDSHAKE = 0xE9
P24_RECEIVE_PE_WORD = 0xEA

SET_SPEED = 0xEC
GET_SPEED = 0xED

# Useful ICSP_PINS macro expansions
ICSP_PINS_ALL_LOW = 0
ICSP_PINS_CLK_IN_DATA_IN = 3
ICSP_PINS_CLK_HIGH_DATA_LOW = 4
ICSP_PINS_CLK_HIGH_DATA_IN = 6
ICSP_PINS_CLK_LOW_DATA_IN = 2

# define SE_ICSP_PIN_CLK_DIR_BIT     0
# define SE_ICSP_PIN_DATA_DIR_BIT    1
# define SE_ICSP_PIN_CLK_VALUE_BIT   2
# define SE_ICSP_PIN_DATA_VALUE_BIT  3

# define SE_ISCP_CLK_INPUT       (1 << SE_ICSP_PIN_CLK_DIR_BIT)
# define SE_ISCP_DATA_INPUT      (1 << SE_ICSP_PIN_DATA_DIR_BIT)
# define SE_ISCP_CLK_HIGH        (1 << SE_ICSP_PIN_CLK_VALUE_BIT)
# define SE_ISCP_DATA_HIGH       (1 << SE_ICSP_PIN_DATA_VALUE_BIT)
