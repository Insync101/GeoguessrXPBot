# Written by octin M8 D30 Y2022.

from http import cookies
import requests
import time
import uuid

def getDomain(v, id = ''):
    if v == 'singleplayer':
        return 'https://www.geoguessr.com/api/v3/games/{}'.format(id)  
    else:
        return 'https://game-server.geoguessr.com/api/{}/{}'.format(v, id)

class geoMatch:
    def __init__(self, matchInfo, cookies, debugMode):
        self.token = matchInfo['token']
        self.matchURL = getDomain('singleplayer', matchInfo['token'])

        self.info = matchInfo
        self.cookies = cookies
        self.debugMode = debugMode
        if debugMode:
            print('Match[{}] has been successfully created.'.format(matchInfo['token']))

    def plonkAt(self, lat, lng):
        plonkResponse = requests.post(self.matchURL, cookies = self.cookies, json = {'lat': lat, 'lng': lng, 'timedOut': False, 'token': self.token})
        self.info = plonkResponse.json() # Updates match state.

        if self.debugMode:
            print('Match[{}] marker set at [{}, {}] for round [{}]'.format(self.token, lat, lng, self.info['round']))

    def nextRound(self):
        if self.info['state'] == 'started':
            proceedRound = requests.get(self.matchURL, cookies = self.cookies, params = {'client': 'web'}, headers = {'Content-type': 'application/json'})
            self.info = proceedRound.json() # Updates match state.
            
            if self.debugMode:
                print('Match[{}] has moved into the next round [{}]'.format(self.token, self.info['round']))
        else:
            print('Match[{}] is finished.'.format(self.token))

class newInstance:
    matches = []

    def __init__(self, cookies, debugMode = False):
        self.cookies =  cookies
        self.debugMode = debugMode
        self.instanceId = uuid.uuid4().hex

        if debugMode:
            print('A new instance has been created [{}]'.format(self.instanceId))

    def newMatch(self, matchSettings):
        if self.debugMode:
            print('Creating a new match.')

        matchResponse = requests.post(getDomain('singleplayer'), cookies = self.cookies, json = matchSettings, headers = {'Content-type': 'application/json'})
        self.matches.append(geoMatch(matchResponse.json(), self.cookies, self.debugMode))
        return self.matches[-1]

    def runningMatches(self):
        onGoing = []

        for match in self.matches:
            if match.info['state'] == 'started':
                onGoing.append(match)
        
        return onGoing