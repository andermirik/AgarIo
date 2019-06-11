from random import random, randint
from threading import Lock
from math import sqrt
import copy
KOEF = 1

class World:
    def __init__(self):
        self.width = 1800
        self.height = 900
        self.players = {}
        self.mutex = Lock()

    def addPlayer(self, sid):
        self.mutex.acquire()
        x = random()*self.width
        y = random()*self.height
        speed = 10
        if len(sid)<6:
            speed = 0
        self.players[sid] = {
          'circles': [
              {
                'position': [x, y],
                'radius': randint(50, 100),
                'speed' : speed
              }
          ],
          'vector':[0, 0],
          'distance':0,
          'image_code':randint(0, 5)
         }
        self.mutex.release()

    def removePlayer(self, sid):
        self.mutex.acquire()
        self.players.pop(sid, None)
        self.mutex.release()

    def updatePlayerWithSid(self, sid, data):
        self.mutex.acquire()
        self.players[sid]['vector'] = data['vector']
        self.players[sid]['distance'] = data['distance']
        self.mutex.release()


    def updateState(self):
        self.mutex.acquire()
        for sid in self.players:
            player = self.players[sid]
            self.calculateMovePlayer(player)
        self.mutex.release()


    def generateStateForSid(self, sid):
        self.mutex.acquire()
        players = copy.deepcopy(self.players)
        x, y = players[sid]['circles'][0]['position']
        for player in players.values():
            player['circles'][0]['position'][0] -= x
            player['circles'][0]['position'][1] -= y
            player['circles'][0]['position'][0] *= KOEF
            player['circles'][0]['position'][1] *= KOEF
            player['circles'][0]['radius']*=KOEF
        self.mutex.release()
        return players

    def calculateMovePlayer(self, player):
        for circle in player['circles']:
            speed = circle['speed']
            dist = player['distance']

            if dist < circle['radius'] and dist != 0:
                speed = circle['speed']/(circle['radius']/dist)

            circle['position'][0]-=player['vector'][0]*speed
            circle['position'][1]-=player['vector'][1]*speed

            circle['position'][0] = max(min(circle['position'][0], self.width), 0)
            circle['position'][1] = max(min(circle['position'][1], self.height), 0)


    def distance(self, p1, p2):
        return sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2)

    def normalize(self, vector):
        speed = sqrt(vector[0]**2 + vector[1]**2)
        if speed != 0:
            vector[0]*= 1/speed
            vector[1]*= 1/speed
        else:
            vector[0] = 0
            vector[1] = 0
        return vector
