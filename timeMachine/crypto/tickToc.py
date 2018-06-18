import logging
import time

# From TimeMachine
from .utils import Return_API_response
from ..database.bitfinexAPI import BitfinexAPI
from ..database.cryptoCompareAPI import CompareAPI

log = logging.getLogger(__name__)

bitfinexURL = 'https://api.bitfinex.com/v2/candles/trade:'
compareURL = 'https://min-api.cryptocompare.com/data/histominute?'


def tickToc(delta, interval, Session):
    """Running in it's own thread this adds a new row to the DB tables"""

    while True:
        session = Session()
        try:
            CompareAPI.chunk(session, delta, compareURL, interval)
        except:
            session.rollback()
            log.error("CompareAPI Error", exc_info=True)
        finally:
            session.close()
            log.info('CompareAPI complete')

        session = Session()
        try:
            BitfinexAPI.chunk(session, delta, bitfinexURL, interval)
        except:
            session.rollback()
            log.error("BitfinexAPI Error", exc_info=True)
        finally:
            session.close()
            log.info('BitfinexAPI, Ticktoc complete')

        # set the tickTock ...
        time.sleep(interval[delta])
