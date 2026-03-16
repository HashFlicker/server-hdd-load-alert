import logging, os, sys
from datetime import datetime
import pytz

def log_setup(name, log_file, level=logging.INFO):

    # Log File location
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    # Log level setup
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Prevent Duplicate Log
    if logger.hasHandlers():
        return logger
    
    def wibTime(*args):
        utc_dt = datetime.now(pytz.utc)
        wib_dt = pytz.timezone('Asia/Jakarta')
        return utc_dt.astimezone(wib_dt).timetuple()
        
    # Log Format
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] [%(name)s] %(message)s")
    formatter.converter = wibTime

    # Log File Handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Log Stream Handler
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    logger.propagate = False
    return logger

