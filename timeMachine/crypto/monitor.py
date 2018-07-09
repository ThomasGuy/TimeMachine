"""
Two Data structures used to translate the Database and keep the State of the 
altcoins. The two dictionaries DB_Tables and altcoins use the same keys, as 
well as pandas DF_Tables which is generated from DB after every iteration.
"""

import sys, time
from datetime  import datetime
# third party imports
import pandas as pd
import logging

# from Time Machine
from .altcoin import Altcoin
from .utils import Email, DF_Tables

log = logging.getLogger(__name__)


class Monitor(Altcoin):
    """This class is instantiated once for each thread. Monitoring each altcoin's
    DataFrame, upon a moving average signal sending out user emails. Updating 
    each 'Coin' in Altcoin with timestamp, trend and latest price"""
    def __init__(self, dbTables):
        self.dbTables = dbTables
        

    def check(self, session):
        """ for each DB table generate dataframe, check for signal then update coin """
        tables = DF_Tables.get_DFTables(session, self.dbTables)

        try:
            for i, dataf in tables.items():
                coin = self.altcoins[i]
                cross = DF_Tables.crossover(dataf)
                coin.df = dataf
                coin.crossRecord = cross
                coin.setPrice(dataf['Close'].iloc[-1])
                transaction = cross['Transaction'].iloc[-1]
                if not coin.trend() == transaction and coin.nextSignal(cross.index.max()):
                    coin.setTrend(transaction)
                    Email.sendEmail(coin.name(), transaction)

        except Exception:
            log.error(f"Monitor Error with coin ", exc_info=True)
            raise


    def initCoin(self, Session):
        """ Set intial 'trend' Buy or Sell for each coin in dbTables"""
        session = Session()
        
        try:
            # for each DB table generate dataframe check for signal then update coin
            tables = DF_Tables.get_DFTables(session, self.dbTables)
            for i, df in tables.items():
                coin = self.altcoins[i]
                cross = DF_Tables.crossover(df)
                coin.setTrend(cross['Transaction'].iloc[-1])
        except IndexError:
            log.error(
                f'Init Altcoins IndexError for {coin.name()}', exc_info=True)
        finally:
            session.close()
