"""Board sensing

Detect which pieces have moved
"""

import chess
from lib.MCP23017 import MCP23017
from logger import logger
from time import sleep

class MagneticPieceTracker:
    def __init__(self):
        self.mcp1 = MCP23017(0x20, 16)
        self.mcp2 = MCP23017(0x21, 16)
        self.mcp3 = MCP23017(0x22, 16)
        self.mcp4 = MCP23017(0x23, 16)

        logger.info("MagneticPieceTracker initialized")

    
        
