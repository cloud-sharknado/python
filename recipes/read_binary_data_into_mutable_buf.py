#!/usr/bin/python3
# Reading Binary Data Into a Mutable Buffer

import os.path

def read_into_buffer(filename):
	buf = bytearray(os.path.getsize(filename))
	with open(filename, 'br') as f:
		f.readin(buf)
	return buf


def read_record_into_buffer(filename):
	RECORD_SIZE = 32
	buf = bytearray(RECORD_SIZE)

	with open(filename, 'rb') as f:
		while True:
			n = f.readin(buf)
			if n < RECORD_SIZE:
				break
			# Process record in some way