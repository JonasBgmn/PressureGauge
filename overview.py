import requests
from datetime import datetime
import os

apiKey = os.getenv("STEAM_WEB_API_KEY")
publicUserSteamId = "76561198310145074"

isVanity = False
vanityTestList = list(publicUserSteamId)

if len(vanityTestList) != 17:
    isVanity = True
else:
    for char in vanityTestList:
        if not char.isnumeric():
            isVanity = True
            break

vanityUrl = f"http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key={apiKey}&vanityurl={publicUserSteamId}"

if isVanity:
    response = requests.get(vanityUrl)
    userSteamId = response.json()["response"]["steamid"]
else:
    userSteamId = publicUserSteamId

urlAcc = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={apiKey}&steamids={userSteamId}"
urlOwnedGames = f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key={apiKey}&steamid={userSteamId}"

responseAcc = requests.get(urlAcc)
dataAcc = responseAcc.json()

responseOwnedGames = requests.get(urlOwnedGames)
dataOwnedGames = responseOwnedGames.json()

print(f"publicid: {publicUserSteamId}")

colList = ["steamid", "personaname", "personastate", "gameid"]

for col in colList:
    try:
        value = dataAcc["response"]["players"][0][col]
        print(f"{col}: {value}")
    except KeyError:
        print(f"{col}: none")

lastOnlineTime = datetime.fromtimestamp(dataAcc["response"]["players"][0]["lastlogoff"]).strftime("%Y-%m-%d %H:%M:%S")
print(f"lastonline: {lastOnlineTime}")

games = dataOwnedGames["response"]["games"]

playedGames = []
i = 0
for game in games:
    if dataOwnedGames["response"]["games"][i]["rtime_last_played"] > 0:
        playedGames.append(game)
    i += 1

playedGames.sort(key=lambda x: x['rtime_last_played'], reverse=True)

if playedGames:
    lastGame = playedGames[0]
    lastPlayedTime = datetime.fromtimestamp(lastGame['rtime_last_played']).strftime('%Y-%m-%d %H:%M:%S')
    print(f"lastplayed: {lastPlayedTime}")
    if lastPlayedTime > lastOnlineTime:
        print("user faked offline")
    else:
        print("user is honest")
else:
    print("lastplayed: no last game found")