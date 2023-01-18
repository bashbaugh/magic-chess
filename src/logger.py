import logging
from logging.handlers import RotatingFileHandler
import config as cfg

logging_formatter = logging.Formatter(cfg.LOGGING_FORMAT, cfg.LOGGING_DATE_FORMAT)

logging_sh = logging.StreamHandler()
logging_sh.setLevel(logging.DEBUG)
logging_sh.setFormatter(logging_formatter)

logging_rfh = RotatingFileHandler(cfg.BASE_DIR + 'logs/chessboard.log', maxBytes=cfg.LOG_FILE_MAX_BYTES, backupCount=cfg.LOGGING_BACKUP_COUNT)
logging_rfh.setLevel(cfg.LOGGING_LEVEL)
logging_rfh.setFormatter(logging_formatter)

logger = logging.getLogger("chess-logger")
logger.setLevel(logging.DEBUG)
logger.addHandler(logging_sh)
logger.addHandler(logging_rfh)
