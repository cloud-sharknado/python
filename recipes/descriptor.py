#!/usr/bin/python3

# A descriptor is a class that implements the three core attribute access operations (get, set and delete)
# in the form of __get__(), __set__() and __delete__() special methods. These methods work by receiving an 
# instance as input. The underlying dictionary of the instance is then manipulated as appropriate.
class String:
	def __init__(self, name):
		'''
		The self.name attribute of the descriptor holds the dictionary key being used to store the actual
		data in the instance dictionary
		'''
		self.name = name

	def __get__(self, instance, cls):
		if instance is None:
			return self
		return instance.__dict__[self.name]

	def __set__(self, instance, value):
		if not isinstance(value, str):
			raise TypeError('Expected a string')
		instance.__dict__[self.name] = value

class Integer:
	def __init__(self, name):
		self.name = name

	def __get__(self, instance, cls):
		if instance is None:
			return self
		return instance.__get__[self.name]

	def __set__(self, instance, value):
		if not isinstance(value, int):
			raise TypeError('Expected an int')
		instance.__dict__[self.name] = value

	def __delete__(self, instance):
		del instance.__dict__[self.name]

# A class with a descriptor
class Person:
	name = String('name')
	def __init__(self, name):
		self.name = name

class SubPerson(Person):
	@property
	def name(self):
		print('Getting name')
		return super().name

	@property.setter
	def name(self, value):
		print('Setting name to', value)
		super(SubPerson, SubPerson).name.__set__(self, value)

	@property.deleter
	def name(self):
		print('Deleting name')
		super(SubPerson, SubPerson).name.__delete__(self)


if __name__ = '__main__':
	class Point:
		'''
		To use a descriptor, instances of the descriptor are placed into a class definition as class variable.
		'''
		x = Integer('x')
		y = Integer('y')

		def __init__(self, x, y):
			self.x = x
			self.y = y