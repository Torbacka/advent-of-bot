from datetime import datetime

import discord

client = discord.Client()
start_time = datetime(2021, 12, 1, 6, 00, 00)


async def send_congratulations(message):
    await client.wait_until_ready()
    channel = client.get_channel(777301286390726663)
    await channel.send(message)


async def countdown():
    now = datetime.now()
    if now > start_time:
        return
    await client.wait_until_ready()
    channel = client.get_channel(777301286390726663)
    timedelta = start_time - now
    messages = await channel.history(limit=300).flatten()
    res=[message for message in messages if message.content[0:19] == 'Det roliga start om']
    if len(res) > 0:
        await res[0].edit(content=
            f"Det roliga start om: {str(timedelta).split('.')[0]}")
    else:
        await channel.send(
            f"Det roliga start om: {str(timedelta).split('.')[0]}")
