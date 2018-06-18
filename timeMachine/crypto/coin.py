import datetime
import logging


log = logging.getLogger(__name__)


class Coin:
	"""Altcoin class representing any altcoin"""
	def __init__(self, name):
		self.altcoin = name
		self.currentPrice = None
		self.currentTrend = None
		self.previousSignal = datetime.datetime.utcnow()

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
	