import datetime


class Coin:
    """Altcoin class representing any altcoin"""
    def __init__(self, name):
        self.altcoin = name
        self.currentPrice = None
        self.currentTrend = None
        self.previousSignal = datetime.datetime.now()

    def nextSignal(self, tstamp):
        """Is the latest MA signal more recent than the last ?"""
        if tstamp > self.previousSignal:
            self.previousSignal = tstamp
            return True
        return False

    def setPrice(self, price):
        """Set with latest price """
        self.currentPrice = price
        print(f'{self.altcoin} = ${self.currentPrice}')

    def price(self):
        """Return latest price"""
        return self.currentPrice

    def setTrend(self, trend):
        """set current trend i.e Sell or Buy"""
        self.currentTrend = trend

    def trend(self):
        """Return current trend"""
        return self.trend

    def name(self):
        """Return coin name"""
        return self.altcoin
    

