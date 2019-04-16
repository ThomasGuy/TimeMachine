from datetime import datetime
import logging
# import pytz

# third party imports
import pandas as pd
from sqlalchemy import func

# package imports
from timeMachine.crypto.utils import Return_API_response
from timeMachine.database.models import CryptoCompare_Tables
from timeMachine.config import Config

log = logging.getLogger(__name__)


class DataError(Exception):
    pass


class CompareAPI:
    period = {
        'm': 'histominute',
        'h': 'histohour',
        'D': 'histoday'
    }

    def __init__(self, delta):
        self.delta = delta
        self._tables = CryptoCompare_Tables[delta]

    def updateDB(self, df, table, conn):
        df.to_sql(con=conn, name=table.__tablename__, index=True, chunksize=100, if_exists='append')

    def chunk(self, session, conn):
        endpoint = f'https://min-api.cryptocompare.com/data/{self.period[self.delta[-1]]}?'
        to_date = int(datetime.now().timestamp())
        resp = Return_API_response()
        for key, table in self._tables.items():
            query = session.query(table.MTS)
            query = query.filter(table.MTS == session.query(func.max(table.MTS))).first()
            from_date = int(query[0].timestamp())
            sym = key.upper()
            holder = []
            date = to_date

            try:
                while date > from_date:
                    if self.delta[-1] == 'm' and (to_date - from_date > (7 * 24 * 3600 - 3600)):
                        endpoint = 'https://min-api.cryptocompare.com/data/histohour?'
                        ipdata = resp.api_response(
                            endpoint + f"fsym={sym}&tsym=USD&limit=2000&toTs={date} \
                                        &aggregate=1&e=CCCAGG&api_key={Config.APIKEY}")
                    else:
                        ipdata = resp.api_response(
                            endpoint + f"fsym={sym}&tsym=USD&limit=2000&toTs={date} \
                                        &aggregate={self.delta[:-1]}&e=CCCAGG&api_key={Config.APIKEY}")
                    if ipdata['Type'] == 100:
                        # raise DataError(f"CompareChunk {sym} {ipdata['Type']} {ipdata['Message']}")
                        holder.append(pd.DataFrame(ipdata['Data']))
                        date = ipdata['TimeFrom']
                    else:
                        raise DataError(f"CompareChunk {sym} {ipdata['Type']} {ipdata['Message']}")
            except DataError as e:
                log.info(e)
            except Exception as e:
                log.error(f'CompareAPI - {key} {e}', exc_info=True)
            else:
                DF = pd.concat(holder, axis=0)
                DF = DF[DF['time'] > from_date]
                DF['MTS'] = pd.to_datetime(DF['time'], unit='s')
                DF['Volume'] = DF['volumefrom'] + DF['volumeto']
                DF.drop(['time', 'volumefrom', 'volumeto'], inplace=True, axis=1)
                DF.set_index('MTS', drop=True, inplace=True)
                DF.rename(columns={'close': 'Close', 'open': 'Open', 'low': 'Low', 'high': 'High'},
                        inplace=True)
                DF = DF[['Open', 'Close', 'High', 'Low', 'Volume']]
                DF.sort_index(ascending=True, inplace=True)
                self.updateDB(DF, table, conn)

        resp.close_session()
