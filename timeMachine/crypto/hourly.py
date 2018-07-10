import logging
import time

# From TimeMachine
from .monitor import Monitor
from .utils import Return_API_response
from ..database.bitfinexAPI import BitfinexAPI
from ..database.cryptoCompareAPI import CompareAPI
from ..database.models import Bitfinex_hourly_Tables, CryptoCompare_hourly_Tables

log = logging.getLogger(__name__)

bitfinexURL = 'https://api.bitfinex.com/v2/candles/trade:'
compareURL = 'https://min-api.cryptocompare.com/data/histohour?'
dbTables = {**Bitfinex_hourly_Tables, **CryptoCompare_hourly_Tables}


def hourly(delta, interval, Session):
    """Running in it's own thread this adds a new row to the DB tables"""
    monitor = Monitor(Session, dbTables)
    # monitor.initCoin(Session, dbTables)

    while True:
        session = Session()
        try:
            CompareAPI.chunk(session, delta, compareURL, interval, CryptoCompare_hourly_Tables)
        except:
            session.rollback()
            log.error("Hourly CompareAPI Error", exc_info=True)
        finally:
            session.close()
            log.info('Hourly CompareAPI complete')


        session = Session()
        try:
            BitfinexAPI.chunk(session, delta, bitfinexURL,
                              interval, Bitfinex_hourly_Tables)
        except:
            session.rollback()
            log.error("Hourly BitfinexAPI Error", exc_info=True)
        finally:
            session.close()
            log.info('Hourly BitfinexAPI, Hourly complete')


        session = Session()
        try:
            monitor.check(session)
        except:
            session.rollback()
            log.error('Oh Hourly monitor rollback', exc_info=True)
        finally:
            session.close()
            log.info('Hourly Monitor complete')

        # set the tickTock ...
        time.sleep(interval[delta])
