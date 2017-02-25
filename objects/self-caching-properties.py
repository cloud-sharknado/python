#!/usr/bin/env python3

import functools

def cachedproperty(name):
	def decorator(func):
		@property
		@functools.wraps(func)
		def wrapper(self, *args, **kwargs):
			if name not in self.__dict__:
				self.__dict__[name] = func(self, *args, **kwargs)
			return self.__dict__[name]
		return wrapper
	return decorator

if __name__ == '__main__':
	class Example(object):
		@cachedproperty('attr')
		def attr(self):
			print('Getting the value!')
			return 42

	e = Example()
	print('--> calling e.attr first time: %s' % e.attr)
	print('--> calling e.attr second time: %s' % e.attr)