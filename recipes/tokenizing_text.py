#!/usr/bin/python3

import re
from collections import namedtuple

text = 'foo = 23 + 42 * 10'

NAME = r'(?P<NAME>[a-zA-Z_][a-zA-Z_0-9]*)'
NUM = r'(?P<NUM>\d+)'
PLUS = r'(?P<PLUS>\+)'
TIMES = r'(?P<TIMES>\*)'
EQ = r'(?P<EQ>=)'
WS = r'(?P<WS>\s+)'

master_pat = re.compile('|'.join([NAME, NUM, PLUS, TIMES, EQ, WS]))

Token = namedtuple('Token', ['type', 'value'])

def generate_tokens(pat, text):
	scanner = pat.scanner(text)
	for m in iter(scanner.match, None):
		yield Token(m.lastgroup, m.group())

for tok in generate_tokens(master_pat, text):
	print(tok)

print()
print('New Run'.center(20, '*'))
print()

tokens = (tok for tok in generate_tokens(master_pat, text) if tok.type != 'WS')

for tok in tokens:
	print(tok)