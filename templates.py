class Text: __init__ = lambda self, value: setattr(self, '_value', "\"\"\""+'}'.join('{'.join(value.split('\{')).split('\}'))+"\"\"\"")
class parent: __init__ = lambda self, value: setattr(self, '_value', value[2:-2].strip())
Interpolation, Directive, RE_MAIN = type('Interpolation', (parent,), dict()), type('Directive', (parent,), dict()), __import__('re').compile("(?P<interpolation>\{\{.*?\}\})|(?P<directive>\{%.*%\})|(?P<text>(?:(?!(\{\{|\{%|\}\}|%\}))(\s|.))*)")
def to_nodes(text):
 for match in iter(RE_MAIN.scanner(text).match, None):
  for x in ['directive','interpolation','text']:
   if match.group(x) is not None:
    yield globals()[x[0].upper()+x[1:]](match.group(x))
    break
def render(template, data):
 r, ws, nodes = [], 0, list(to_nodes(template))
 for node in nodes:
  if isinstance(node, (Interpolation, Text)):
   r.append(" "*ws + """yield %s""" % node._value)
  elif isinstance(node, Directive):
   if node._value == 'end': ws -= 1
   else: r.append(" "*(ws-1 if'else:' in node._value or node._value.startswith('elif ') else ws) + node._value)
   if node._value.endswith(':'): ws += 1
 code, lcs = """def output():\n %s""" % "\n ".join(r), {'__builtins__':__import__('builtins')}
 return (exec(code, data, lcs),''.join(list(lcs['output']())))[1]