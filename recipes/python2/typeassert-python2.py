#!/usr/bin/python
from __future__ import print_function
from functools import wraps
from inspect import getargspec
from types import ListType

def typeassert(*ty_args, **ty_kwargs):
	def decorate(func):
		signature = getargspec(func)
		bound_types = dict()
		bound_types.update(zip(signature.args, ty_args))
		bound_types.update(ty_kwargs)

		@wraps(func)
		def wrapper(*args, **kwargs):
			# Magic goes here
			# Create mapping of parameters and arguments
			bound_values = dict()
			if signature.defaults:
				bound_values.update(zip(signature.args[:-len(signature.defaults)], signature.defaults))
			bound_values.update(zip(signature.args, args))
			bound_values.update(kwargs)
			for name, value in bound_values.items():
				if name in bound_types:
					if not isinstance(value, bound_types[name]):
						raise TypeError(
							'Argument {} must be {}'.format(name, bound_types[name])
							)
			return func(*args, **kwargs)
		return wrapper
	return decorate

if __name__ == "__main__":
	import unittest

	@typeassert(int, int, default=float, debug=bool, comment=str)
	def foo(a, b, c, default=0.1, debug=False, comment='Test'):
		return (a, b, c, default, debug, comment)

	@typeassert(y=int, z=int)
	def spam(x, y, z=42):
		return (x, y, z)

	class TestTypeAssertDecorator(unittest.TestCase):
		def test_foo_1(self):
			self.assertEqual(foo(1, 2, 'bla', default=0.1, debug=True, comment='First Test'), (1, 2, 'bla', 0.1, True, 'First Test'))

		def test_foo_2(self):
			self.assertEqual(foo(1, 2, 3, debug=False), (1, 2, 3, 0.1, False, 'Test'))

		def test_foo_3(self):
			self.assertEqual(foo(1, 2, 3, comment='out of order', debug=True, default=0.2), (1, 2, 3, 0.2, True, 'out of order'))

		def test_foo_4(self):
			self.assertEqual(foo(1, 2, 3, 0.9, False), (1, 2, 3, 0.9, False, 'Test'))

		def test_foo_5(self):
			with self.assertRaises(TypeError):
				foo('1', 2, 'bla', default=0.1, debug=True, comment='TypeError Test')

		def test_foo_6(self):
			with self.assertRaises(TypeError):
				foo(1, 2, 'bla', debug='True', comment='TypeError Test')

		def test_spam_1(self):
			self.assertEqual(spam('a', 1, 3), ('a', 1, 3))

		def test_spam_2(self):
			self.assertEqual(spam('a', 1, z=1), ('a', 1, 1))

		def test_spam_3(self):
			self.assertEqual(spam(z=2, x='1', y=1), ('1', 1, 2))

		def test_spam_4(self):
			with self.assertRaises(TypeError):
				spam(z='True', x=1, y=2)


	unittest.main()