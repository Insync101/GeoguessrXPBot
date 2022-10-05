# Written by corewave M8 D30 Y2022. ( Make sure you have your _ncfa set in ncfa.json )

import random
import json
import time
import geoguessr

amount = 0 # To play X matches.
speed = 0 # To wait X seconds after each round.
randomness = [-0.0002, 0.0002] # How accurate you want it to be ( The lower these both values are the more accurate **[0, 0] IS ALWAYS GONNA BE 25k **)
mapId = str() # Input to which map you want. ( **RUNNING IT WITH NO RANDOMIZATION ON A POPULAR MAP WILL MAKE YOU APPEAR ON THE LEADERBOARD AND WILL GET YOU BANNED** )

f = open('ncfa.json')
cookiesTable = json.load(f)
clientInstance = geoguessr.newInstance(cookiesTable, True)

amount = int(input("Matches: "))
mapId = input("MapID: ").strip()

while True:
    speed = int(input("Seconds per round (**ANYTHING >3 SECONDS IS BANNABLE**): "))
    if speed < 3:
        answer = input("Are you sure you want set speed to {}? (**DO IT AT YOUR OWN RISK**)(Y/N): ".format(speed)).strip()
        if answer == 'Y':
            break
        else:
            pass
    else:
        break


for match in range(amount): 
    aw = clientInstance.newMatch({"map": mapId, "type": "standard", "timeLimit": 0, "forbidMoving": False, "forbidZooming": False, "forbidRotating": False})

    for round in range(5):
        matchData = aw.info
        matchTG = matchData['rounds'][-1]

        lat = matchTG['lat']
        lng = matchTG['lng']

        time.sleep(speed)
        aw.plonkAt(lat + random.uniform(randomness[0], randomness[1]), lng + random.uniform(randomness[0], randomness[1]))
        aw.nextRound()
