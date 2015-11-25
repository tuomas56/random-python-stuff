import bcrypt
from tinydb import TinyDB, where
from tinydb.storages import MemoryStorage, JSONStorage
from tinydb.middlewares import CachingMiddleware
from cherrypy import wsgiserver
from cherrypy.wsgiserver.ssl_builtin import BuiltinSSLAdapter
from bottle import Bottle, run, request, response, server_names, ServerAdapter, abort, error
from datetime import datetime, timedelta
import uuid
import configparser

class SSLCherryPy(ServerAdapter):
    def run(self, handler):
        server = wsgiserver.CherryPyWSGIServer((self.host, self.port), handler)
        server.ssl_adapter = BuiltinSSLAdapter(config['ssl'].get('cert', None), config['ssl'].get('priv_key', None))
        try:
            server.start()
        finally:
            server.stop()

server_names['sslcherrypy'] = SSLCherryPy

def enable_cors(fn):
    def _enable_cors(*args, **kwargs):
        response.headers['Access-Control-Allow-Origin'] = '*'
        
        return fn(*args, **kwargs)

    return _enable_cors


config = configparser.ConfigParser()
config.read('config.ini')

db_pass = TinyDB(config['db'].get('pass_db','pass.json'), storage=JSONStorage)
db_todo = TinyDB(config['db'].get('todo_db','todo.json'), storage=CachingMiddleware(JSONStorage))
db_session = TinyDB(storage=MemoryStorage)

app = Bottle()

@app.post('/login')
@enable_cors
def login():
    user = request.POST.get('user', None)
    password = request.POST.get('pass', None)
    if user is None or password is None:
        abort(422, 'Username and Password fields are required.')
    hashed = dict(enumerate(db_pass.search(where('user') == user))).get(0, {'pass': None}).get('pass').encode('ascii')
    if hashed is None:
        abort(401, 'User does not exist.')
    if bcrypt.hashpw(password.encode('ascii'), hashed) == hashed:
        user_hash = str(uuid.uuid4())
        if db_session.search(where('ip') == request.remote_addr) == []:
            db_session.insert({'ip': request.remote_addr, 'data': (user_hash, datetime.now() + timedelta(minutes=int(config['auth'].get('timeout',30))), user)})
            return {'success': True, 'hash': user_hash}
        else:
            server_hash, timeout, user = dict(enumerate(db_session.search(where('ip') == request.remote_addr))).get(0, {'data': (None, None, None)}).get('data')
            return {'success': True, 'hash': server_hash}
    else:
        abort(401, 'Password incorrect.')

@app.post('/new_user')
@enable_cors
def new_user():
    user = request.POST.get('user', None)
    password = request.POST.get('pass', None)
    if user is None or password is None:
        abort(422, 'Username and Password fields are required.')
    users = db_pass.search(where('user') == user)
    if users != []:
        abort(401, 'User already exists.')
    db_pass.insert({'user': user, 'pass': bcrypt.hashpw(password.encode('ascii'), bcrypt.gensalt()).decode()})
    return {'success': True}

def check_hash():
    user_hash = request.POST.get('hash', None)
    user = request.POST.get('user', None)
    if user_hash is None or user is None:
        abort(422, 'Hash field is required.')
    server_hash, timeout, server_user = dict(enumerate(db_session.search(where('ip') == request.remote_addr & where('user') == user))).get(0, {'data': (None, None, None)}).get('data')
    if datetime.now() >= timeout:
        abort(401, 'Timeout.')
        db_session.remove(where('ip') == request.remote_addr & where('user') == user)
    if server_hash is None:
        abort(401, 'Not authenticated.')
    if server_hash == user_hash:
        return True, user
    
@app.post('/logout')
@enable_cors
def logout():
    success, user = check_hash()
    if success:
        db_session.remove(where('ip') == request.remote_addr) & where('user') == user)
    return {'success': True}


run(app, host=config['server'].get('host','localhost'), port=config['server'].get('port','8080'), server='sslcherrypy')
