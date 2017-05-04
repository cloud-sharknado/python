#!/usr/bin/python3
# Reading and Writing Binary Arrays of Structures

from struct import Struct
from tempfile import TemporaryFile

def write_records(records, fmt, f):
	'''
	Write a sequence of tuples to a binary file of structures.
	'''
	record_struct = Struct(fmt)
	for record in records:
		f.write(record_struct.pack(*record))


def read_records(fmt, f):
	'''
	Reading a file incrementally in chunks.
	'''
	record_struct = Struct(fmt)
	chunks = iter(lambda: f.read(record_struct.size), b'')
	return (record_struct.unpack(chunk) for chunk in chunks)


def unpack_records(fmt, data):
	'''
	Read file entirely into a byte string with a single read.
	'''
	record_struct = Struct(fmt)
	return (record_struct.unpack_from(data, offset) for offset in range(0, len(data), record_struct.size))


if __name__ == '__main__':
	from collections import namedtuple

	Record = namedtuple('Record', ['kind', 'x', 'y'])

	print('Write some data using write_records(records, fmt, f)')
	records = [
		(1, 2.3, 4.5),
		(6, 7.8, 9.0),
		(12, 13.4, 56.7)
		]

	with TemporaryFile('w+b') as f:
		write_records(records, '<idd', f)
		print('Done!\n')

		print('Read back data using read_records(fmt, f):')
		f.seek(0)
		records = (Record(*record) for record in read_records('<idd', f))
		for record in records:
			print(record.kind, record.x, record.y)

		print('Read back data using unpack_records(fmt, data):')
		f.seek(0)
		data = f.read()
		records = (Record(*record) for record in unpack_records('<idd', data))
		for record in records:
			print(record.kind, record.x, record.y)
		print('Done\n')