"""Board sensing

Detect which pieces have moved
"""

import chess
from lib.MCP23017 import MCP23017
from logger import logger
from time import sleep

class MagneticPieceTracker:
    def __init__(self):
        self.mcp = [
            MCP23017(0x20, 16),
            MCP23017(0x21, 16),
            MCP23017(0x22, 16),
            MCP23017(0x23, 16)
        ]

        self.mcp[3].pullUp(15, 1)

        logger.info("MagneticPieceTracker initialized")

    def read_val(self):
        return self.mcp[3].input(15)

    
        
