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

log = logging.getLogger(__name__)


class Monitor(Altcoin):
    """This class is instantiated once for each thread. Monitoring each altcoin's
    DataFrame, upon a moving average cross signal send out user emails. Updating 
    each 'Coin' in dbTables with timestamp, trend and latest price"""
    def __init__(self, Session, dbTables):
        super().initCoin(Session, dbTables)
        self.dbTables = dbTables

        
    def __repr__(self):
        return super().__repr__()
        

    def check(self, session):
        """ for each DB table generate dataframe, check for signal then update coin """
        tables = DF_Tables.get_DFTables(session, self.dbTables)

        try:
            for i, dataf in tables.items():
                coin = self.altcoins[i]
                cross = DF_Tables.crossover(dataf)
                coin.df = dataf
                coin.crossRecord = cross
                coin.price = dataf['Close'].iloc[-1]
                transaction = cross['Transaction'].iloc[-1]
                if not coin.trend == transaction and coin.nextSignal(cross.index.max()):
                    coin.trend = transaction
                    log.info(f'Transaction update: {coin}')
                    Email.sendEmail(coin.name, transaction)

        except Exception:
            log.error(f"Monitor Error with coin {coin.name}:- ", exc_info=True)
            raise



