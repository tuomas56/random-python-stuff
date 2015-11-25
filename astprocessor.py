from ast import *
from astpp import dump
from meta import dump_python_source


class RewriteOps(NodeTransformer):
     _names = {Add: '__add__', Sub: '__sub__', Mult: '__mul__', Div: '__truediv__', FloorDiv: '__floordiv__', Mod: '__mod__', Pow: '__pow__'}

     def visit_BinOp(self, node):
         name = self._names.get(node.op.__class__, None)
         if name is not None:
            return copy_location(Call(func=Attribute(value=node.left, attr=name, ctx=Load()),args=[node.right], keywords=[], starargs=[], kwargs=[]),node)
         else:
            self.generic_visit(node)

source = '"Hello " + "World!"'
print(source,'\n')

node = parse(source)
print(dump(node),'\n')

node = RewriteOps().visit(node)
print(dump(node))

source2 = dump_python_source(node)
print(source2)

print(eval(source))
print(eval(source2))