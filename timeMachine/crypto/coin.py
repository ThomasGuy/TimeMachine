import datetime
import logging
import pandas as pd
import matplotlib.pyplot as plt


log = logging.getLogger(__name__)


class Coin:
    """Altcoin class representing any of many altcoins"""
    def __init__(self, name):
        self.altcoin = name
        self.currentPrice = None
        self.currentTrend = None
        self.previousSignal = datetime.datetime.utcnow()
        self.df = pd.DataFrame()
        self.record = pd.DataFrame()

    def nextSignal(self, tstamp):
        """Is the latest MA signal more recent than the last ?"""
        if tstamp > self.previousSignal:
            self.previousSignal = tstamp
            return True
        return False

    def setPrice(self, price):
        """Set with latest price """
        self.currentPrice = price

    def price(self):
        """Return latest price"""
        return self.currentPrice

    def setTrend(self, trend):
        """set current trend i.e Sell or Buy"""
        self.currentTrend = trend
        log.info(f"{self.altcoin} is on '{self.currentTrend}' trend at {self.previousSignal}")

    def trend(self):
        """Return current trend"""
        return self.currentTrend

    def name(self):
        """Return coin name"""
        return self.altcoin
    

    def plotData(self, title):
        """plot self.df with self.record these are dataframes representing
        the data and the crossover indicators"""
        fig = plt.figure(figsize=(16, 8))
        axes = fig.add_axes([0, 0, 1, 1])
        # plot df
        axes.plot(self.df.index, self.df['sewma'],
                label='ewma={}'.format(10), color='blue')
        axes.plot(self.df.index, self.df['bewma'],
                label='ewma={}'.format(27), color='red')
        axes.plot(self.df.index, self.df['Close'],
                label='close', color='green', alpha=.5)
        axes.plot(self.df.index, self.df['longewma'],
                label=f'longma={74}', color='orange', alpha=.5)
        axes.plot(self.df.index, self.df['High'],
                label='high', color='pink', alpha=.5)

        # plot the crossover points
        sold = pd.DataFrame(self.record[self.record['Transaction'] == 'Sell']['Close'])
        axes.scatter(sold.index, sold['Close'], color='r', label='Sell', lw=3)
        bought = pd.DataFrame(self.record[self.record['Transaction'] == 'Buy']['Close'])
        axes.scatter(bought.index, bought['Close'], color='g', label='Sell', lw=3)

        axes.set_ylabel('closing price')
        axes.set_xlabel('Date')
        axes.grid(color='b', alpha=0.5, linestyle='--', linewidth=0.5)
        axes.grid(True)
        axes.set_title(title)
        # axes.set_xticks()
        plt.legend()
        plt.show()
