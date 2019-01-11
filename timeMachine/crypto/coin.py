import datetime
import logging
import threading

# 3rd party imports
import pandas as pd
import matplotlib.pyplot as plt

# package imports
from .utils import Email
log = logging.getLogger(__name__)


class Coin:
    """Cryptocoin class representing one of many altcoins"""
    def __init__(self, name):
        self.name = name
        self.price = 0.0
        self.trend = 'n/a'
        self.previousSignal = datetime.datetime.utcnow()
        self.dframe = pd.DataFrame()
        self.crossRecord = pd.DataFrame()
        self._value_lock = threading.Lock()

    def __repr__(self):
        return '<Coin> {:>32} price=${: 10.4f} is on a "{:4s}" trend since {}'. \
            format(self.name, self.price, self.trend, self.previousSignal)

    def nextSignal(self, tstamp):
        """Is the latest MA signal more recent than the last ?"""
        if tstamp > self.previousSignal:
            self.previousSignal = tstamp
            return True
        return False

    def update(self, dataf, cross):
        with self._value_lock:
            self.dframe = dataf
            self.crossRecord = cross
            self.price = dataf['Close'].iloc[-1]
            transaction = cross['Transaction'].iloc[-1]
            if not self.trend == transaction and self.nextSignal(cross.index.max()):
                self.trend = transaction
                log.info(f'Transaction update: {self}')
                Email.sendEmail(self.name, transaction)
