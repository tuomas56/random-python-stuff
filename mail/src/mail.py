import argparse
import rethinkdb as r
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA
from Crypto.Signature import PKCS1_v1_5
import cmd
import readline
import sys
import os.path
import time

NAME = "mail"
VERSION = "0.0.1"
USERTABLE = "users"
KEYLEN = 2048

class MailShell(cmd.Cmd):
	def __init__(self, ip, port, conn):
		self.ip, self.port, self.conn = ip, port, conn
		self.intro = "[%s cli - v%s] [connected to %s:%s]" % (NAME, VERSION, ip, port)
		self.prompt = "[%s:%s] " % (ip, port)
		self.is_logged_in = False
		self.key = None
		self.username = None
		super().__init__()

	def do_setup(self, arg):
		"""Setup the database to be used with mail."""
		r.db_create(NAME).run(self.conn)
		r.db(NAME).table_create(USERTABLE).run(self.conn)
		print("Setup successful for %s:%s" % (self.ip, self.port))

	def do_login(self, arg):
		"""Set <username> and load your RSA <key>."""
		username, keyfile = arg.split()
		with open(keyfile, 'rb') as f:
			key = RSA.importKey(f.read())
		userpubkey = next(r.db(NAME).table(USERTABLE).filter(r.row['username'] == username).pluck('pubkey').run(self.conn)).get('pubkey')
		if userpubkey == key.publickey().exportKey('PEM'):
			self.username = username
			self.key = key
		else:
			print('Error, invalid key.')

	def do_signup(self, arg):
		"""Create new user with <username> and save the key to <file>."""
		username, keyfile = arg.split()
		key = RSA.generate(KEYLEN)
		with open(keyfile, 'wb') as f:
			f.write(key.exportKey('PEM'))
		r.db(NAME).table(USERTABLE).insert({
			"username": username,
			"messages": [],
			"pubkey": key.publickey().exportKey('PEM')
		}).run(self.conn)

	def do_send(self, arg):
		"""Send a message to <user> with <message>."""
		to, *body = arg.split()
		body = ' '.join(body).encode()
		keystring = next(r.db(NAME).table(USERTABLE).filter(r.row['username'] == to).pluck('pubkey').run(self.conn)).get('pubkey')
		pubkey = RSA.importKey(keystring)
		cipher = PKCS1_OAEP.new(pubkey)
		h = SHA.new(body)
		signer = PKCS1_v1_5.new(self.key)
		signature = signer.sign(h)
		enc_data = cipher.encrypt(body)
		r.db(NAME).table(USERTABLE).filter(r.row['username'] == to).update({"messages": r.row['messages'].append({
			"from": self.username,
			"body": enc_data,
			"signature": signature,
			"time": time.time()
		})}).run(self.conn)
		print("Message sent at %s." % time.asctime())

	def do_read(self, arg):
		"""Read all your messages."""
		messages = next(r.db(NAME).table(USERTABLE).filter(r.row['username'] == self.username).pluck('messages').run(self.conn)).get('messages')
		for message in messages:
			print("From: %s" % message['from'])
			print("Sent at: %s" % time.asctime(time.gmtime(message['time'])))
			cipher = PKCS1_OAEP.new(self.key)
			plaintext = cipher.decrypt(message['body'])
			print("Body: %s" % plaintext.decode())
			h = SHA.new(plaintext)
			pubkey = next(r.db(NAME).table(USERTABLE).filter(r.row['username'] == message['from']).pluck('pubkey').run(self.conn)).get('pubkey')
			verifier = PKCS1_v1_5.new(RSA.importKey(pubkey))
			if verifier.verify(h, message['signature']):
				print("Message Authenticated.\n")
			else:
				print("Message NOT Authenticated.\n")

	def do_quit(self, arg):
		return True


def main(*args):
	if os.path.exists('%s.conf' % NAME):
		args = ('@%s.conf' % NAME,) + args
	parser = argparse.ArgumentParser(fromfile_prefix_chars="@")
	parser.add_argument("--ip", help="ip address of database.", default="0.0.0.0")
	parser.add_argument("--port", help="port for database.", type=int, default=28015)
	args = parser.parse_args(args[1:])
	conn = r.connect(args.ip, args.port)
	shell = MailShell(args.ip, args.port, conn)
	shell.cmdloop()
	return 0

if __name__ == "__main__":
	sys.exit(main(*sys.argv))