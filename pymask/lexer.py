import re
from .token import bool_token
from .token import dedent_token
from .token import end_token
from .token import float_token
from .token import indent_token
from .token import int_token
from .token import keyword_token
from .token import name_token
from .token import newline_token
from .token import operator_token
from .token import string_token
from .token import symbol_token
from collections import OrderedDict

OPERATORS = (
  '->', '<-',
  '<=', '>=', '>', '<', '==', '!=',
  '&', '|', '^', '~',
  '*', '/', '+', '-',
  '$', '%', '.', '@',
)

KW_OPERATORS = (
  'and', 'or', 'xor', 'not',
  'in', 'is', 'to',
)

KEYWORDS = (
  'print', 'import',
  'if', 'else',
  'for', 'while', 'until', 'loop', 'defer', 'block',
  'pass', 'break', 'continue', 'return',
  'struct', 'func', 'type', 'extern',
)

def factory(data):
  if data.lower() in KEYWORDS:
    return keyword_token(data.lower())
  elif data.lower() in KW_OPERATORS:
    return operator_token(data.lower())
  else:
    return name_token(data)

raw = OrderedDict()
raw[r'#.*'] = None
raw[r'""|"(.*?[^\\])"'] = string_token
raw[r'(?:0|[1-9][0-9]*)\.[0-9]+'] = float_token
raw[r'0|[1-9][0-9]*'] = int_token
raw[r'true|false'] = bool_token
raw[r'[a-zA-Z_][a-zA-Z0-9_]*'] = factory
raw['|'.join(re.escape(x) for x in OPERATORS)] = operator_token
raw[r'.'] = symbol_token

rules = OrderedDict()
for k, v in raw.items():
  rules[re.compile(k)] = v

indent = re.compile('^[ ]*')

def mask_stream(source):
  indents = [0]
  line = 1
  col = 0

  def skip(amt):
    nonlocal source, col
    source = source[amt:]
    col += amt

  last = None
  while source:
    if source[0] == '\n':
      # skip repeated newlines
      while source and source[0] == '\n':
        skip(1)
        col = 0
        line += 1

      # get this line's indentation
      depth = indent.match(source)
      depth_amt = len(depth.group(0))

      # skip this line if it was just an indentation
      if source and source[depth_amt] == '\n':
        skip(1)
        col = 0
        line += 1
        continue

      # handle indents
      if depth_amt > indents[-1]:
        last = indent_token()
        yield last
        indents.append(depth_amt)

      # handle newlines at the same indentation
      else:
        if not isinstance(last, (type(None), indent_token, newline_token)):
          last = newline_token()
          yield last

      # handle dedents
      while depth_amt < indents[-1]:
        last = newline_token()
        yield dedent_token()
        yield last
        del indents[-1]

      skip(depth_amt)
      if not source:
        break

    # skip internal whitespace
    if source[0].isspace():
      skip(1)
      continue

    # tokenize
    for rule, kind in rules.items():
      match = rule.match(source)
      if match:
        value = match.group(0)
        skip(len(value))
        if kind:
          last = kind(value)
          yield last
        break

  yield end_token()
