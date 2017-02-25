#!/usr/bin/env python3

class TypedProperty(object):
	'''
	Simple Descriptor class that enforces type checking 
	for any attribute of a class which it is used to represent.
	'''
	def __init__(self, name, type, default=None):
		self.name = '_' + name
		self.type = type
		self.default = default if default else type()

	def __get__(self, instance, owner):
		return getattr(instance, self.name, self.default)

	def __set__(self, instance, value):
		if not isinstance(value, self.type):
			raise TypeError('Must be a %s' % self.type)
		setattr(instance, self.name, value)

	def __delete__(self, instance):
		raise AttributeError("Can't delete attribute")

if __name__ == '__main__':
	class Foo(object):
	    name = TypedProperty("name",str) 
	    num = TypedProperty("num",int,42)

	acct = Foo()
	acct.name = 'obi'
	acct.num = 1234
	print(acct.num)
	print(acct.name)
	print('acct.num = "1234"')
	acct.num = '1234'