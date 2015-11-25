import sqlite3
from bottle import route, run, debug, request, redirect

@route('/uc')
def todo_list():
	con = sqlite3.connect('todo.db')
	c = con.cursor()
	c.execute("SELECT id, task FROM todo WHERE status LIKE '1'")
	result = c.fetchall()
	for i, (id, task) in enumerate(result):
		yield """(%s) %s <br/> 
				<form action='/del/uc/%s' method='post'>
					<input type='submit' value='Delete'/>
				</form>
				<form action='/edit/uc/%s' method='post'>
					<input type='submit' value='Edit'/>
				</form>
				<form action='/toggle/uc/%s' method='post'>
					<input type='submit' value='Completed'/>
				</form>""" % (i + 1, task, id, id, id)
	yield "<form action='/new/uc' method='post'><input name='task' type='text'/><input type='submit' value='New Todo'/></form>"
	yield "<a href='/uc'>Show uncompleted</a>   <a href='/c'>Show completed</a>   <a href='/all'>Show all</a>"

@route('/c')
def todo_list():
	con = sqlite3.connect('todo.db')
	c = con.cursor()
	c.execute("SELECT id, task FROM todo WHERE status LIKE '0'")
	result = c.fetchall()
	for i, (id, task) in enumerate(result):
		yield """(%s) %s <br/>
				<form action='/del/c/%s' method='post'>
					<input type='submit' value='Delete'/>
				</form>
				<form action='/edit/c/%s' method='post'>
					<input type='submit' value='Edit'/>
				</form>
				<form action='/toggle/c/%s' method='post'>
					<input type='submit' value='Not completed'/>
				</form>""" % (i + 1, task, id, id, id)
	yield "<form action='/new/c' method='post'><input name='task' type='text'/><input type='submit' value='New Todo'/></form>"
	yield "<a href='/uc'>Show uncompleted</a>   <a href='/c'>Show completed</a>   <a href='/all'>Show all</a>"


@route('/todo')
@route('/')
@route('/all')
def todo_list():
	con = sqlite3.connect('todo.db')
	c = con.cursor()
	c.execute("SELECT id, task, status FROM todo")
	result = c.fetchall()
	for i, (id, task, status) in enumerate(result):
		name = 'Completed' if status == 1 else 'Not completed' 
		yield """(%s) %s <br/> 
				<form action='/del/all/%s' method='post'>
					<input type='submit' value='Delete'/>
				</form>
				<form action='/edit/all/%s' method='post'>
					<input type='submit' value='Edit'/>
				</form>
				<form action='/toggle/all/%s' method='post'>
					<input type='submit' value='%s'/>
				</form>""" % (i + 1, task, id, id, id, name)
	yield "<form action='/new/all' method='post'><input name='task' type='text'/><input type='submit' value='New Todo'/></form>"
	yield "<a href='/uc'>Show uncompleted</a>   <a href='/c'>Show completed</a>   <a href='/all'>Show all</a>"

@route('/new/<prev>')
def new_todo(prev):
	con = sqlite3.connect('todo.db')
	c = con.cursor()
	new = request.GET.get('task','').strip()
	c.execute("INSERT INTO todo (task,status) VALUES (?,?)", (new,1))
	con.commit()
	c.close()
	redirect('/%s' % prev)

@route('/del/<prev>/<del_id>')
def del_todo(prev,del_id):
	con = sqlite3.connect('todo.db')
	c = con.cursor()
	c.execute("DELETE FROM todo WHERE id=?", (del_id,))
	con.commit()
	c.close()
	redirect('/%s' % prev)

@route('/edit/<prev>/<edit_id>')
def edit_todo(prev,edit_id):
	con = sqlite3.connect('todo.db')
	c = con.cursor()
	if prev == "c":
		c.execute("SELECT id, task FROM todo WHERE status LIKE '0'")
	elif prev == "uc":
		c.execute("SELECT id, task FROM todo WHERE status LIKE '1'")
	else:
		c.execute("SELECT id, task FROM todo")
	result = c.fetchall()
	for i, (id, task) in enumerate(result):
		if id == int(edit_id):
			yield """<form action='/save/%s/%s' method='post'>(%s)
						<input type='text' name='value' value='%s'/>
						<input type='submit' value='Save'/>
					</form> <br/> 
					<form action='/del/%s/%s' method='post'>
						<input type='submit' value='Delete'/>
					</form>""" % (prev,id, i+1, task, prev, id)
		else:
			yield "(%s) %s<br/> <form action='/del/%s/%s' method='post'><input type='submit' value='Delete'/></form>" % (i + 1, task, prev, id)
	yield "<form action='/new/%s' method='post'><input name='task' type='text'/><input type='submit' value='New Todo'/></form>" % prev
	con.commit()
	c.close()

@route('/save/<prev>/<save_id>')
def save_todo(prev,save_id):
	con = sqlite3.connect('todo.db')
	c = con.cursor()
	c.execute("UPDATE todo SET task=? WHERE id=?", (request.POST.get('value',''),save_id))
	con.commit()
	c.close()
	redirect('/%s' % prev)

@route('/toggle/<prev>/<todo_id>')
def toggle_status_todo(prev, todo_id):
	con = sqlite3.connect('todo.db')
	c = con.cursor()
	c.execute("SELECT status FROM todo WHERE id=?",(todo_id,))
	status = c.fetchall()[0][0]
	print(status)
	if status == 1:
		status = 0
	else:
		status = 1
	con.commit()
	c.execute("UPDATE todo SET status=? WHERE id=?", (status, todo_id))
	con.commit()
	c.close()
	redirect("/%s" % prev)


debug(True)
run(reloader=True)
