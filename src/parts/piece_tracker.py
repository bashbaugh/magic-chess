"""Board sensing

Detect which pieces have moved
"""

import chess

class MagneticPieceTracker:
    def __init__(self):
        self.move_recieved = False
        self.fromsquare = None
        self.tosquare = None
    
    def piece_moving(self):
        return False
        
    def piece_moved(self):
        move = chess.Move(self.fromsquare, self.tosquare)
        return False if move_recieved else move
        
    def update(self):
        pass
        
