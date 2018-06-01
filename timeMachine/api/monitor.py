"""
Two Data structures used to translate the Database and keep the State of the 
altcoins. The two dictionaries DB_Tables and altcoins use the same keys, as 
well as pandas DF_Tables which is generated from DB after every iteration.
"""

import sys, time
from datetime  import datetime
# third party imports
import pandas as pd
import logging

# from Time Machine
from .database.db_init import DB_Tables, CryptoCompare_DB_Tables
from .utils import Email
from .coin import Coin

log = logging.getLogger(__name__)


def monitor(delta, interval, Session):
	"""Running in it's own thread monitor continually updates the Altcoins and
	checks for any signals from the Moving Averages"""
	all_DB_Tables = {}
	for table in [DB_Tables, CryptoCompare_DB_Tables]:
		for i, v in table.items():
			all_DB_Tables[i] = v
	
	altcoins = _init_Coins(Session, all_DB_Tables)
	
	while True:
		session = Session()
		try:
			Monitor(session, all_DB_Tables).check(altcoins)
		except:
			session.rollback()
			log.error('Oh deBugger', exc_info=True)
		finally:
			session.close()
			log.info('Monitor complete')        

		# set the sleep interval ...
		time.sleep(interval[delta])


class Monitor:
	"""This class is instantiated every interval. Monitoring each altcoin's
	DataFrame, upon a moving average signal sending out user emails. Updating 
	each 'altcoin' instance with timestamp, trend and latest price"""
	def __init__(self, session, dbTables):
		self.session = session
		self.dbTables = dbTables


	def check(self, altcoins):
		DF_Tables = self._get_DF_Tables()
		# for each DB table generate dataframe check for signal then update coin
		try:
			for i, df in DF_Tables.items():
				coin = altcoins[i]
				cross = self._crossover(df)
				coin.setPrice(df['Close'].iloc[-1])
				transaction = cross['Transaction'].iloc[-1]
				if not coin.trend() == transaction and coin.nextSignal(cross.index.max()):
					coin.setTrend(transaction)
					Email.sendEmail(coin.name(), transaction)

		except Exception:
			log.error(f"Error with coin {coin.name()}", exc_info=True)
			

	def _get_DF_Tables(self, resample='6H', sma=10, bma=27, lma=74):
		"""Generate a DataFrame for each DB_Table, reasmple back from the present
		time i.e. the right of the sample frequency interval. Add in the moving averages
		"""
		# Combine the 2 DB_Tables to get all the tables. Note I use the same
		#  index for DB, DF and altcoins
		
		DF_Tables = {}
		try:
			for i, table in self.dbTables.items():
				data = self.session.query(table.MTS, table.Open, table.Close,
									table.High, table.Low).all()
				df = pd.DataFrame([[item for item in tpl] for tpl in data],
								columns=('MTS', 'Open', 'Close', 'High', 'Low'))
				df.set_index('MTS', drop=True, inplace=True)
				latest_timestamp = df.index.max()
				# log.info(f'{i} {table}/n{df.head()}/nLatest_timestamp = {latest_timestamp}')
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
		except:
			raise
			 
		return DF_Tables


	def _crossover(self, dataset):
		"""Record all crossing points of the moving averages"""
		record = []
		# use 5th db record as 1st has equal MA values
		Higher = dataset.iloc[5]['sewma'] > dataset.iloc[5]['bewma']
		# adding a record ensures record is never empty
		if Higher:
			record.append([dataset.index.min(), dataset['Close'].iloc[0], 'Buy'])
		else:
			record.append([dataset.index.min(), dataset['Close'].iloc[0], 'Sell'])
		
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

def _init_Coins(Session, all_DB_Tables):
	# Initialize coins
	altcoins = {
		'avt': Coin('Aventus (AVT)'),
		'bch': Coin('Bitcoin Cash (BTH)'),
		'btc': Coin('Bitcoin (BTC)'),
		'btg': Coin('Bitcoin Gold (BTG)'),
		'dsh': Coin('Dash (DSH)'),
		'etc': Coin('Ethereum Classic (ETC)'),
		'eth': Coin('Ethereum (ETH)'),
		'eos': Coin('Eosio (EOS)'),
		'fun': Coin('FunFair (FUN)'),
		'gnt': Coin('Golem (GNT)'),
		'iot': Coin('Iota (IOT)'),
		'ltc': Coin('Litecoin (LTC)'),
		'neo': Coin('Neon (NEO)'),
		'omg': Coin('Omisego'),
		'qsh': Coin('QASH (QSH)'),
		'qtm': Coin('Qtum (QTM)'),
		'rcn': Coin('Ripio Credit Network (RCN)'),
		'rlc': Coin('iExec (RLC)'),
		'san': Coin('Santiment (SAN)'),
		'spk': Coin('SpankChain (SPK)'),
		'trx': Coin('Tron (TRX)'),
		'xlm': Coin('Stella Lumen (XLM)'),
		'xmr': Coin('Monero (XMR)'),
		'xrp': Coin('Ripple (XRP)'),
		'zec': Coin('Zcash (ZEC)'),
		'ada': Coin('Cardano (ADA)'),
		'xvg': Coin('Verge (XVG)'),
		'xem': Coin('NEM (XEM)'),
		'ven': Coin('VeChain (VEN)'),
		'bnb': Coin('Binance Coin (BNB)'),
		'bcn': Coin('Bytecoin (BCN)'),
		'icx': Coin('ICON (ICX)'),
		'lsk': Coin('Lisk (LSK)'),
		'zil': Coin('Zilliqa (ZIL)'),
		'ont': Coin('Ontology (ONT)'),
		'ae': Coin('Aeternity (AE)'),
		'zrx': Coin('Ox (ZRX)'),
		'dcr': Coin('Decred (DCR)'),
		'nano': Coin('Nano (NANO)'),
		'waves': Coin('Waves (WAVES)')
		}


	# Set intial 'trend' Buy or Sell for each coin
	session = Session()
	initialize = Monitor(session, all_DB_Tables)
	try:
		# for each DB table generate dataframe check for signal then update coin
		DF_Tables = initialize._get_DF_Tables()
		for i, df in DF_Tables.items():
			coin = altcoins[i]
			cross = initialize._crossover(df)
			coin.setTrend(cross['Transaction'].iloc[-1])
	except IndexError:
		session.rollback()
		log.error(f'Init Altcoins error for {coin.name()}', exc_info=True)
		sys.exit()
	finally:
		session.close()

	return altcoins
