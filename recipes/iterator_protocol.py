#!/usr/bin/python3
# Implementig the Iterator Protocol

class Node:
	def __init__(self, value):
		self._value = value
		self._children = []

	def __repr__(self):
		return 'Node({!r})'.format(self._value)

	def add_child(self, node):
		self._children.append(node)

	def __iter__(self):
		return iter(self._children)

	def depth_first(self):
		return DepthFirstIterator(self)

class DepthFirstIterator(object):
	'''
	Depth-first traversal
	'''

	def __init__(self, start_node):
		self._node = start_node	
		self._children_iter = None	# Iterate over children nodes
		self._child_iter = None		# Child iterator

	def __iter__(self):
		return self

	def __next__(self):
		# Return myself if just started; create an iterator for children
		if self._children_iter is None:
			self._children_iter = iter(self._node)
			return self._node

		# If processing a child, return its next item
		elif self._child_iter:
			try:
				nextchild = next(self._child_iter)
				return nextchild
			except StopIteration:
				self._child_iter = None
				return next(self)

		# Advance to the next child and start its iteration
		else:
			self._child_iter = next(self._children_iter).depth_first()
			return next(self)

if __name__ == '__main__':
	root = Node(0)
	child1 = Node(1)
	child2 = Node(2)
	root.add_child(child1)
	root.add_child(child2)
	child1.add_child(Node(3))
	child1.add_child(Node(4))
	child2.add_child(Node(5))

	for ch in root.depth_first():
		print(ch)