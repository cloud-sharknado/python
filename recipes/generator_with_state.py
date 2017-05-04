#!/usr/bin/python3
# Generator functions with extra state

from collections import deque

class linehistory:
	def __init__(self, lines, histlen=3):
		self.lines = lines
		self.history = deque(maxlen=histlen)

	def __iter__(self):
		for lineno, line in enumerate(self.lines, 1):
			self.history.append((lineno, line))
			yield line

	def clear(self):
		self.history.clear()

if __name__ == '__main__':
	with open('/etc/passwd') as f:
		lines = linehistory(f)

		for line in lines:
			if 'games' in line:
				for lineno, hline in lines.history:
					print('{} : {}'.format(lineno, hline), end='')