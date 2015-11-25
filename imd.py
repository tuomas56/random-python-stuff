from mistune import InlineLexer, InlineGrammar, Renderer, Markdown
import re

class PythonScriptRenderer(Renderer):
	def block_html(self, html):
		return '<script src="brython.js"></script>' + super().block_html(html)

	def python_script(self, code):
		return '<script type="text/python">%s</script>' % code

class PythonScriptLexer(InlineLexer):
	def enable_python_script(self):
		self.rules.python_script = re.compile(r"\%\%(.*)\%\%")
		self.default_rules.insert(1, 'python_script')

	def output_python_script(self, m):
		return self.renderer.python_script(m.group(1))

renderer = PythonScriptRenderer()
inline = PythonScriptLexer(renderer)
inline.enable_python_script()
markdown = Markdown(renderer, inline=inline)

print(markdown("""


###Hello World!

%%alert("Hello")%%

Hello!

"""))
