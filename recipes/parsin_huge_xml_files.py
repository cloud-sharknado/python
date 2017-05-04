#!/usr/bin/python3
# Parsing Huge XML Files Incrementally

from xml.etree.ElementTree import iterparse

def parse_and_remove(filename, path):
	path_parts = path.split('/')
	doc = iterparse(filename, ('start', 'end'))
	# Skip the root element
	next(doc)

	tag_stack = []
	elem_stack = []
	for event, elem in doc:
		if event == 'start':
			tag_stack.append(elem.tag)
			elem_stack.append(elem)
		elif event == 'end':
			if tag_stack == path_parts:
				yield elem
				elem_stack[-2].remove(elem)
			try:
				tag_stack.pop()
				elem_stack.pop()
			except IndexError:
				pass

if __name__ == '__main__':
	from collections import Counter
	import os.path

	potholes_by_zip = Counter()
	sample_file = os.path.join(os.path.expanduser('~'), 'scripts/python/sample_files', 'sample_xml.xml')


	data = parse_and_remove(sample_file, 'row/row')
	for pothole in data:
		potholes_by_zip[pothole.findtext('zip')] += 1

	for zipcode, num in potholes_by_zip.most_common():
		print(zipcode, num)
