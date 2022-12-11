import os

import aiohttp

SLACK_TOKEN = os.getenv("SLACK_TOKEN")


async def send(message):
    async with aiohttp.ClientSession() as session:
        async with session.post(url=f"https://slack.com/api/chat.postMessage",
                               headers={'Authorization': f"Bearer {SLACK_TOKEN}"},
                               data={
                                   "channel": "C04DMKVFB0R",
                                   "text": message
                               }) as response:
                body = await response.json()
                print(f"Slack status {response.status}, {body}")
