#!/usr/bin/env python3
import inspect

def example(a=1, b=1, *c, d, e=2, **f) -> str:
	pass

def get_arguments(func, args, kwargs):
	'''
	Given a function and a set of arguments, return a dictionary
	of argument values that will be sent to the function.
	'''

	arguments = {}
	spec = inspect.getfullargspec(func)

	if spec.defaults:
		arguments.update(zip(reversed(spec.args), reversed(spec.defaults)))
	if spec.kwonlydefaults:
		arguments.update(spec.kwonlydefaults)
	arguments.update(zip(spec.args, args))
	arguments.update(kwargs)

	return arguments

print(get_arguments(example, (1,), {'f':4}))