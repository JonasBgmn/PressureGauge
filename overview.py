import requests
from datetime import datetime
import os

api_key = os.getenv("STEAM_WEB_API_KEY")
public_user_steam_id = "76561198310145074"

is_vanity = False
vanity_test_list = list(public_user_steam_id)

if len(vanity_test_list) != 17:
    is_vanity = True
else:
    for char in vanity_test_list:
        if not char.isnumeric():
            is_vanity = True
            break

vanity_url = f"http://api.steampowered.com/ISteamUser/Resolvevanity_url/v0001/?key={api_key}&vanity_url={public_user_steam_id}"

if is_vanity:
    response = requests.get(vanity_url)
    user_steam_id = response.json()["response"]["steamid"]
else:
    user_steam_id = public_user_steam_id

url_acc = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={api_key}&steamids={user_steam_id}"
url_owned_games = f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key={api_key}&steamid={user_steam_id}"

response_acc = requests.get(url_acc)
data_acc = response_acc.json()

response_owned_games = requests.get(url_owned_games)
data_owned_games = response_owned_games.json()

print(f"publicid: {public_user_steam_id}")

col_list = ["steamid", "personaname", "personastate", "gameid"]

for col in col_list:
    try:
        value = data_acc["response"]["players"][0][col]
        print(f"{col}: {value}")
    except KeyError:
        print(f"{col}: none")

last_online_time = datetime.fromtimestamp(data_acc["response"]["players"][0]["lastlogoff"]).strftime("%Y-%m-%d %H:%M:%S")
print(f"lastonline: {last_online_time}")

games = data_owned_games["response"]["games"]

played_games = []
i = 0
for game in games:
    if data_owned_games["response"]["games"][i]["rtime_last_played"] > 0:
        played_games.append(game)
    i += 1

played_games.sort(key=lambda x: x['rtime_last_played'], reverse=True)

if played_games:
    last_game = played_games[0]
    last_played_time = datetime.fromtimestamp(last_game['rtime_last_played']).strftime('%Y-%m-%d %H:%M:%S')
    print(f"lastplayed: {last_played_time}")
    if last_played_time > last_online_time:
        print("user faked offline")
    else:
        print("user is honest")
else:
    print("lastplayed: no last game found")