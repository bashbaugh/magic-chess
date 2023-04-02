"""Open Magic Chess

https://github.com/bashbaugh/open-magic-chess

Copyright (c) 2023 Benjamin Ashbaugh
Licensed under MIT license, located in /LICENSE
"""

from time import sleep, time

import config as cfg

from threading import Thread
from queue import Queue
import traceback
from setproctitle import *
import socket
import os
from math import floor

import chess
import chess.engine

from constants import *
from logger import logger
from parts import piece_tracker, actuator, leds
from gatt_server import BleApplication

# Set process name so that it can be easily found/killed:
setproctitle(cfg.PROCESS_NAME)

# Create logs and saves directory:
if not os.path.isdir(cfg.BASE_DIR + 'logs'):
    os.mkdir(cfg.BASE_DIR + 'logs')
if not os.path.isdir(cfg.BASE_DIR + 'data'):
    os.mkdir(cfg.BASE_DIR + 'data')

crash_counter = 0

class Board:
    """ Magic chess board
    """
    
    def __init__(self, ble_app):
        self.game = None
        
        # Parts
        # If you want to use a customized part just replace any of these class names with your own.
        # self.led = leds.Neopixel_RGB_LEDs(self.log_warning)
        # self.pieces = piece_tracker.MagneticPieceTracker()
        self.magnet = actuator.StepperMagnetActuator()        
        
        # In-game variables
        # self.white_clock_time = None
        # self.black_clock_time = None
        # self.last_update = 0
        # self.ptype = None # Current player type
        # self.last_BWcolors = ("off", "off")
        
        # Game options
        # self.mode = None
        # self.flip_board = None
        # self.white_type = None
        # self.black_type = None
        # self.player_color = None
        # self.engine_time_limit = None
        # self.use_clock = None
        # self.clock_time = None
        # self.clock_time_increment = None
        
        # Engine
        self.engine = chess.engine.SimpleEngine.popen_uci("/usr/games/stockfish")
        self.engine_process = None
        self.engine_results =  []

        # Bluetooth
        self.ble_app = ble_app
        self.ble_app.setBoard(self)
        self.ble_thread = Thread(target=self.ble_thread_run)
        self.ble_thread.start()
        logger.info("Started BLE Thread")

        self.magnet.home()
        
        # self.led.rainbow(40)

    def ble_thread_run(self):
        self.ble_app.run()
            
    def main(self):
        try:
            while True:
                pass
        except KeyboardInterrupt:
            logger.debug("Keyboard Interrupt")
            self.shutdown()
        
    def clear_board(self):
        self.game = chess.Board()
            
    def _check_local_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('10.255.255.255', 1))
            hostname = s.getsockname()[0]
            # self.confirm("Local IP is:", hostname)
        except OSError:
            pass
            # self.confirm("Network", "Unreachable")
        finally:
            s.close()
            
    def play_engine(self):
        result = self.engine.play(self.game, chess.engine.Limit(time=self.engine_time_limit))
        self.engine_results.append(result)
        
    @staticmethod
    def log_warning(msg):
        logger.warning(msg)

    def shutdown(self):
        # self.led.shutdown()
        # self.status = SHUTDOWN
        self.magnet.shutdown()

def start():
    global crash_counter
    try:
        ble_app = BleApplication()
        board = Board(ble_app)
        board.main()
    except Exception as e:
        crash_counter += 1

        ble_app.quit()
        board.shutdown()
        
        logger.error("Program crashed")
        logger.critical(traceback.format_exc())
        if crash_counter >= cfg.MAXIMUM_CRASHES:
            logger.warning("Maximum crashes reached. Stopping.")
            return
        
        # if cfg.RESTART_ON_CRASH:
        #     logger.info("Restarting...")
        #     start()

if __name__ == "__main__":
    start()

if cfg.SHUTDOWN_AT_END:
    logger.info("Shutting Down")
    os.system("sudo shutdown -h now")
