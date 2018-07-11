import logging
import time

# package imports
from .monitor import Monitor
from ..database.bitfinexAPI import BitfinexAPI
from ..database.cryptoCompareAPI import CompareAPI


log = logging.getLogger(__name__)


class MyCrypto:
    """ Instances run in their own thread each for a different sample frequency
    'delta'.
    Collect data from Bitfinex and CryptoCompare monitor it, then
    save it to the Database """
    def __init__(self, Bitfinex_DB_Tables, CryptoCompare_DB_Tables, delta):
        self.Bitfinex_DB_Tables = Bitfinex_DB_Tables
        self.CryptoCompare_DB_Tables = CryptoCompare_DB_Tables
        self.dbTables = {**Bitfinex_DB_Tables, **CryptoCompare_DB_Tables}
        self.delta = delta


    def getin(self, Session):
        """Running in it's own thread this continually (frequency=delta) adds a
         new row to the Database"""

        monitor = Monitor(Session, self.dbTables)

        interval = {'5m': 300, '15m': 900, '30m': 1800, '1h': 3600, '3h': 10800}
        bitfinexURL = 'https://api.bitfinex.com/v2/candles/trade:'
        if self.delta == '15m':
            compareURL = 'https://min-api.cryptocompare.com/data/histominute?'
        else:
            compareURL = 'https://min-api.cryptocompare.com/data/histohour?'


        while True:
            session = Session()
            try:
                CompareAPI.chunk(session, self.delta, compareURL,
                                interval, self.CryptoCompare_DB_Tables)
            except:
                session.rollback()
                log.error("CompareAPI Error", exc_info=True)
            finally:
                session.close()
                log.info(f'CompareAPI "{self.delta}" complete')

            session = Session()
            try:
                BitfinexAPI.chunk(session, self.delta, bitfinexURL,
                                interval, self.Bitfinex_DB_Tables)
            except:
                session.rollback()
                log.error("BitfinexAPI Error", exc_info=True)
            finally:
                session.close()
                log.info(f'BitfinexAPI "{self.delta}" complete')

            session = Session()
            try:
                monitor.check(session)
            except:
                session.rollback()
                log.error('Oh tickToc monitor rollback', exc_info=True)
            finally:
                session.close()
                log.info(f'"{self.delta}" Monitor complete')

            # set the tickTock ...
            time.sleep(interval[self.delta])
