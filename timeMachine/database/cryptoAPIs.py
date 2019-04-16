from datetime import datetime
import logging
# import pytz

# third party imports
import pandas as pd
from sqlalchemy import func

# from TimeMachine
from ..crypto.utils import Return_API_response, Error_429
from ..database.models import Bitfinex_Tables, CryptoCompare_Tables, Binance_Tables

log = logging.getLogger(__name__)


class CryptoAPI:
    """chunk_update will bring the DB up to date from exchange API relative to the last DB entry"""

    def __init__(self, delta, maxLimit, interval):
        self.delta = delta
        self.maxLimit = maxLimit
        self.interval = interval

    def _numRecords(self, key, table, session):
        # find time of last entry
        query = session.query(table.MTS).filter(
            table.MTS == session.query(func.max(table.MTS))).all()
        if query == []:  # Check for empty db-table
            limit = self.maxLimit
        else:
            # How many 'intervals' since last entry
            limit = int((datetime.utcnow() - query[0][0]).total_seconds() // self.interval)
        if limit > self.maxLimit:
            log.error(f'DB chunk missing data:= {key} limit={limit} delta = {self.delta} this has not been updated')
            # limit = 0 we need to change delta to update this database table
            limit = -1
        return limit

    def updateDB(self, df, table, conn):
        df.to_sql(con=conn, name=table.__tablename__, index=True, chunksize=100, if_exists='append')


class Bitfinex(CryptoAPI):
    """ Bitfinex API get lastest data chunk"""

    endpoint = 'https://api.bitfinex.com/v2/candles/trade:'
    maxLimit = 1000

    def __init__(self, delta, interval):
        super().__init__(delta, self.maxLimit, interval)
        self.DB_Tables = Bitfinex_Tables[delta]

    def chunk(self, session, conn):
        resp = Return_API_response()
        for key, table in self.DB_Tables.items():
            limit = self._numRecords(key, table, session)
            if limit > 0:
                sym = key.upper() + 'USD'
                try:
                    data = resp.api_response(self.endpoint + f'{self.delta}:t{sym}/hist?limit={limit}')[::-1]
                    df = pd.DataFrame(data, columns=['MTS', 'Open', 'Close', 'High', 'Low', 'Volume'])
                    df['MTS'] = pd.to_datetime(df['MTS'], unit='ms')
                    df.set_index('MTS', drop=True, inplace=True)
                    self.updateDB(df, table, conn)
                except Error_429 as err:
                    log.info(f'Bitfinex {key} 429 error {err}')
                except Exception as err:
                    log.error(f'BitfinexAPI {key} {err.__class__.__name__}')
        resp.close_session()


class Compare(CryptoAPI):
    """ CryptoCompare API """

    APIkey = '484cb8d70ed62517ecfec5b4666fb83c8e62944a4b460222d72becd39d6e4412'
    endpoint_minute = 'https://min-api.cryptocompare.com/data/histominute?'
    endpoint_hour = 'https://min-api.cryptocompare.com/data/histohour?'
    maxLimit = 2000

    def __init__(self, delta, interval):
        self.maxLimit = int(self.maxLimit / int(delta[:-1]))
        self.endpoint = self.endpoint_minute if delta[-1] == 'm' else self.endpoint_hour
        super().__init__(delta, self.maxLimit, interval)
        self.DB_Tables = CryptoCompare_Tables[delta]

    def chunk(self, session, conn):
        resp = Return_API_response()
        for key, table in self.DB_Tables.items():
            limit = self._numRecords(key, table, session)
            if limit > 0:
                try:
                    sym = key.upper()
                    data = resp.api_response(
                        self.endpoint + f"fsym={sym}&tsym=USD&limit={limit}&aggregate={self.delta[:-1]} \
                                          &e=CCCAGG&api_key={self.APIkey}")
                    if data['Type'] >= 100:
                        DF = pd.DataFrame(data['Data'][1:])
                        DF['MTS'] = pd.to_datetime(DF['time'], unit='s')
                        DF['Volume'] = DF['volumefrom'] + DF['volumeto']
                        DF.drop(['time', 'volumefrom', 'volumeto'], inplace=True, axis=1)
                        DF.set_index('MTS', drop=True, inplace=True)
                        DF.rename(columns={'close': 'Close', 'open': 'Open', 'low': 'Low', 'high': 'High'},
                                  inplace=True)
                        DF = DF[['Open', 'Close', 'High', 'Low', 'Volume']]
                        self.updateDB(DF, table, conn)
                    else:
                        if data['Type'] == 99:
                            log.info(f"CompareChunk {sym} {data['Message']}")
                except Exception as err:
                    log.error(f'CompareAPI - {key} {err.args}', exec_info=True)
        resp.close_session()


class Binance(CryptoAPI):
    """ Bitfinex API get lastest data chunk"""

    endpoint = 'https://api.binance.com/api/v1/klines'
    maxLimit = 1000

    def __init__(self, delta, interval):
        super().__init__(delta, self.maxLimit, interval)
        self.DB_Tables = Binance_Tables[delta]

    def chunk(self, session, conn):
        resp = Return_API_response()
        for key, table in self.DB_Tables.items():
            limit = self._numRecords(key, table, session)
            if limit > 0:
                sym = key.upper() + 'USDT'
                try:
                    data = resp.api_response(self.endpoint + f'?symbol={sym}&interval={self.delta}&limit={limit}')
                    df = pd.DataFrame(data, columns=['MTS', 'Open', 'High', 'Low', 'Close', 'Volume',
                                                     'MTS_close', 'a', 'b', 'c', 'd', 'e'])
                    df.drop(['MTS_close', 'a', 'b', 'c', 'd', 'e'], inplace=True, axis=1)
                    df['MTS'] = pd.to_datetime(df['MTS'], unit='ms')
                    df.set_index('MTS', drop=True, inplace=True)
                    df = df[['Open', 'Close', 'High', 'Low', 'Volume']]
                    self.updateDB(df, table, conn)
                except Error_429 as err:
                    log.info(f'Binance {key} 429 error {err.args}')
                except Exception as err:
                    log.error(f'BinanceAPI {key} {err.args}')
        resp.close_session()
