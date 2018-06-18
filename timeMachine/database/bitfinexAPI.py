from datetime import datetime
import logging

# third party imports
from sqlalchemy import func

# from TimeMachine
from .models import DB_Tables
from ..crypto.utils import Return_API_response, Error_429


log = logging.getLogger(__name__)

class BitfinexAPI:
    """chunk_update will bring the DB up to date from Bitfinex API relative to
     the last DB entry"""

    @classmethod
    def chunk(self, session,  delta, bitfinexURL, interval):
        resp = Return_API_response()
        for key, table in DB_Tables.items():
            # find time of last entry
            query = session.query(table.MTS).filter(
                table.MTS == session.query(func.max(table.MTS))).all()
            if query == []:  # Check for empty db-table
                limit = 1000
            else:
                # How many 'intervals' since last entry
                if delta in ('5m', '15m'):
                    limit = int((datetime.now() - query[0][0]).total_seconds() // interval[delta])
                else:
                    limit = int((datetime.utcnow() - query[0][0]).total_seconds() // interval[delta])
            if limit > 1000:
                log.error(f'Bitfinex DB missing data:= {key} limit={limit}')
                limit = 1000
            if limit > 0:
                sym = key.upper() + 'USD'
                try:
                    data = resp.api_response(bitfinexURL + f'{delta}:t{sym}/hist?limit={limit}')[::-1]
                    inventory = []
                    for row in data:
                        inventory.append(table(
                            MTS=datetime.fromtimestamp(row[0]/1000),
                            Open=row[1],
                            Close=row[2],
                            High=row[3],
                            Low=row[4],
                            Volume=row[5]
                            ))
                    session.bulk_save_objects(inventory)
                    session.commit()
                except Error_429 as err:
                    log.info(f'Bitfinex {key} 429 error {err.args}')
                except Exception as err:
                    log.error(f'BitfinexAPI {key} {err.args}')

        resp.close_session()          
