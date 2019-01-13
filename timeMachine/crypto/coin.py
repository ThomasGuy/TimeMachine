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
    def __init__(self, name, dataf, cross):
        self.name = name
        self._df = dataf
        self.price = self._df['Close'].iloc[-1]
        self._cross = cross
        self.trend = self._cross['Transaction'].iloc[-1]
        self._previousSignal = self._cross.index[-1]
        self._value_lock = threading.Lock()

    def __repr__(self):
        return '<Coin> {:>32} price=${: 10.4f} is on a "{:4s}" trend since {}'. \
            format(self.name, self.price, self.trend, self._previousSignal)

    def nextSignal(self, tstamp):
        """Is the latest MA signal more recent than the last ?"""
        if tstamp > self._previousSignal:
            self._previousSignal = tstamp
            return True
        return False

    def update(self, dataf, cross):
        with self._value_lock:
            self._df = dataf
            self._cross = cross
            self.price = dataf['Close'].iloc[-1]
            transaction = cross['Transaction'].iloc[-1]
            if not self.trend == transaction and self.nextSignal(cross.index.max()):
                self.trend = transaction
                log.info(f'Transaction update: {self}\n')
                Email.sendEmail(self.name, transaction)
