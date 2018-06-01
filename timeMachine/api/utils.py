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
				log.info(f'{res.status_code} {res.url[38:]}')
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
	def __init__(self, coinName, transaction):
		self.name = coinName
		self.msg = transaction

	def _findUser(self, coin):
		"""Find all users who hold this coin"""
		pass

	@staticmethod
	def sendEmail(name, msg, to_addr='twguy66@gmail.com'):
		"""Send user email"""
		header = 'From: room4rent@buriramvillas.com\n'
		header += f'To: {to_addr}\n'
		header += 'Subject: MA-Alert\n'
		message = header + f'Moving average:- {name} advises {msg} indicator...'
		
		smtpObj = smtplib.SMTP('smtp.stackmail.com', 587)
		smtpObj.ehlo()
		smtpObj.starttls()
		smtpObj.login('room4rent@buriramvillas.com', 'Sporty66')
		sendmailStatus = smtpObj.sendmail('room4rent@buriramvillas.com', to_addr, message)
		if sendmailStatus != {}:
			log.error('There was a problem sending email to %s: %s' %
					(to_addr, sendmailStatus), exc_info=True)
		smtpObj.quit()
		
													   
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
