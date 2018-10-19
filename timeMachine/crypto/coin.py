import datetime
import logging
import pandas as pd
import matplotlib.pyplot as plt


log = logging.getLogger(__name__)


class Coin:
    """Cryptocoin class representing one of many altcoins"""
    def __init__(self, name):
        self.name = name
        self.price = 0.0
        self.trend = None
        self.previousSignal = datetime.datetime.utcnow()
        self.dframe = pd.DataFrame()
        self.crossRecord = pd.DataFrame()

    def __repr__(self):
        return '<Coin> {:>32} price=${: 10.4f} is on a "{:4s}" trend since {}'. \
            format(self.name, self.price, self.trend, self.previousSignal)

    def nextSignal(self, tstamp):
        """Is the latest MA signal more recent than the last ?"""
        if tstamp > self.previousSignal:
            self.previousSignal = tstamp
            return True
        return False
