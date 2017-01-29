#!/usr/bin/env python3

import functools

def decorator(declared_decorator):
	'''
	Create a decorator out of function,	which will be used as wrapper.
	'''

	@functools.wraps(declared_decorator)
	def final_decorator(func=None, **kwargs):
		# This will be exposed to the rest
		# of your application as a decorator

		def decorated(func):
			# This will be exposed to the rest
			# of your application as a decorated
			# function, regardless how it was called
			@functools.wraps(func)
			def wrapper(*a, **kw):
				# This is used when actually executing
				# the function that was decorated
				return declared_decorator(func, a, kw, **kwargs)

			return wrapper

		if func is None:
			# The decorator was called with arguments,
			# rather than a function to decorate
			return decorated
		else:
			# The decorator was called without arguments,
			# so the function should be decorated immediately
			return decorated(func)

	return final_decorator

		
if __name__=='__main__':
	'''
	Do some testing ...
	'''

	@decorator
	def suppress_errors(func, args, kwargs, log_func=None):
		try:
			return func(*args, **kwargs)
		except Exception as e:
			if log_func is not None:
				log_func(str(e))


	@suppress_errors
	def example():
		return non_existing_var

	example() # Doesn't raise any errors

	def print_logger(message):
		print(message)

	@suppress_errors(log_func=print_logger)
	def example():
		return non_existing_var

	example()