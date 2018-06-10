import logging, time
import threading
from sqlalchemy.orm import sessionmaker

log = logging.getLogger(__name__)

# initialize globals
delta = '15m'
db_name = f'sqlite:///c:\\data\\sqlite\\db\\tickToc{delta}.db'
interval = {'5m': 300, '15m': 900, '30m': 1800, '1h': 3600}
altcoins = None

# From TimeMachine, initialize the DB
from .database.db_init import engine, all_DB_tables
# Intialize global Session class
Session = sessionmaker(bind=engine)

# From TimeMachine
from timeMachine.app.coin import Coin
from timeMachine.app.utils import DF_Tables
from timeMachine.app.tickToc import tickToc
from timeMachine.app.monitor import monitor


def _init_Coins():
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
        'waves': Coin('Waves (WAVES)'),
        'elf': Coin('aelf (ELF')
    }

    # Set intial 'trend' Buy or Sell for each coin
    try:
        # for each DB table generate dataframe check for signal then update coin
        tables = DF_Tables.get_DFTables(all_DB_tables())
        for i, df in tables.items():
            coin = altcoins[i]
            cross = DF_Tables.crossover(df)
            coin.setTrend(cross['Transaction'].iloc[-1])
    except IndexError:
        log.error(f'Init Altcoins IndexError for {coin.name()}', exc_info=True)

    return altcoins


def main():
    global altcoins
    altcoins = _init_Coins()

    # Start tickToc
    watcher = threading.Thread(target=tickToc, args=[delta, interval, Session])
    watcher.start()
    log.info(f"TickToc started {watcher.getName()}")

    # wait then start Monitor
    time.sleep(30)
    looking = threading.Thread(target=monitor, args=[delta, interval, altcoins])
    looking.start()
    log.info(f"Monitor started {looking.getName()}")
