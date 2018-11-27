import logging
import time

# package imports
from .monitor import Monitor
from ..database.cryptoAPIs import Bitfinex, Compare
from ..database.base import engine


log = logging.getLogger(__name__)


class MyCrypto:
    """ Instances run continuously in it's own thread for a sample frequency 'delta'.
    Collect data from Bitfinex and CryptoCompare, then save it to the Database """

    interval = {'15m': 900, '1h': 3600, '3h': 10800, '6h': 21600, '1D': 86400}

    def __init__(self, Bitfinex_DB_Tables, Compare_DB_Tables, delta, **kwargs):
        self.Bitfinex_DB_Tables = Bitfinex_DB_Tables
        self.Compare_DB_Tables = Compare_DB_Tables
        self.dbTables = {**Bitfinex_DB_Tables, **Compare_DB_Tables}
        self.delta = delta

    def getin(self, Session, msg, showCoins=False):
        """(frequency=delta) adds bulk rows to the Database"""

        monitor = Monitor(Session, self.dbTables)

        while True:
            with engine.begin() as conn:
                session = Session()
                try:
                    compare = Compare(self.Compare_DB_Tables, self.delta, self.interval[self.delta])
                    compare.chunk(session, conn)
                except Exception:
                    session.rollback()
                    log.error(f'CompareAPI "{self.delta}" Error', exc_info=True)
                finally:
                    session.close()
                    log.info(f'CompareAPI "{self.delta}" complete')

                session = Session()
                try:
                    bitfinex = Bitfinex(self.Bitfinex_DB_Tables, self.delta, self.interval[self.delta])
                    bitfinex.chunk(session, conn)
                except Exception:
                    session.rollback()
                    log.error(f'BitfinexAPI "{self.delta}" Error', exc_info=True)
                finally:
                    session.close()
                    log.info(f'BitfinexAPI "{self.delta}" complete')

                log.info(f'"{self.delta}" {msg} update completed')

            session = Session()
            try:
                monitor.check(session)
            except Exception:
                session.rollback()
                log.error(f'Oh "{self.delta}" monitor rollback', exc_info=True)
            finally:
                session.close()
                # log.info(f'"{self.delta}" Monitor complete')

            log.info(f'"{self.delta}" {msg} update completed')

            if showCoins:
                log.info(f'{monitor}')

            # set the tickTock ...
            time.sleep(self.interval[self.delta])
