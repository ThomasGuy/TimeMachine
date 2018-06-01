import sys, logging
import time
import threading
from datetime import datetime

# Import Third-Party
import requests

# From TimeMachine
from .utils import Return_API_response
from .database.db_init import DB_Tables
from .database.db_chunk_update import Chunk_update
from .database.compareAPI_chunk import Chunk_CompareAPI

log = logging.getLogger(__name__)

bitfinexURL = 'https://api.bitfinex.com/v2/candles/trade:'
compareURL = 'https://min-api.cryptocompare.com/data/histominute?'
sleep = {
	'5m' : 280,
	'15m': 880,
	'30m': 1770,
	'1h' : 3570
}


def tickToc(delta, interval, Session):
	"""Running in it's own thread this adds a new row to the DB tables"""

	while True:
		session = Session()
		try:
			Chunk_CompareAPI().chunk(session, delta, compareURL, interval)
		except:
			session.rollback()
			log.error("Chunk_Compare Error", exc_info=True)
		finally:
			session.close()
			log.info('Chunk_Compare complete')

		session = Session()
		try:
			Chunk_update().chunk(session, delta, bitfinexURL, interval)
		except:
			session.rollback()
			log.error("Chunk_update Error", exc_info=True)
		finally:
			session.close()
			log.info('Chunk_update, Ticktoc complete')

		# set the tickTock ...
		time.sleep(sleep[delta])