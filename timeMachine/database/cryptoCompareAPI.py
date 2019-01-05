from datetime import datetime
import logging
import pytz

# third party imports
import pandas as pd
from sqlalchemy import func

# package imports
from timeMachine.crypto.utils import Return_API_response
from timeMachine.database.models import CryptoCompare_Tables

log = logging.getLogger(__name__)


class CompareAPI:

    APIkey = '484cb8d70ed62517ecfec5b4666fb83c8e62944a4b460222d72becd39d6e4412'
    period = {
        'm': 'histominute',
        'h': 'histohour',
        'D': 'histoday'
    }

    def __init__(self, delta, interval):
        self.delta = delta
        self.interval = interval
        self.endpoint = f'https://min-api.cryptocompare.com/data/{self.period[self.delta[-1]]}?'
        self.DB_Tables = CryptoCompare_Tables[delta]

    def updateDB(self, df, table, conn):
        df.to_sql(con=conn, name=table.__tablename__, index=True, chunksize=100, if_exists='append')

    def chunk(self, session, conn):
        to_date = int(datetime.now().timestamp())
        for key, table in self.DB_Tables.items():
            resp = Return_API_response()
            query = session.query(table.MTS)
            query = query.filter(table.MTS == session.query(func.max(table.MTS))).first()
            from_date = int(query[0].timestamp())
            sym = key.upper()
            holder = []
            date = to_date

            try:
                while date > from_date:
                    ipdata = resp.api_response(
                        self.endpoint + f"fsym={sym}&tsym=USD&limit=2000&toTs={date} \
                                        &aggregate={self.delta[:-1]}&e=CCCAGG&api_key={self.APIkey}")
                    if ipdata['Type'] == 100:
                        holder.append(pd.DataFrame(ipdata['Data']))
                        date = ipdata['TimeFrom']
                    else:
                        log.info(f"CompareChunk {sym} {ipdata['Type']} {ipdata['Message']} {ipdata['Response']}")

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

            except Exception as err:
                log.error(f'CompareAPI - {key} {err.args} {err.value}')




            resp.close_session()
