import os
import discord


TOKEN = "DISCORD_TOKEN"
CHANNEL_ID = 123

client = discord.Client()


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


async def send_message(message):
    channel = client.get_channel(CHANNEL_ID)
    await channel.send(message)


# client.run(TOKEN)
