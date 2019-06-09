from random import random
from threading import Lock
from math import sqrt

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
        self.players[sid] = {
          'position': [x, y],
          'cursor_position':[x, y]
         }
        self.mutex.release()
        return

    def removePlayer(self, sid):
        self.mutex.acquire()
        self.players.pop(sid, None)
        self.mutex.release()
        return

    def updatePlayerWithSid(self, sid, cursor_position):
        self.mutex.acquire()

        self.players[sid]['cursor_position'] = cursor_position

        self.mutex.release()
        return

    def updateState(self):
        self.mutex.acquire()

        for sid in self.players:
            player = self.players[sid]
            _from = player['position']
            _to = player['cursor_position']
            #print('from ', _from)
            #print('to ', _to)
            move = self.move( _from, _to, 3)
            #print('move ', move)
            player['position'][0]-=move[0]
            player['position'][1]-=move[1]

        self.mutex.release()
        return

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

    def move(self, _from, to, speed):
        vector = [_from[0]- to[0], _from[1]-to[1]]
        vector = self.normalize(vector)
        #print('normalize ', vector)
        vector[0] = vector[0]*speed
        vector[1] = vector[1]*speed
        return vector
