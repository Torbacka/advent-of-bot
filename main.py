import asyncio
import os

from dotenv import load_dotenv
from datetime import datetime
from service.aoc_client import retrieve_leaderboard
from service.discord_client import client, send_congratulations
from service.slack_client import send

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")


async def congratulate_competitor():
    if not os.path.exists('data'):
        os.makedirs('data')
    leaderboard1 = await retrieve_leaderboard("141549")
    leaderboard2 = await retrieve_leaderboard("277430")
    leaderboard3 = await retrieve_leaderboard("1518258")
    leaderboards = {**leaderboard1, **leaderboard2}
    message = ""
    for day, user_messages in leaderboards.items():
        if len(message) > 0:
            message += '\n\n'
        message += f"Day {day}\n"
        message += '\n'.join(user_messages)
    if len(message) > 0:
        await send_congratulations(message)
    message = ""
    for day, user_messages in leaderboard3.items():
        if len(message) > 0:
            message += '\n\n'
        message += f"Day {day}\n"
        message += '\n'.join([message.replace('<:silver_star:783234781017538590>', ':silver_star:') for message in user_messages])
    if len(message) > 0:
        await send(message)
    await client.close()
    print(f"Done executing {datetime.now()}", )


async def main():
    asyncio.create_task(client.start(DISCORD_TOKEN))
    asyncio.create_task(congratulate_competitor())
    while len(asyncio.all_tasks()) > 1:  # Any task besides loop_job() itself?
        await asyncio.sleep(0.2)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
