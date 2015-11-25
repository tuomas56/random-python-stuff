import json

def classloads(s):
	o = json.loads(s)
	x = _Empty()
	x.__class__ = globals()[o['class']]
	x.__dict__ = o['dict']
	return x

def classdumps(o):
	return json.dumps({'class':o.__class__.__name__,'dict':o.__dict__})

class _Empty: pass