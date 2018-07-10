import logging
import time

# From TimeMachine
from .monitor import Monitor
from .utils import Return_API_response
from ..database.bitfinexAPI import BitfinexAPI
from ..database.cryptoCompareAPI import CompareAPI
from ..database.models import Bitfinex_outsiders, CryptoCompare_outsiders

log = logging.getLogger(__name__)

bitfinexURL = 'https://api.bitfinex.com/v2/candles/trade:'
compareURL = 'https://min-api.cryptocompare.com/data/histohour?'
dbTables = {**Bitfinex_outsiders, **CryptoCompare_outsiders}


def outsider(delta, interval, Session):
    """Longer interval 3 hour sample rate for the lowest volume coins"""
    monitor = Monitor(dbTables)
    monitor.initCoin(Session, dbTables)

    while True:
        session = Session()
        try:
            CompareAPI.chunk(session, delta, compareURL, interval, CryptoCompare_outsiders)
        except:
            session.rollback()
            log.error("Outsider CompareAPI Error", exc_info=True)
        finally:
            session.close()
            log.info('Outsider, CompareAPI complete')


        session = Session()
        try:
            BitfinexAPI.chunk(session, delta, bitfinexURL, interval, Bitfinex_outsiders)
        except:
            session.rollback()
            log.error("Outsider BitfinexAPI Error", exc_info=True)
        finally:
            session.close()
            log.info('Outsider, BitfinexAPI complete')


        session = Session()
        try:
            monitor.check(session)
        except:
            session.rollback()
            log.error('Oh Outsider monitor rollback', exc_info=True)
        finally:
            session.close()
            log.info('Outsider Monitor complete')

        time.sleep(interval[delta])
