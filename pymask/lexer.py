import re

class metatoken(type):
  def __str__(self):
    return self.__name__

  def __repr__(self):
    return '<{}>'.format(self.__name__)

class token(metaclass=metatoken):
  def __eq__(self, other):
    return type(self) is type(other)

class end_token(token):
  pass

# Mask

class indent_token(token):
  pass

class dedent_token(token):
  pass

class newline_token(token):
  pass

class value_token(token):
  def __init__(self, value):
    self.value = value

  def __eq__(self, other):
    return type(self) is type(other) and self.value == other.value

  def __str__(self):
    return '{}({!r})'.format(type(self), self.value)

  def __repr__(self):
    return '<{}({!r})>'.format(type(self), self.value)

class keyword_token(value_token):
  pass

class name_token(value_token):
  pass

class symbol_token(value_token):
  pass

class operator_token(value_token):
  pass

class int_token(value_token):
  def __init__(self, value):
    super().__init__(int(value))

class float_token(value_token):
  def __init__(self, value):
    super().__init__(float(value))

class bool_token(value_token):
  def __init__(self, value):
    super().__init__(value.lower() == 'true')

class string_token(value_token):
  def __init__(self, value):
    super().__init__(self.unescape(value))

  @staticmethod
  def unescape(data):
    return bytes(data[1:-1].encode('utf-8')).decode('unicode_escape')


# Lexing

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

rules = {
  r'#.*': None,
  r'""|"(.*?[^\\])"': string_token,
  r'(?:0|[1-9][0-9]*)\.[0-9]+': float_token,
  r'0|[1-9][0-9]*': int_token,
  r'true|false': bool_token,
  r'[a-zA-Z_][a-zA-Z0-9_]*': factory,
  '|'.join(re.escape(x) for x in OPERATORS): operator_token,
  r'.': symbol_token,
}

rules = {re.compile(k): v for k,v in rules.items()}


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
      while source and source[0] == '\n':
        skip(1)
        col = 0
        line += 1

      depth = indent.match(source)
      depth_amt = len(depth.group(0))

      if depth_amt > indents[-1]:
        last = indent_token()
        yield last
        indents.append(depth_amt)
      else:
        if not isinstance(last, (type(None), indent_token, newline_token)):
          last = newline_token()
          yield last

      while depth_amt < indents[-1]:
        last = newline_token()
        yield dedent_token()
        yield last
        del indents[-1]

      skip(depth_amt)

      if not source:
        break

    if source[0].isspace():
      skip(1)
      continue

    for rule, kind in rules.items():
      match = rule.match(source)
      if match:
        value = match.group(0)
        skip(len(value))
        last = kind(value)
        yield last
        break

  yield end_token()
