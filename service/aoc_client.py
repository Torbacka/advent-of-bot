import json
import os
from datetime import datetime, timedelta
from os.path import isfile

import aiohttp
from dotenv import load_dotenv

load_dotenv()
start_date = datetime(2020, 12, 1, 6, 0)
AOC_COOKIE = os.getenv("AOC_COOKIE")


async def retrieve_leaderboard(board_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=f"https://adventofcode.com/2020/leaderboard/private/view/{board_id}.json",
                               headers={'Cookie': AOC_COOKIE}) as response:
            leaderboard = await response.json()
            print(leaderboard)
            message = dict()
            if isfile(f"data/leaderboard_{board_id}.json"):
                with open(f"data/leaderboard_{board_id}.json", "r") as old_leaderboard_file:
                    old_leaderboard = json.load(old_leaderboard_file)
                    if leaderboard == old_leaderboard:
                        return message
                    else:
                        for user_id, user in leaderboard['members'].items():
                            old_user = old_leaderboard['members'].get(user_id)
                            if user == old_user or 'name' not in user:
                                continue
                            keys = set(
                                [f"{key}:{sorted(user['completion_day_level'][key].keys(), reverse=True)[0]}"
                                 for key in user['completion_day_level'].keys()])
                            if user_id in old_leaderboard['members']:
                                old_keys = set(
                                    [f"{key}:{sorted(old_user['completion_day_level'][key].keys(), reverse=True)[0]}"
                                     for key in old_user['completion_day_level'].keys()])
                                difference = keys.difference(old_keys)
                            else:
                                difference = keys
                            for diff_day in difference:
                                day = diff_day.split(":")[0]
                                if old_user and user['completion_day_level'].get(day) == old_user[
                                    'completion_day_level'].get(day):
                                    continue
                                if day not in message:
                                    message[day] = [await extract_message(day, user)]

                                else:
                                    message[day].append(await extract_message(day, user))
            with open(f"data/leaderboard_{board_id}.json", "w") as old_leaderboard_file:
                json.dump(leaderboard, old_leaderboard_file)
            return message


async def extract_message(day, user):
    star_times = user['completion_day_level'][day]
    day_time = start_date + timedelta(days=int(day) - 1)
    part1 = datetime.fromtimestamp(int(star_times['1']['get_star_ts']))
    if '2' in star_times:
        part2 = datetime.fromtimestamp(int(star_times['2']['get_star_ts']))
        return f"{user['name']} <:silver_star:783234781017538590>  {str(part1 - day_time)} :star:  {str(part2 - day_time)}"
    else:
        return f"{user['name']} <:silver_star:783234781017538590>  {str(part1 - day_time)}"
