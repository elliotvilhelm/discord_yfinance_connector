import time
from yfinance_connector import get_prepped_df
from discord_connector import client, CHANNEL_ID
from secrets import TOKEN
import asyncio
import discord


starttime = time.time()
interval = 60.0 * 15
time_frame = "15m"
ticker = "ES"
short_ma_period = 21
long_ma_period = 34
red = 0xFF0000
green = 0x008000


async def stock_watch_job():
    await client.wait_until_ready()

    while not client.is_closed():
        try:
            ohlc = get_prepped_df(ticker, short_ma_period, long_ma_period, interval=time_frame)
            last_bar = ohlc.iloc[-1]

            channel = client.get_channel(CHANNEL_ID)
            if last_bar['MA_21'] > last_bar['MA_34']:
                trend = "Uptrend"
                color = green
            else:
                trend = "Downtrend"
                color = red

            em1 = discord.Embed(title=f'${ticker}', colour=color)
            em1.add_field(name="Current Price", value=f"${last_bar['Close']}")
            em1.add_field(name="Time Frame", value=time_frame)
            em1.add_field(name="Trend", value=trend)

            await channel.send(embed=em1)
            await asyncio.sleep(5)

            # if last_bar['Crossover'] is True:
            #     # Get AI Prediction
            #     pass

        except Exception as e:
            print(str(e))
            await asyncio.sleep(5)

client.loop.create_task(stock_watch_job())
client.run(TOKEN)
