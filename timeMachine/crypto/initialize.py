import logging, time
import threading

# From TimeMachine
from timeMachine.config import Config
from .utils import DF_Tables
from .tickToc import tickToc
from .outsider import outsider
from .hourly import  hourly


log = logging.getLogger(__name__)

# initialize globals
interval = {'5m': 300, '15m': 900, '30m': 1800, '1h': 3600, '3h': 10800}

def main(Session):
    # Start tickToc ( 15 mins )
    watcher = threading.Thread(target=tickToc, args=[Config.DELTA, interval, Session])
    watcher.start()
    log.info(f"TickToc started {watcher.getName()}")


    # wait then start Hourly
    time.sleep(65)
    peeker = threading.Thread(target=hourly, args=[Config.HOUR, interval, Session])
    peeker.start()
    log.info(f"Hourly started {peeker.getName()}")


    # wait then start outsider ( 3 hours )
    time.sleep(65)
    stalker = threading.Thread(target=outsider, args=[Config.OUTSIDER, interval, Session])
    stalker.start()
    log.info(f"Outsider started {stalker.getName()}")
