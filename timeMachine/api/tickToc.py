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

log = logging.getLogger(__name__)

endpoint = 'https://api.bitfinex.com/v2/candles/trade:'
sleep = {
	'5m' : 280,
	'15m': 880,
	'30m': 1770,
}


def tickToc(coins, delta, Session, interval):
	"""Running in it's own thread this adds a new row to the DB tables"""

	while True:
		# set the tickTock ...
		time.sleep(sleep[delta])
		session = Session()
		try:
			Chunk_update().chunk(session, delta, endpoint, interval)
		except:
			session.rollback()
			log.error("TickToc Error", exc_info=True)
		finally:
			session.close()
			log.info('TickToc complete')
