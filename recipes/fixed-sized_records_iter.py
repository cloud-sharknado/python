#!/usr/bin/python3
# Iterating over fixed-sized 

from functools import partial
import os.path

RECORD_SIZE = 32
filename = '/home/d3ky/sample_text.txt'

with open(filename, 'rb') as f:
	records = iter(partial(f.read, RECORD_SIZE), b'')
	for record in records:
		# Process record in some way
		print(record.decode('UTF-8'))
