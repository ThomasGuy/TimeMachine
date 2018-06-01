from datetime import datetime
import logging

# third party imports
import pandas as pd
from sqlalchemy import func

# from TimeMachine
from .db_init import CryptoCompare_DB_Tables
from ..utils import Return_API_response


log = logging.getLogger(__name__)


class Chunk_CompareAPI:
    """Chunk update for the CryptoCompare API"""

    def chunk(self, session,  delta, compareURL, interval):
        resp = Return_API_response()
        for key, table in CryptoCompare_DB_Tables.items():
            try:
                # find time of last entry
                query = session.query(table.MTS).filter(
                    table.MTS == session.query(func.max(table.MTS))).all()
            except:
                log.error('compare Chunk query Bollocks', exc_info=True)
            
            if query == []:  # Check for empty db-table
                limit = 2000
            else:
                limit = int((datetime.utcnow() - query[0][0]).total_seconds()
                             // interval[delta])
            
            if limit > 0:
                try:
                    sym = key.upper()
                    data = resp.api_response(compareURL + 
                        f'fsym={sym}&tsym=USD&limit={limit}&aggregate={delta[:-1]}')
                    data = pd.DataFrame(data['Data'])
                    data['time'] = pd.to_datetime(data['time'], unit='s')
                    inventory = []
                    # Miss first row, CompareAPI gives us 1 extra row at he begining
                    for i in range(1, len(data)):
                        inventory.append(table(
                            MTS=data.loc[i]['time'],
                            Open=data.loc[i]['open'],
                            Close=data.loc[i]['close'],
                            High=data.loc[i]['high'],
                            Low=data.loc[i]['low'], 
                            Volume=data.loc[i][['volumefrom','volumeto']].sum()
                            ))
                    session.bulk_save_objects(inventory)
                    session.commit()
                except KeyError as err:
                    log.error(f'Where is it {key} code: {data.response}\n \
                                {data}\n{err}\n', exc_info=True)
        
        resp.close_session()
