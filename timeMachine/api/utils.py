"""
Provides utility functions used across more than one module or sub module.

"""

# Import Built-Ins
import logging
import json
import sys, time
import smtplib

# Import Third-Party
import requests
from requests import Session
import pandas as pd
import matplotlib.pyplot as plt

# Init Logging Facilities
log = logging.getLogger(__name__)


# get request response from exchange api
class Return_API_response:
	"""Get data from BitFinex API. Bitfinex rate limit policy can vary in a
	 range of 10 to 90 requests per minute. So if we get a 429 response wait
	 for a minute"""
	def __init__(self):
		self.sesh = requests.Session()

	def api_response(self, url):
		try:
			res = self.sesh.get(url)
			while res.status_code == 429:
				log.info(f'{res.status_code} {url[42:]}')
				# wait for Bitfinex
				time.sleep(62)
				res = self.sesh.get(url)

			data = res.json()
			res.raise_for_status()
		except requests.exceptions.HTTPError:
			log.error("Requsts error ", exc_info=True)
			# Do something here to fix error
			return False
		return data

	def close_session(self):
		self.sesh.close()


class Email:
	"""Send Email to users"""
	def __init__(self, coin, msg):
		self.coin = coin
		self.msg = msg

	def _findUser(self, coin):
		"""Find all users who hold this coin"""
		pass

	def sendEmail(self, email='twguy66@gmail.com'):
		"""Send user email"""
		body = f'Subject: Moving average Alert, \n {self.coin} says {self.msg}'
		smtpObj = smtplib.SMTP('smtp.stackmail.com', 587)
		smtpObj.ehlo()
		smtpObj.starttls()
		smtpObj.login('mail@TWGuy.co.uk', 'Sporty66')
		sendmailStatus = smtpObj.sendmail('mail@TWGuy.co.uk', email, body)
		if sendmailStatus != {}:
			log.error('There was a problem sending email to %s: %s' %
					  (email, sendmailStatus), exc_info=True)

		smtpObj.quit()
		log.info(f'{self.coin} sends signal {self.msg}. Email sent to {email}')
		
													   


class Queue:
	"""Queue class"""
	def __init__(self):
		self.items = []

	def isEmpty(self):
		return self.items == []

	def enqueue(self, item):
		self.items.insert(0, item)

	def dequeue(self):
		return self.items.pop()

	def size(self):
		return len(self.items)


def plotDataset(dataset, record, title):
	fig = plt.figure(figsize=(16, 8))
	axes = fig.add_axes([0, 0, 1, 1])
	# plot dataset
	axes.plot(dataset.index, dataset['sewma'],
			  label='ewma={}'.format(10), color='blue')
	axes.plot(dataset.index, dataset['bewma'],
			  label='ewma={}'.format(27), color='red')
	axes.plot(dataset.index, dataset['Close'],
			  label='close', color='green', alpha=.5)
	axes.plot(dataset.index, dataset['longewma'],
			  label='longma', color='orange', alpha=.5)
	axes.plot(dataset.index, dataset['High'],
			  label='high', color='pink', alpha=.5)

	# plot the crossover points
	sold = pd.DataFrame(record[record['Transaction'] == 'Sell']['Close'])
	axes.scatter(sold.index, sold['Close'], color='r', label='Sell', lw=3)
	bought = pd.DataFrame(record[record['Transaction'] == 'Buy']['Close'])
	axes.scatter(bought.index, bought['Close'], color='g', label='Sell', lw=3)

	axes.set_ylabel('closing price')
	axes.set_xlabel('Date')
	axes.grid(color='b', alpha=0.5, linestyle='--', linewidth=0.5)
	axes.grid(True)
	axes.set_title(title)
	# axes.set_xticks()
	plt.legend()
	plt.show()
