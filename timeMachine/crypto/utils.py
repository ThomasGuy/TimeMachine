"""
Provides utility functions used across more than one module or sub module.

"""

# Import Built-Ins
import logging
import json
import sys, time
import smtplib
import warnings

# Import Third-Party
import requests
import pandas as pd

# package imports
# from ..database.base import session_factory as Session


# Init Logging Facilities
log = logging.getLogger(__name__)


class Error_429(Exception):
    pass

class Empty_Table(Exception):
    pass


# get request response from exchange api
class Return_API_response:
    """Get data from BitFinex API. Bitfinex rate limit policy can vary in a
     range of 10 to 90 requests per minute. So if we get a 429 response wait
     for a minute"""
    def __init__(self):
        self.sesh = requests.Session()

    def api_response(self, url):
        try:
            res = self.sesh.get(url)
            data = res.json()
            if res.status_code == 429:
                raise Error_429

            res.raise_for_status()
        except Error_429 as err:
            raise Error_429
        except requests.exceptions.HTTPError as err:
            log.info(f'Raise_for_status: {err.__class__.__name__}')
            raise err
            
        return data

    def close_session(self):
        self.sesh.close()


class Email:
    """Send Email to users"""
    def __init__(self, coinName, transaction):
        self.name = coinName
        self.msg = transaction

    def _findUser(self, coin):
        """Find all users who hold this coin"""
        pass

    @staticmethod
    def sendEmail(name, msg, to_addr='twguy66@gmail.com'):
        """Send user email"""
        header = 'From: room4rent@buriramvillas.com\n'
        header += f'To: {to_addr}\n'
        header += 'Subject: MA-Alert\n'
        message = header + f'Moving average:- {name} advises {msg} indicator...'
        
        smtpObj = smtplib.SMTP('smtp.stackmail.com', 587)
        smtpObj.ehlo()
        smtpObj.starttls()
        smtpObj.login('room4rent@buriramvillas.com', 'Sporty66')
        sendmailStatus = smtpObj.sendmail('room4rent@buriramvillas.com', to_addr, message)
        if sendmailStatus != {}:
            log.error('There was a problem sending email to %s: %s' %
                    (to_addr, sendmailStatus), exc_info=True)
        smtpObj.quit()
        log.info(f"Email sent {name} is on '{msg}' trend")


class DF_Tables:
    """Generate a DataFrame for each DB_Table, reasmple back from the present
    time i.e. the right of the sample frequency interval. Add in the moving averages
    """
    # Note I use the same index for DB, DF and altcoins

    @classmethod
    def get_DFTables(self, session, dbTables, sma=10, bma=27, lma=74, resample='6H'):
        DF_Tables = {}
        # session = Session()
        try:
            for i, table in dbTables.items():
                data = session.query(table.MTS, table.Open, table.Close,
                                            table.High, table.Low).all()
                if data == []:
                    raise Empty_Table
                df = pd.DataFrame([[item for item in tpl] for tpl in data],
                                    columns=('MTS', 'Open', 'Close', 'High', 'Low'))
                df.set_index('MTS', drop=True, inplace=True)
                latest_timestamp = df.index.max()
                base = latest_timestamp.hour + latest_timestamp.minute/60.0
                df.drop_duplicates()
                df = df.groupby('MTS')['Open', 'Close', 'High', 'Low'].mean()
                df = df.resample(rule=resample, closed='right', label='right', base=base).agg(
                    {'Open': 'first', 'Close': 'last', 'High': 'max', 'Low': 'min'})
                df['sewma'] = df['Close'].ewm(span=sma).mean()
                df['bewma'] = df['Close'].ewm(span=bma).mean()
                df['longewma'] = df['Close'].ewm(span=lma).mean()
                DF_Tables[i] = df
        except AttributeError:
            log.error(f'{i} in {table} ', exc_info=True)
        except Empty_Table as err:
            log.info(f'Empty Table {i} in {table} errors: {err.args}', exc_info=True)
        except Exception as err:
            raise(err)
        finally:
            session.close()

        return DF_Tables


    @classmethod
    def crossover(self, dataset):
        """From DataFrame 'dataset'. Return a DataFrame of all crossing points
         of the moving averages"""
        record = []
        # Don't use 1st db record as it has equal SEWMA = BEWMA
        Higher = dataset.iloc[4]['sewma'] > dataset.iloc[4]['bewma']
        # initialize record[] ensures record is never empty
        if Higher:
            record.append([dataset.index[4], dataset['Close'].iloc[4], 'Buy'])
        else:
            record.append([dataset.index[4], dataset['Close'].iloc[4], 'Sell'])

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)
            for date, row in dataset.iterrows():
                if Higher:
                    # Sell condition
                    if row['sewma'] / row['bewma'] < 0.9965:
                        record.append([date, row['Close'], 'Sell'])
                        Higher = not Higher
                else:
                    # Buy condition
                    if row['sewma'] / row['bewma'] > 1.0035:
                        record.append([date, row['Close'], 'Buy'])
                        Higher = not Higher


        cross = pd.DataFrame(record, columns=('Date Close Transaction').split())
        cross.set_index('Date', drop=True, inplace=True)
        return cross

                                                       
class Queue:
    """Queue class"""
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0, item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)


if __name__=='__main__':
    pass
