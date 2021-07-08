import ccxt
import sys

api_key = ""
sec_key = ""

with open("key.txt") as keys:
    for line in keys:
        key, val = line.split('=')
        if key == "api_key":
            api_key = val.rstrip()
        else:
            sec_key = val.rstrip()

binance = ccxt.binance(config={
    'apiKey' : api_key,
    'secret' : sec_key,
    'enableRateLimit' : True,
    'options' : {
        'defaultType' : 'future'
    }
})

symbol = sys.argv[1]
symbol = symbol.upper()
amount = ''

markets = binance.load_markets()
market = binance.market(symbol)
leverage = 30

resp = binance.fapiPrivate_post_leverage({
    "symbol" : symbol,
    "leverage" : leverage
})

def market_buy():
    order = binance.create_market_buy_order(symbol=symbol, amount=amount)

def market_sell(pre_price):
    while True:
        curr_price = binance.fetch_ticker(symbol).get('last')
        if curr_price >= pre_price * 1.01:
            order = binance.create_market_sell_order(symbol=symbol, amount=amount)
            break

def get_max_position_available(balance, market_price):
    position_to_use = balance / market_price
    return position_to_use

def get_balance():
    balance = binance.fetch_balance(params={"type" : "future"})
    return float(balance['USDT']['free'])

def get_market_price():
    market_price = binance.fetch_ticker(symbol)
    return float(market_price['last'])

def main() :
    balance = get_balance()
    market_price = get_market_price()
    amount = get_max_position_available(balance, market_price)
    market_buy()
    market_sell()


if __name__ == "__main__" :
    main()