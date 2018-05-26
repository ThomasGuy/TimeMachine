from datetime import datetime
import logging

# third party imports
from sqlalchemy import func

# from TimeMachine
from .db_init import DB_Tables
from ..utils import Return_API_response


log = logging.getLogger(__name__)

class Chunk_update:
    """chunk_update will bring the DB up to date relative to the last
    DB entry"""
    def chunk(self, session, delta, endpoint, interval):
        resp = Return_API_response()
        for key, table in DB_Tables.items():
            # find time of last entry
            query = session.query(table.MTS).filter(
                table.MTS == session.query(func.max(table.MTS))).all()
            if query == []:  # Check for empty db-table
                limit = 1000
            else:
                # How many 'intervals' since last entry
                limit = int((datetime.now() - query[0][0]).total_seconds() // interval[delta])
            sym = key.upper() + 'USD'
            if limit > 0:
                data = resp.api_response(endpoint + f'{delta}:t{sym}/hist?limit={limit}')[::-1]
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

        resp.close_session()
