"""
Two Data structures used to translate the Database and update the State of the
altcoins. The dictionaries of DB_Tables and altcoins use the same keys, as do
the pandas DF_Tables which are generated from DB after every iteration.
"""

import logging

# third party imports


# from Time Machine
from .utils import DF_Tables
from ..database.models import delta_tables
from .coin import Coin

log = logging.getLogger(__name__)


class Altcoin(dict):
    """A collection of Coins"""
    def __repr__(self):
        li = ''
        for key in self.keys():
            li = li + self[key] + '\n'
        return li


class Monitor():
    """This class is instantiated once for each thread. Monitoring each altcoin's
    DataFrame, upon a moving average cross signal sends out user emails. Updating
    each 'Coin' in dbTables with timestamp, trend and latest price"""

    altcoin = Altcoin()

    def __init__(self, Session, delta):
        self.db_tables = delta_tables(delta)
        session = Session()
        for key, dataf in DF_Tables.get_DFTables(session, self.db_tables).items():
            cross = DF_Tables.crossover(dataf)  # need to allow for the 'bma' difference '''dataf[bma:]'''
            self.altcoin[key] = Coin(self.db_tables[key].name, dataf, cross)
            log.info(f'Initialize: {self.altcoin[key]}')
        session.close()

    def __repr__(self):
        li = '\n'
        for value in self.altcoin.values():
            li = li + repr(value) + '\n'
        return li

    def check(self, session):
        """ for each DB table generate dataframe, check for signal then update coin """
        tables = DF_Tables.get_DFTables(session, self.db_tables)

        try:
            for i, dataf in tables.items():
                cross = DF_Tables.crossover(dataf[55:])
                coin = self.altcoin[i]
                coin.update(dataf, cross)

        except Exception:
            log.error(f"Monitor Error with coin {coin.name}:- ", exc_info=True)
            raise
