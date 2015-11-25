from mistune import InlineLexer, InlineGrammar, Renderer

class PythonScriptRenderer(Renderer):
	def python_script(self, code):
		return '<script type="text/python">%s</script>' % code