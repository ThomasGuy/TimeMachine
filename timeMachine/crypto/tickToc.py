import logging
import time

# From TimeMachine
from .monitor import Monitor
from .utils import Return_API_response
from ..database.bitfinexAPI import BitfinexAPI
from ..database.cryptoCompareAPI import CompareAPI
from ..database.models import Bitfinex_DB_Tables, CryptoCompare_DB_Tables

log = logging.getLogger(__name__)

bitfinexURL = 'https://api.bitfinex.com/v2/candles/trade:'
compareURL = 'https://min-api.cryptocompare.com/data/histominute?'
dbTables = {**Bitfinex_DB_Tables, **CryptoCompare_DB_Tables}


def tickToc(delta, interval, Session):
    """Running in it's own thread this adds a new row to the DB tables"""
    monitor = Monitor(Session, dbTables)
    # monitor.initCoin(Session, dbTables)

    while True:
        session = Session()
        try:
            CompareAPI.chunk(session, delta, compareURL, interval, CryptoCompare_DB_Tables)
        except:
            session.rollback()
            log.error("CompareAPI Error", exc_info=True)
        finally:
            session.close()
            log.info('CompareAPI complete')


        session = Session()
        try:
            BitfinexAPI.chunk(session, delta, bitfinexURL,
                              interval, Bitfinex_DB_Tables)
        except:
            session.rollback()
            log.error("BitfinexAPI Error", exc_info=True)
        finally:
            session.close()
            log.info('BitfinexAPI, Ticktoc complete')


        session = Session()
        try:
            monitor.check(session)
        except:
            session.rollback()
            log.error('Oh tickToc monitor rollback', exc_info=True)
        finally:
            session.close()
            log.info('TickToc Monitor complete') 

        # set the tickTock ...
        time.sleep(interval[delta])
