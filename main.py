import time
from yfinance_connector import get_prepped_df
from discord_connector import send_message

starttime = time.time()
interval = 60.0 * 15
ticker = "SPY"
short_ma_period = 21
long_ma_period = 34


while True:
    # Be sure to launch loop on time increment you wish to be updated, e.g. if 15 min bar, launch program at 3:45
    print("tick")
    ohlc = get_prepped_df(ticker, short_ma_period, long_ma_period)
    last_bar = ohlc.iloc[-1]
    print(last_bar)
    if last_bar['Crossover'] is True:
        # Get AI Prediction
        # send_message("AI PREDICTION .........")
        pass

    time.sleep(interval - ((time.time() - starttime) % interval))
