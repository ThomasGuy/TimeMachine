import logging, time
import threading
from sqlalchemy.orm import sessionmaker

log = logging.getLogger(__name__)

# initialize globals
delta = '15m'
db_name = f'sqlite:///c:\\data\\sqlite\\db\\tickToc{delta}.db'

'''
coins = ['BTCUSD', 'ETHUSD', 'EOSUSD', 'IOTUSD', 'LTCUSD', 'NEOUSD', 'OMGUSD',
		'TRXUSD', 'XRPUSD', 'ZECUSD', 'BCHUSD', 'BTGUSD', 'DSHUSD',
		'ETCUSD', 'GNTUSD', 'QTMUSD', 'SANUSD', 'XLMUSD', 'XMRUSD', 
		'RLCUSD', 'FUNUSD', 'QSHUSD', 'AVTUSD', 'SPKUSD', 'RCNUSD']

compareAPI = ['ADA','XVG','XEM','VEN','BNB','BCN','ICX',
			'LSK','ZIL','ONT','AE','ZRX','DCR','NANO', 'WAVES']
'''

interval = {'5m': 300, '15m': 900, '30m': 1800, '1h': 3600}


# From TimeMachine, initialize the DB
from .database.db_init import engine

# Intialize Session class for whole application
Session = sessionmaker(bind=engine)

# From TimeMachine
from .database.db_chunk_update import Chunk_update
from .tickToc import tickToc
from .monitor import monitor


def start():
	# update the db to present time
	# session = Session()
	# try:
	# 	Chunk_update().chunk(session, delta,  bitfinexURL, interval)
	# except:
	# 	session.rollback()
	# 	log.error("Chunky Error", exc_info=True)
	# finally:
	# 	session.close()
	# 	log.info('Chunks updated')

	# Start tickToc
	watcher = threading.Thread(target=tickToc, args=[delta, interval, Session])
	watcher.start()
	log.info(f"TickToc started {watcher.getName()}")

	# wait then start Monitor
	time.sleep(30)
	looking = threading.Thread(target=monitor, args=[delta, interval, Session])
	looking.start()
	log.info(f"Monitor started {looking.getName()}")
