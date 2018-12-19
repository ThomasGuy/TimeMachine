import logging
import time

# third party imports
from sqlalchemy.orm import scoped_session

# package imports
from .monitor import Monitor
from ..database.cryptoAPIs import Bitfinex, Compare, Binance
from timeMachine import engine, session_factory


log = logging.getLogger(__name__)


class MyCrypto:
    """ Instances run continuously in it's own thread for a sample frequency 'delta'.
    Collect data from Bitfinex and CryptoCompare, then save it to the Database """

    interval = {'15m': 900, '1h': 3600, '3h': 10800, '6h': 21600, '1D': 86400}

    def __init__(self, delta, **kwargs):
        self.delta = delta
        self.Session = scoped_session(session_factory)

    def getin(self, msg, showCoins=False):
        """(frequency=delta) adds bulk rows to the Database"""

        monitor = Monitor(self.Session, self.delta)

        while True:
            with engine.begin() as conn:
                session = self.Session()
                try:
                    compare = Compare(self.delta, self.interval[self.delta])
                    compare.chunk(session, conn)
                except Exception:
                    session.rollback()
                    log.error(f'CompareAPI "{self.delta}" Error', exc_info=True)
                finally:
                    session.close()

                session = self.Session()
                try:
                    bitfinex = Bitfinex(self.delta, self.interval[self.delta])
                    bitfinex.chunk(session, conn)
                except Exception:
                    session.rollback()
                    log.error(f'BitfinexAPI "{self.delta}" Error', exc_info=True)
                finally:
                    session.close()

                session = self.Session()
                try:
                    binance = Binance(self.delta, self.interval[self.delta])
                    binance.chunk(session, conn)
                except Exception:
                    session.rollback()
                    log.error(f'BinanceAPI "{self.delta}" Error', exc_info=True)
                finally:
                    session.close()

                log.info(f'"{self.delta}" {msg} update completed')

            session = self.Session()
            try:
                monitor.check(session)
            except Exception:
                session.rollback()
                log.error(f'Oh "{self.delta}" monitor rollback', exc_info=True)
            finally:
                session.close()
                # log.info(f'"{self.delta}" Monitor complete')

            if showCoins:
                log.info(f'{monitor}')

            # set the tickTock ...
            time.sleep(self.interval[self.delta])
