import sys, time
from datetime  import datetime
# third party imports
import pandas as pd
import logging

# from Time Machine
from .database.db_init import DB_Tables
from .utils import Email
from .coin import Coin

log = logging.getLogger(__name__)


def monitor(delta, interval, Session):
	"""Running in it's own thread monitor continually updates the Altcoins and
	checks for any signals from the Moving Averages"""
	altcoins = _init_Coins()
	while True:
		session = Session()
		try:
			Monitor(session).check(altcoins)
			# session.close()
		except:
			session.rollback()
			log.debug('Oh deBugger', exc_info=True)
		finally:
			session.close()
			log.warn('Monitor')        

		# set the sleep interval ...
		time.sleep(interval[delta])


class Monitor:
	"""This class is instantiated every interval. Monitoring each coin 
	DataFrame, upon a moving average signal sending out user emails. Updating 
	each coin instance with timestamp, trend and latest price"""
	def __init__(self, session):
		self.session = session


	def check(self, altcoins):
		DF_Tables = self._get_DF_Tables()
		# for each DB table generate dataframe check for signal then update coin
		try:
			for i, df in DF_Tables.items():
				coin = altcoins[i]
				cross = self._crossover(df)
				coin.setPrice(df['Close'].iloc[-1])
				if len(cross) > 0 and coin.nextSignal(cross.index.max()):
					log.warn(f'Cross signal detected for {coin.name()}')
					transaction = cross['Transaction'].iloc[-1]
					coin.setTrend(transaction)
					Email(coin.name(), transaction).sendEmail('TWGuy66@gmail.com')
		except Exception:
			log.error(f"Error with coin {coin.name()}", exc_info=True)
			
			

	def _get_DF_Tables(self, resample='6H', sma=10, bma=27, lma=74):
		"""Generate a DataFrame for each DB_Table, reasmple back from the present
		time i.e. the right of the sample frequency interval. Add in the moving averages
		"""
		DF_Tables = {}
		for i, table in DB_Tables.items():
			data = self.session.query(table.MTS, table.Open, table.Close,
								table.High, table.Low).all()
			df = pd.DataFrame([[item for item in tpl] for tpl in data],
							columns=('MTS', 'Open', 'Close', 'High', 'Low'))
			latest_timestamp = df['MTS'].max()
			base = latest_timestamp.hour + latest_timestamp.minute/60.0
			df.set_index('MTS', drop=True, inplace=True)
			df.drop_duplicates()
			df = df.groupby('MTS')['Open', 'Close', 'High', 'Low'].mean()
			df = df.resample(rule=resample, closed='right', label='right', base=base).agg(
				{'Open': 'first', 'Close': 'last', 'High': 'max', 'Low': 'min'})
			df['sewma'] = df['Close'].ewm(span=sma).mean()
			df['bewma'] = df['Close'].ewm(span=bma).mean()
			df['longewma'] = df['Close'].ewm(span=lma).mean()
			DF_Tables[i] = df
		
		return DF_Tables


	def _crossover(self, dataset):
		"""Record ant crossing points of the moving averages"""
		record = []
		# use 2nd db record as 1st has equal MA values
		Higher = dataset.iloc[1]['sewma'] > dataset.iloc[1]['bewma']
		for date, row in dataset.iterrows():
			if Higher:
				# Sell condition
				if row['sewma'] / row['bewma'] < 1:
					record.append([date, row['Close'], 'Sell'])
					Higher = not Higher
			else:
				# Buy condition
				if row['sewma'] / row['bewma'] > 1:
					record.append([date, row['Close'], 'Buy'])
					Higher = not Higher
		
		cross = pd.DataFrame(record, columns=('Date Close Transaction').split())
		cross.set_index('Date', drop=True, inplace=True)
		return cross

def _init_Coins():
	# Initialize coins
	altcoins = {
		'avt': Coin('Aventus'),
		'bch': Coin('Bitcoin Cash'),
		'btc': Coin('Bitcoin'),
		'btg': Coin('Bitcoin Gold'),
		'dsh': Coin('Dash'),
		'etc': Coin('Ethereum Classic'),
		'eth': Coin('Ethereum'),
		'eos': Coin('Eosio'),
		'fun': Coin('FunFair'),
		'gnt': Coin('Golem'),
		'iot': Coin('Iota'),
		'ltc': Coin('Litecoin'),
		'neo': Coin('Neon'),
		'omg': Coin('Omisego'),
		'qsh': Coin('QASH'),
		'qtm': Coin('Qtum'),
		'rcn': Coin('Ripio Credit Network (RCN)'),
		'rlc': Coin('iExec (RLC)'),
		'san': Coin('Santiment'),
		'spk': Coin('SpankChain'),
		'trx': Coin('Tron'),
		'xlm': Coin('Stella Lumen'),
		'xmr': Coin('Monero'),
		'xrp': Coin('Ripple'),
		'zec': Coin('Zcash')
		}
	return altcoins
