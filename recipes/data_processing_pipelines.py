#!/usr/bin/python3
# Create Data Processing Pipelines using chain of generator functions
# This example will process series of access logs 

import os 
import fnmatch
import gzip
import bz2
import re

def gen_find(filepat, top):
	'''
	Find all filenames in a directory tree that match a shell wildcartd pattern
	'''
	for path, dirlist, filelist in os.walk(top):
		for name in fnmatch.filter(filelist, filepat):
			yield os.path.join(path, name)

def gen_opener(filenames):
	'''
	Open a sequence of filenames one at a time producing a file object.
	The file is closed immediateky when proceeding to the next iteration.
	'''
	for filename in filenames:
		if filename.endswith('.gz'):
			f = gzip.open(filename, 'rt', errors='ignore')
		elif filename.endswith('.bz2'):
			f = bz2.open(filename, 'rt', errors='ignore')
		else:
			f = open(filename, 'rt', errors='ignore')
		yield f
		f.close()

def gen_concatenate(iterators):
	'''
	Chain a swquence of iterators together into a single swquence.
	'''
	for it in iterators:
		yield from it

def gen_grep(pattern, lines):
	'''
	Look for a regex pattern in a sequenec of lines
	'''

	pat = re.compile(pattern)
	for line in lines:
		if pat.search(line):
			yield line

if __name__ == '__main__':
	lognames = gen_find('access_log*', '/home/d3ky/Downloads')
	files = gen_opener(lognames)
	lines = gen_concatenate(files)
	p_lines = gen_grep('.*', lines)
	try:
		bytecoulumn = (line.rsplit(None, 1)[1] for line in p_lines)
	except IndexError as e:
		print(line, str(e))
	bytes = (int(x) for x in bytecoulumn if x != '-')
	print('Total', sum(bytes))