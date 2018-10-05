import logging
import time
import threading

# From TimeMachine
from timeMachine.config import Config
from .myCrypto import MyCrypto
from ..database.models import Bitfinex_DB_Tables, Bitfinex_hourly_Tables, \
    Bitfinex_outsiders, CryptoCompare_DB_Tables, CryptoCompare_hourly_Tables, CryptoCompare_outsiders


log = logging.getLogger(__name__)

"""
Each 'delta' (time interval) create a seperate thread. Each thread is given its own set of coins (DB tables) to update
"""


def main(Session):
    # Start tickToc ( 15 mins )
    msg = 'TickToc'
    tickToc = MyCrypto(Bitfinex_DB_Tables, CryptoCompare_DB_Tables, Config.DELTA)
    watcher = threading.Thread(target=tickToc.getin, args=(Session, msg))
    watcher.start()
    log.info(f"TickToc started {watcher.getName()}")

    # wait then start Hourly ( 1 hour )
    time.sleep(65)
    msg = 'Hourly'
    hourly = MyCrypto(Bitfinex_hourly_Tables, CryptoCompare_hourly_Tables, Config.HOUR)
    peeker = threading.Thread(target=hourly.getin, args=[Session, msg])
    peeker.start()
    log.info(f"Hourly started {peeker.getName()}")

    # wait then start outsider ( 3 hours )
    time.sleep(65)
    msg = 'Outsider'
    outsider = MyCrypto(Bitfinex_outsiders, CryptoCompare_outsiders, Config.OUTSIDER)
    stalker = threading.Thread(target=outsider.getin, args=[Session, msg], kwargs={'showCoins': True})
    stalker.start()
    log.info(f"Outsider started {stalker.getName()}")
