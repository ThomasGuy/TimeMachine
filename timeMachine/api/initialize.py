import logging, time
import threading
from sqlalchemy.orm import sessionmaker

log = logging.getLogger(__name__)

# initialize globals
delta = '30m'
db_name = f'sqlite:///c:\\data\\sqlite\\db\\tickToc{delta}.db'
endpoint = 'https://api.bitfinex.com/v2/candles/trade:'
coins = ['BTCUSD', 'ETHUSD', 'EOSUSD', 'IOTUSD', 'LTCUSD', 'NEOUSD', 'OMGUSD',
		'TRXUSD', 'XRPUSD', 'ZECUSD', 'BCHUSD', 'BTGUSD', 'DSHUSD',
		'ETCUSD', 'GNTUSD', 'QTMUSD', 'SANUSD', 'XLMUSD', 'XMRUSD', 
		'RLCUSD', 'FUNUSD', 'QSHUSD', 'AVTUSD', 'SPKUSD', 'RCNUSD']
interval = {'5m': 300, '15m': 900, '30m': 1800}


# From TimeMachine
from .database.db_init import engine

# Intialize Session class for whole application
Session = sessionmaker(bind=engine)

# From TimeMachine
from .database.db_chunk_update import Chunk_update
from .tickToc import tickToc
from .monitor import monitor


def start():
	# update the db to present time
	session = Session()
	try:
		Chunk_update().chunk(session, delta, endpoint, interval)
	except:
		session.rollback()
		log.error("Chunky Error", exc_info=True)
	finally:
		session.close()

	# Start tickToc
	watcher = threading.Thread(target=tickToc, args=[coins, delta, Session])
	watcher.start()

	# wait then start Monitor
	time.sleep(30)
	looking = threading.Thread(target=monitor, args=[delta, interval, Session])
	looking.start()
