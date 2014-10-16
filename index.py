import bottle, calendar, pymongo
from datetime import datetime
from bson.json_util import dumps

app = bottle.Bottle()

client = pymongo.MongoClient()
db = client.live_chat_db

APP_ROOT = './'
DEBUG = True

@app.get('/')
def index():
    return bottle.static_file('index.html', APP_ROOT)


@app.route('/static/<filepath:path>')
def server_static(filepath):
    return bottle.static_file(filepath, root=APP_ROOT + 'static')


@app.post('/login')
def login_user():
    username = bottle.request.json.get('username', '')
    if username == '':
        return {'error': 'Username cannot be empty'}

    if not db.clients.find({'client': username}).count() == 0:
        return {'error': 'Username must be unique'}

    db.clients.insert({'client': username, 'ip': bottle.request.remote_addr})
    notify_clients('User logged in', username, 'login')
    return {'status': 'ok'}


@app.post('/logout')
def logout():
    username = bottle.request.json.get('username', '')
    if username == '':
        return {'error': 'Username cannot be empty'}

    if db.clients.find({'client': username}).count() == 0:
        return {'error': 'Username must be logged in'}

    if db.clients.find({'client': username, 'ip': bottle.request.remote_addr}).count() == 0:
        return {'error': 'Cannot logout other users'}

    db.clients.remove({'client': username})
    db.messages.remove({'client': username})
    notify_clients('User logged out', username, 'logout')

    return {'status': 'ok'}

@app.post('/send')
def send_message():
    notify_clients(bottle.request.json['username'], bottle.request.json['message'])


def notify_clients(user, message, messge_type='msg'):
    db_clients = db.clients.find()
    if db_clients.count() == 0:
        return

    clients = [c['client'] for c in db_clients]
    for c in clients:
        db.messages.insert({
            'client': c,
            'time': calendar.timegm(datetime.utcnow().timetuple()),
            'username': user,
            'message': message,
            'type': 'self' if c == user else messge_type
        })


@app.post('/receive')
def get_messages():
    username = bottle.request.json['username']
    if username == '':
        return {'error': 'Username cannot be empty'}
    if db.clients.find({'client': username}).count() == 0:
        return {'error': 'Username must be logged in'}

    messages = dumps(db.messages.find({'client': username}))
    db.messages.remove({'client': username})
    return messages



if __name__ == '__main__':
    db.messages.remove({})
    db.clients.remove({})
    bottle.run(app, host='localhost', port=8000, reloader=DEBUG)