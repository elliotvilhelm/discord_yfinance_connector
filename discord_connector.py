import os
import discord
import asyncio


CHANNEL_ID = 699745065118990356

client = discord.Client()


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')



