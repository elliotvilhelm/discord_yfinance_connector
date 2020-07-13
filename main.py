import time
from datetime import datetime
from yfinance_connector import get_prepped_df
from discord_connector import client, CHANNEL_ID
from secrets import TOKEN
import asyncio
import discord
import sys


if len(sys.argv) != 7:
    print("Usage: python main.py <TICKER> <TIME_FRAME> <REQ_PERIOD> <PROFITABLE> <SHORT_MA> <LONG_MA>")
    exit(1)


starttime = time.time()
interval = 60.0 * 15
ticker = sys.argv[1]
time_frame = sys.argv[2]
req_period = sys.argv[3]
profitable = sys.argv[4]
short_ma_period = int(sys.argv[5])
long_ma_period = int(sys.argv[6])
red = 0xFF0000
green = 0x008000


async def stock_watch_job():
    await client.wait_until_ready()

    while not client.is_closed():
        try:
            ohlc = get_prepped_df(ticker, short_ma_period, long_ma_period, period=req_period, interval=time_frame)
            last_bar = ohlc.iloc[-1]

            channel = client.get_channel(CHANNEL_ID)
            if last_bar['MA_21'] > last_bar['MA_34']:
                trend = "Uptrend"
                color = green
            else:
                trend = "Downtrend"
                color = red

            if last_bar['Crossover']:
                time = datetime.now().strftime("%I:%M %p") + " PT"
                em1 = discord.Embed(title=f'${ticker}', description="https://www.theprofitgate.com", colour=color)
                em1.add_field(name="Current Price", value=f"${last_bar['Close']}")
                em1.add_field(name="Time Frame", value=time_frame)
                em1.add_field(name="Trend", value=trend)
                em1.add_field(name="Time", value=time)
                em1.add_field(name="Short MA", value=short_ma_period)
                em1.add_field(name="Long MA", value=long_ma_period)
                em1.add_field(name="Profitable", value=f"{profitable}%")
                em1.set_footer(text="©2020 by The Profit Gate", icon_url="https://static.wixstatic.com/media/14f8c6_3f1c2f683b174f8c84505832d46150bf~mv2.png/v1/fill/w_242,h_242,al_c,q_85,usm_0.66_1.00_0.01/circle-cropped%20(6).webp")
                em1.set_thumbnail(url="https://static.wixstatic.com/media/14f8c6_3f1c2f683b174f8c84505832d46150bf~mv2.png/v1/fill/w_242,h_242,al_c,q_85,usm_0.66_1.00_0.01/circle-cropped%20(6).webp")
                await channel.send(embed=em1)
                await channel.send("@here")

            await asyncio.sleep(interval)

        except Exception as e:
            print(str(e))
            await asyncio.sleep(interval)

client.loop.create_task(stock_watch_job())
client.run(TOKEN)
