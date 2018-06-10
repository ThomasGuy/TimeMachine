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
from .database.db_init import all_DB_tables
from .utils import Email, DF_Tables
from .coin import Coin

log = logging.getLogger(__name__)


def monitor(delta, interval, altcoins):
    """Running in it's own thread monitor continually updates the Altcoins and
    checks for any signals from the Moving Averages"""
    
    while True:
        #session = Session()
        try:
            Monitor.check(altcoins)
        except:
            #session.rollback()
            log.error('Oh deBugger', exc_info=True)
        finally:
            #session.close()
            log.info('Monitor complete')        

        # set the sleep interval ...
        time.sleep(interval[delta])


class Monitor:
    """This class is instantiated every interval. Monitoring each altcoin's
    DataFrame, upon a moving average signal sending out user emails. Updating 
    each 'altcoin' instance with timestamp, trend and latest price"""
    #def __init__(self, dbTables):
        #self.session = session
        
    @classmethod
    def check(self, altcoins):
        tables = DF_Tables.get_DFTables(all_DB_tables())
        # for each DB table generate dataframe check for signal then update coin
        try:
            for i, df in tables.items():
                coin = altcoins[i]
                cross = DF_Tables.crossover(df)
                coin.setPrice(df['Close'].iloc[-1])
                transaction = cross['Transaction'].iloc[-1]
                if not coin.trend() == transaction and coin.nextSignal(cross.index.max()):
                    coin.setTrend(transaction)
                    Email.sendEmail(coin.name(), transaction)

        except Exception:
            log.error(f"Error with coin {coin.name()}", exc_info=True)
