import logging
import time
import threading

# From TimeMachine
from timeMachine.config import Config
from .myCrypto import MyCrypto


log = logging.getLogger(__name__)

"""
For each 'delta' (time interval) create a seperate thread.
Each thread is given its own set of coins (DB tables) to update
"""


def main():
    # Start tickToc ( 15 mins )
    msg = 'TickToc'
    tickToc = MyCrypto(Config.DELTA)
    watcher = threading.Thread(target=tickToc.getin, args=[msg])
    watcher.start()
    log.info(f"TickToc started {watcher.getName()} - id - {watcher.ident}")

    # wait then start Hourly ( 1 hour )
    time.sleep(65)
    msg = 'Hourly'
    hourly = MyCrypto(Config.HOUR)
    peeker = threading.Thread(target=hourly.getin, args=[msg])
    peeker.start()
    log.info(f"Hourly started {peeker.getName()} - id - {peeker.ident}")

    # wait then start outsider ( 3 hours )
    time.sleep(65)
    msg = 'Outsider'
    outsider = MyCrypto(Config.OUTSIDER)
    seeker = threading.Thread(target=outsider.getin, args=[msg], kwargs={'showCoins': True})
    seeker.start()
    log.info(f"Outsider started {seeker.getName()} - id - {seeker.ident}")
