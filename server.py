import eventlet
import socketio

sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)


def get_device_id(environ):
    return environ.get('HTTP_DEVICE_ID', None)


@sio.event
def connect(sid, environ):
    device_id = get_device_id(environ) or sid
    sio.save_session(sid, {'device_id': device_id})
    print('{} is connected'.format(device_id))


@sio.event
def my_message(sid, data):
    session = sio.get_session(sid)
    sio.emit('my_message', data, broadcast=True)
    print('Received data from {}: {}'.format(session['device_id'], data))


@sio.event
def disconnect(sid):
    print('disconnect ', sid)


if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
