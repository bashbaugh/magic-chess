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

        # Pull up all inputs
        for i in range(16 * 4):
            self.mcp[i // 16].pullUp(i % 16, 1)

    def read_val(self):
        return self.mcp[3].input(15)

pt = MagneticPieceTracker()
    
while True:
    ins = []
    for i in range(16 * 4):
        ins.append(pt.mcp[i // 16].input(i % 16))

    # print(ins)
    #print number of 0s
    print("PIECES ON BOARD: " + str(ins.count(0)))

    sleep(0.2)
        
