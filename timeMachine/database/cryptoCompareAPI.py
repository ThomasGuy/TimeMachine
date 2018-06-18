from datetime import datetime
import logging

# third party imports
import pandas as pd
from sqlalchemy import func

# from TimeMachine
from .models import CryptoCompare_DB_Tables
from ..crypto.utils import Return_API_response


log = logging.getLogger(__name__)


class CompareAPI:
    """Chunk update for the CryptoCompare API"""

    @classmethod
    def chunk(self, session,  delta, compareURL, interval):
        resp = Return_API_response()
        for key, table in CryptoCompare_DB_Tables.items():
            try:
                # find time of last entry
                query = session.query(table.MTS).filter(
                    table.MTS == session.query(func.max(table.MTS))).all()
            except Exception as err:
                log.error(f'compare Chunk query DB-Bollocks {err.args}', exc_info=True)
            
            if query == []:  # Check for empty db-table
                limit = 2000
            else:
                limit = int((datetime.utcnow() - query[0][0]).total_seconds()
                             // interval[delta])
            if limit > 2000:
                log.error(f'CryptoCompare DB missing data:= {key} limit={limit}')
                limit = 2000
            if limit > 0:
                try:
                    sym = key.upper()
                    data = resp.api_response(compareURL + 
                        f"fsym={sym}&tsym=USD&limit={limit}&aggregate={delta[:-1]}")
                    
                    if data['Type'] >= 100:
                        df = pd.DataFrame(data['Data'])
                        df['time'] = pd.to_datetime(df['time'], unit='s')
                        inventory = []
                        # Miss first row, CompareAPI gives us 1 extra row at he begining
                        for i in range(1, len(df)):
                            inventory.append(table(
                                MTS=df.loc[i]['time'],
                                Open=df.loc[i]['open'],
                                Close=df.loc[i]['close'],
                                High=df.loc[i]['high'],
                                Low=df.loc[i]['low'], 
                                Volume=df.loc[i][['volumefrom','volumeto']].sum()
                                ))
                        session.bulk_save_objects(inventory)
                        session.commit()
                    else:
                        if data['Type'] == 99:
                            log.info(f"CompareChunk {sym} {data['Message']}") 
                        
                except Exception as err:
                    log.error(f'CompareAPI - {key} {err.args}')
        
        resp.close_session()
