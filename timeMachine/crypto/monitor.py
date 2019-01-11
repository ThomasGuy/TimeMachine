"""
Two Data structures used to translate the Database and update the State of the
altcoins. The dictionaries of DB_Tables and altcoins use the same keys, as do
the pandas DF_Tables which are generated from DB after every iteration.
"""

import logging

# third party imports


# from Time Machine
from .altcoin import Altcoin
from .utils import Email, DF_Tables
from ..database.models import delta_tables

log = logging.getLogger(__name__)


class Monitor(Altcoin):
    """This class is instantiated once for each thread. Monitoring each altcoin's
    DataFrame, upon a moving average cross signal sends out user emails. Updating
    each 'Coin' in dbTables with timestamp, trend and latest price"""
    def __init__(self, Session, delta):
        self.dbTables = delta_tables(delta)
        super().initCoin(Session, self.dbTables)

    def __repr__(self):
        return super().__repr__()

    def check(self, session):
        """ for each DB table generate dataframe, check for signal then update coin """
        tables = DF_Tables.get_DFTables(session, self.dbTables)

        try:
            for i, dataf in tables.items():
                cross = DF_Tables.crossover(dataf[55:])
                coin = self.altcoins[i]
                coin.update(dataf, cross)

        except Exception:
            log.error(f"Monitor Error with coin {coin.name}:- ", exc_info=True)
            raise
