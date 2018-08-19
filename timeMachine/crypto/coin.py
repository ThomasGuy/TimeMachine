import datetime
import logging
import pandas as pd
import matplotlib.pyplot as plt


log = logging.getLogger(__name__)


class Coin:
    """Cryptocoin class representing any of many altcoins"""
    def __init__(self, name):
        self.name = name
        self.price = 0.0
        self.trend = None
        self.previousSignal = datetime.datetime.utcnow()
        self.dframe = pd.DataFrame()
        self.crossRecord = pd.DataFrame()

    def __repr__(self):
        return '<Coin> {:>27} price=${: 10.4f} is on a "{:4s}" trend since {}'. \
            format(self.name, self.price, self.trend, self.previousSignal)

    def nextSignal(self, tstamp):
        """Is the latest MA signal more recent than the last ?"""
        if tstamp > self.previousSignal:
            self.previousSignal = tstamp
            return True
        return False
    
    def plotData(self, title):
        """plot self.dframe with self.crossRecord these are dataframes representing
        the data and the crossover indicators"""
        fig = plt.figure(figsize=(16, 8))
        axes = fig.add_axes([0, 0, 1, 1])
        # plot dframe
        axes.plot(self.dframe.index, self.dframe['sewma'],
                  label='ewma={}'.format(10), color='blue')
        axes.plot(self.dframe.index, self.dframe['bewma'],
                  label='ewma={}'.format(27), color='red')
        axes.plot(self.dframe.index, self.dframe['Close'],
                  label='close', color='green', alpha=.5)
        axes.plot(self.dframe.index, self.dframe['longewma'],
                  label=f'longma={74}', color='orange', alpha=.5)
        axes.plot(self.dframe.index, self.dframe['High'],
                  label='high', color='pink', alpha=.5)

        # plot the crossover points
        sold = pd.DataFrame(self.crossRecord[self.crossRecord['Transaction'] == 'Sell']['Close'])
        axes.scatter(sold.index, sold['Close'], color='r', label='Sell', lw=3)
        bought = pd.DataFrame(self.crossRecord[self.crossRecord['Transaction'] == 'Buy']['Close'])
        axes.scatter(bought.index, bought['Close'], color='g', label='Sell', lw=3)

        axes.set_ylabel('closing price')
        axes.set_xlabel('Date')
        axes.grid(color='b', alpha=0.5, linestyle='--', linewidth=0.5)
        axes.grid(True)
        axes.set_title(title)
        # axes.set_xticks()
        plt.legend()
        plt.show()
