import logging

# package  imports
from .coin import Coin
from .utils import DF_Tables

log = logging.getLogger(__name__)


class Altcoin:
    """ Initialize coins """
    altcoins = {
        'avt': Coin('Aventus (AVT)'),
        'bch': Coin('Bitcoin Cash (BCH)'),
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
        'omg': Coin('Omisego (OMG)'),
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
        'elf': Coin('aelf (ELF'),
        'steem': Coin('Steem (STEEM)'),
        'mana': Coin('Decentraland (MANA)'),
        'edo': Coin('Eidoo (EDO)')
    }


    @classmethod
    def initCoin(cls, Session, dbTables):
        """ Initialize 'trend' Buy or Sell for each coin in dbTables"""
        session = Session()

        try:
            # for each DB table (Coin) generate dataframe then initialize coin
            tables = DF_Tables.get_DFTables(session, dbTables)
            for i, dataf in tables.items():
                coin = cls.altcoins[i]
                cross = DF_Tables.crossover(dataf)
                if dataf['Close'].iloc[-1]:
                    coin.price = dataf['Close'].iloc[-1]
                coin.trend = cross['Transaction'].iloc[-1]
                coin.previousSignal = cross.index[-1]
                log.info(f'Initialize: {coin}')
        except IndexError:
            log.error(
                f'Init Altcoins IndexError for {coin.name()}', exc_info=True)
        finally:
            session.close()


    def __repr__(self):
        coins = '\n'
        for coin in self.altcoins.values():
            coins += coin.__repr__() + '\n'
        return coins
