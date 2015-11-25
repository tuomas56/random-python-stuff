from bottle import server_names, ServerAdapter, run, request, Bottle, redirect,response, abort
import markdown
import re
import os
import pickle
import uuid
import scrypt
import base64
from datetime import datetime, timedelta
from cherrypy import wsgiserver
from cherrypy.wsgiserver.ssl_builtin import BuiltinSSLAdapter
from config import SSL_PRIV_KEY, PASS_DB, SALT_DB, HASH_TIME


SCRIPT_RE = re.compile(r"\<script\>(.*?)\<\\script\>")
HASH_TIME = timedelta.strptime("%H:%M:%S")
InvalidUserPass = RuntimeError("Invalid username or password.")

class SSLCherryPy(ServerAdapter):
    def run(self, handler):
        server = wsgiserver.CherryPyWSGIServer((self.host, self.port), handler)
        server.ssl_adapter = BuiltinSSLAdapter(SSL_PRIV_KEY, SSL_PRIV_KEY)
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

app = Bottle()
current_hashes = {}

with open(PASS_DB, "rb") as f:
	pass_db = pickle.load(f)

with open(SALT_DB, "rb") as f:
	salt_db = pickle.load(f)

class HashData:
	def __init__(self, hash, expiry, user):
		self.hash = hash
		self.expiry = expiry
		self.user = user

	def expired(self):
		return self.expiry < datetime.now()

def authenticated(fn):
	def _authenticated(hash, *args, **kwargs):
		if hash in current_hashes:
			if not current_hashes[hash].expired():
				return fn(current_hashes[hash], *args, **kwargs)
			else:
				del current_hashes[hash]
				redirect('/login/expired')
		else:
			redirect('/login/expired')
	return _authenticated

def action_login(user, passwd):
	if user not in pass_db or pass_db[user] != passwd_hash(user, passwd):
		raise InvalidUserPass
	else:
		return generate_hash(user)

def generate_hash(user):
	expiry = datetime.now() + HASH_TIME
	hash = uuid.uuid4()
	return Hash(hash, expiry, user)

def generate_salt():
	return base64.b64encode(os.urandom(16)).decode()

def passwd_hash(user, passwd):
	return salt_db[user] + scrypt.hash(passwd, salt_db[user], mintime=0.1)

@app.route("/do/login/<user>/<passwd>")
@enable_cors
def do_login(user, passwd):
	try:
		current_hashes[user] = action_login(user, passwd)
		redirect('/home/%s' % current_hashes[user])
	except RuntimeError:
		redirect('/login/invalid')

@app.route("/login/<error>")
def login(error):
	return template('pages/login.html.tpl', error=login_error(error))

def login_error(error):
	if error = 'invalid':
		return 'Invalid username or password.'
	elif error = 'expired':
		return 'Hash has expired; please login.'
	elif error = 'none':
		return ''
	else:
		raise RuntimeError("No such login error.")

class Article:
	def __init__(self, author, date_written, tags, text):
		self.author = author
		self.date_written = date_written
		self.tags = tags
		self.text = text

class Comment:
	def __init__(self, author, date_posted, parent, article, text):
		self.author = author
		self.date_posted = date_posted
		self.parent = parent
		self.article = article
		self.text = text

def process_article(text):
	lines = text.split("\n")
	author, date_written, tags, *lines = lines
	date_written = datetime.strptime(date_written, "%d/%m/%Y %H:%M")
	tags = tags.split(",")
	text = markdown.markdown('\n'.join(lines))
	return Article(author, date_written, tags, text)

def process_comment(author, date_posted, parent, article, text):
	return Comment(author, datetime.strptime(date_written, "%d/%m/%Y %H:%M"),article,SCRIPT_RE.replace(markdown.markdown(text), r"<code>\1</code>"))