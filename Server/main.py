from threading import Thread, Lock
import time
from world import World

import eventlet
import socketio
eventlet.monkey_patch()

from pprint import pprint

world = World()

sio = socketio.Server()
app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'index.html'}
})

@sio.event
def connect(sid, environ):
    print('connect ', sid)
    world.addPlayer(sid)
    for i in range(15):
        world.addPlayer(chr(i))

@sio.on('update_start')
def update_start(sid, data):
    world.updatePlayerWithSid(sid, data)
    return

@sio.event
def disconnect(sid):
    print('disconnect ', sid)
    world.removePlayer(sid)

def gameloop():
    while True:
        world.updateState()
        print('emitting', len(world.players))
        if len(world.players):
            pprint(world.players)
            for sid in world.players:
               sio.emit('state_changed', world.generateStateForSid(sid), room=sid)
        time.sleep(1/60)

if __name__== '__main__':
    t = Thread(target=gameloop)
    t.start()
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 27002)), app)



















#
