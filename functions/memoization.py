#!/usr/bin/env python3

import functools

def memoize(func):
	'''
	Cach the results of the function so it doesn't need to be called
	again, if the same arguments are provided a second time.
	'''

	cache = {}

	@functools.wraps(func)
	def wrapper(*args):
		if args in cache:
			return cache[args]

		print('Calling %s()' % func.__name__)

		result = func(*args)
		cache[args] = result
		return result

	return wrapper

@memoize
def multiply(x, y):
	return x * y

@memoize
def add(x, y):
	return x + y


if __name__=='__main__':
	print(multiply(1, 2))
	print(multiply(3, 5))
	print(multiply(1, 2))
	print(multiply(1, 1))
	print(add(1, 2))
	print(add(3, 4))
	print(add(3, 5))
	print(add(1, 2))