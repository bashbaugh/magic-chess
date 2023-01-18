# Chessboard Configuration

import logging
import os

# Project location, don't change this:
SRC_DIR = os.path.dirname(os.path.realpath(__file__))
BASE_DIR = os.path.join(SRC_DIR, '../')

SHUTDOWN_AT_END = False # Shutdown pi at end of program
RESTART_ON_CRASH = True # Restart when program crashes
MAXIMUM_CRASHES = 2 # Maximum number of restarts

PROCESS_NAME = 'magic-chess'

LOGGING_LEVEL = logging.INFO # Minimum level for logging messages stored in logs
LOGGING_FORMAT = '%(asctime)-10s CHESS |%(levelname)s: %(message)s' # Log message format
LOGGING_DATE_FORMAT = '%m-%d %H:%M:%S' # Log message date format
LOGGING_BACKUP_COUNT = 3 # Number of log files
LOG_FILE_MAX_BYTES = 30000 # Max bytes per log file
