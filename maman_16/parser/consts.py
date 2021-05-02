
INT_OPCODES = [
    "IASN",
    "IPRT",
    "IINP",
    "IEQL",
    "INQL",
    "ILSS",
    "IGRT",
    "IADD",
    "ISUB",
    "IMLT",
    "IDIV"
]

REAL_OPCODES = [
    "RASN",
    "RPRT",
    "RINP",
    "REQL",
    "RNQL",
    "RLSS",
    "RGRT",
    "RADD",
    "RSUB",
    "RMLT",
    "RDIV"
]

CONVERT_OPCODES = ["ITOR", "RTOI"]

JUMP_OPCODES = ["JUMP", "JMPZ"]

HALT_OPCODE = ["HALT"]

QUAD_OPCODES = INT_OPCODES + \
               REAL_OPCODES + \
               CONVERT_OPCODES + \
               JUMP_OPCODES + \
               HALT_OPCODE
