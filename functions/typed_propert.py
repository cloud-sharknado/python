#!/usr/bin/env python3

class TypedProperty(object):
	'''
	Simple Descriptor class that enforces type checking 
	for any attribute of a class which it is used to represent.

	https://docs.python.org/3.5/howto/descriptor.html
	http://intermediatepythonista.com/classes-and-objects-ii-descriptors
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

class Property(object):
    "Emulate PyProperty_Type() in Objects/descrobject.c"

    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        if doc is None and fget is not None:
            doc = fget.__doc__
        self.__doc__ = doc

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        if self.fget is None:
            raise AttributeError("unreadable attribute")
        return self.fget(obj)

    def __set__(self, obj, value):
        if self.fset is None:
            raise AttributeError("can't set attribute")
        self.fset(obj, value)

    def __delete__(self, obj):
        if self.fdel is None:
            raise AttributeError("can't delete attribute")
        self.fdel(obj)

    def getter(self, fget):
        return type(self)(fget, self.fset, self.fdel, self.__doc__)

    def setter(self, fset):
        return type(self)(self.fget, fset, self.fdel, self.__doc__)

    def deleter(self, fdel):
        return type(self)(self.fget, self.fset, fdel, self.__doc__)

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