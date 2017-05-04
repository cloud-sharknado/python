#!/usr/bin/python3
from collections import deque

def search(lines, pattern, history=5):
	previous_lines = deque(maxlen=history)
	for line in lines:
		if pattern in line:
			yield line, previous_lines
		previous_lines.append(line)

# Example use on a file
if __name__ == '__main__':
	with open('/etc/passwd') as f:
		for line, previous in search(f, 'd3ky'):
			for pline in previous:
				print(pline, end='')
			print(line, end='')
			print('-'*20)