#!/usr/bin/python3

# Implementing the visitor pattern without recursion

import types
from pprint import pprint

class Node:
	pass

class UnaryOperator(Node):
	def __init__(self, operand):
		self.operand = operand

class BinaryOperator(Node):
	def __init__(self, left, right):
		self.left = left
		self.right = right

class Add(BinaryOperator):
	pass

class Sub(BinaryOperator):
	pass

class Mul(BinaryOperator):
	pass

class Div(BinaryOperator):
	pass

class Negate(UnaryOperator):
	pass

class Number(Node):
	def __init__(self, value):
		self.value =value

class NodeVisitor:
	def visite(self, node):
		stack = [ node ]
		last_result = None
		print('Start visit({})'.format(type(node).__name__))
		pprint(locals())
		while stack:
			try:
				last = stack[-1]
				if isinstance(last, types.GeneratorType):
					stack.append(last.send(last_result))
					last_result = None
					print('GeneratorType')
					pprint(locals())
				elif isinstance(last, Node):
					stack.append(self._visit(stack.pop()))
					print('Node')
					pprint(locals())
				else:
					last_result = stack.pop()
					print('Value')
					pprint(locals())
			except StopIteration:
				stack.pop()
				print('StopIteration')
				pprint(locals())
		return last_result

	def _visit(self, node):
		methname = 'visit_' + type(node).__name__
		meth = getattr(self, methname, None)
		if meth is None:
			meth = self.generic_visit
		return meth(node)

	def generic_visit(self, node):
		return RuntimeError('No {} method'.format('visit_' + type(node).__name__))

# Simple visitor class that evaluates expression
class Evaluator(NodeVisitor):
	def visit_Number(self, node):
		return node.value

	def visit_Add(self, node):
		yield (yield node.left) + (yield node.right)

	def visit_Sub(self, node):
		yield (yield node.left) - (yield node.right)

	def visit_Mul(self, node):
		yield (yield node.left) * (yield node.right)

	def visit_Div(self, node):
		yield (yield node.left) / (yield node.right)

	def visit_Negate(self, node):
		yield -(yield node.operand)

if __name__ == '__main__':
	# 1 + 2*(3-4) /5
	t1 = Sub(Number(3), Number(4))
	t2 = Mul(Number(2), t1)
	t3 = Div(t2, Number(5))
	t4 = Add(Number(1), t3)

	# Evalaute it
	e = Evaluator()
	print(e.visite(t4))
