import time
from yfinance_connector import get_prepped_df
from discord_connector import client, CHANNEL_ID
from secrets import TOKEN
import asyncio
import discord


starttime = time.time()
interval = 60.0 * 15
ticker = "SPY"
short_ma_period = 21
long_ma_period = 34


async def stock_watch_job():
    await client.wait_until_ready()
    f = client.get_all_channels()
    print(list(f))

    while not client.is_closed():
        try:
            ohlc = get_prepped_df(ticker, short_ma_period, long_ma_period)
            last_bar = ohlc.iloc[-1]

            channel = client.get_channel(CHANNEL_ID)
            em1 = discord.Embed(title="Downtrend", description=str(last_bar), colour=0xFF0000)
            em2 = discord.Embed(title="Uptrend", description=str(last_bar), colour=0x008000)
            # await channel.send(f'{ticker}\n{last_bar}')
            await channel.send(embed=em1)
            await channel.send(embed=em2)
            await asyncio.sleep(5)

            # if last_bar['Crossover'] is True:
            #     # Get AI Prediction
            #     pass

        except Exception as e:
            print(str(e))
            await asyncio.sleep(5)

client.loop.create_task(stock_watch_job())
client.run(TOKEN)
