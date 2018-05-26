import sys, logging
import time
import threading
from datetime import datetime

# Import Third-Party
import requests

# From TimeMachine
from .utils import Return_API_response, Queue
from .database.db_init import DB_Tables

log = logging.getLogger(__name__)

endpoint = 'https://api.bitfinex.com/v2/candles/trade:'
response_Q = Queue()
sleep = {
	'5m' : 280,
	'15m': 880
}


def tickToc(coins, delta, Session):
    """Running in it's own thread this adds a new row to the DB tables"""

    while True:
        # set the tickTock ...
        time.sleep(sleep[delta])
        session = Session()
        resp = Return_API_response()
        try:
            for coin in coins:
                sym = coin[:3]
                url = endpoint + f'{delta}:t{coin}/last'
                row = resp.api_response(url)
                # Insert row in dataBase Table, with DateTime object index
                if row:
                    insertRow(row, sym, session)
                else:
                    print('Get row error')
                    sys.exit(1)
            # session.close()
        except:
            session.rollback()
            log.error("TickToc Error", exc_info=True)
        finally:
            session.close()
            resp.close_session()
            print('TickToc')


def insertRow(row, coin, session):
    """Insert a new row"""
    coin = coin.lower()
    update = DB_Tables[coin](MTS=datetime.fromtimestamp(row[0]/1000),
                             Open=row[1],
                             Close=row[2],
                             High=row[3],
                             Low=row[4],
                             Volume=row[5])
    session.add(update)
    session.commit()
