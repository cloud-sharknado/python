#!/usr/bin/python3

# A source that mimics Unix 'tail -f'
import time

# A decorator function that takes care of starting a coroutine
# automatically on call.

def coroutine(func):
    def start(*args,**kwargs):
        cr = func(*args,**kwargs)
        next(cr)
        return cr
    return start

def follow(thefile, target):
	thefile.seek(0, 2)
	while True:
		line = thefile.readline()
		if not line:
			time.sleep(0.1)
			continue
		target.send(line)

@coroutine
def printer():
	while True:
		line = (yield)
		print(line, end='')