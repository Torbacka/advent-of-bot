import os

import aiohttp

SLACK_TOKEN = os.getenv("SLACK_TOKEN")


async def send(message):
    async with aiohttp.ClientSession() as session:
        async with session.post(url=f"https://slack.com/api/chat.postMessage",
                               headers={'Authorization': f"Bearer {SLACK_TOKEN}"},
                               data={
                                   "channel": "C02P3RYH0E6",
                                   "text": message
                               }) as response:
                body = await response.json()
                print(f"Something went wrong with posting to slack {response.status}, {body}")
