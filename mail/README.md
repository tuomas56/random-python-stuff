#Mail

A simple mail-like message delivery system.

##Design Goals

* Simple - either send messages or get new messages, nothing else.
* Secure - messages are RSA encrypted, public keys stored on server.
* Primarily Client Side - the server is simply a database - uses RethinkDB for scalability.

##Usage

```
usage: mail.py [-h] [--ip IP] [--port PORT]

optional arguments:
  -h, --help   show this help message and exit
  --ip IP      ip address of database.
  --port PORT  port for database.
```

A config file will be loaded from mail.conf if it exists.
This will then open a REPL.

##REPL Commands

**setup**: Setup the connected database for use with mail.py
**signup** *username* *keyfile*: Create a new user called username, generate a key and save it in keyfile.
**login** *username* *keyfile*: Login with username, and load the key from keyfile.
**send** *user* *body*: Send a message to user, containing body.
**read**: Get all of your mail.
