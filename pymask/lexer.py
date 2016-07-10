#########
# Lexer #
#########

class metatoken(type):
  def __str__(self):
    return self.__name__

  def __repr__(self):
    return '<{}>'.format(self.__name__)

class token(metaclass=metatoken):
  pass

class end_token(token):
  pass

class value_token(token):
  def __init__(self, value):
    self.value = value

  def __eq__(self, other):
    if not isinstance(other, value_token):
      return False

    return self.value == other.value

  def __str__(self):
    return '{}({!r})'.format(type(self), self.value)

  def __repr__(self):
    return '<{}({!r})>'.format(type(self), self.value)

class name_token(value_token):
  pass

class number_token(value_token):
  pass

class symbol_token(value_token):
  pass

#######
# AST #
#######

class metanode(type):
  def method(cls, func):
    setattr(cls, func.__name__, func)
    return func

  def __str__(self):
    return self.__name__

  def __repr__(self):
    return '<{}>'.format(self.__name__)

class node(metaclass=metanode):
  pass

class value_node(node):
  def __init__(self, value):
    self.value = value

  def __eq__(self, other):
    if not isinstance(other, value_token):
      return False

    return self.value == other.value

  def __str__(self):
    return '{}({!r})'.format(type(self), self.value)

  def __repr__(self):
    return '<{}({!r})>'.format(type(self), self.value)

class literal_node(value_node):
  pass

##########
# Parser #
##########

class context:
  def __init__(self, stream):
    self.stream = stream
    self.peek = next(stream)
    self.next()

  def next(self):
    self.token = self.peek
    try:
      self.peek = next(self.stream)
    except StopIteration:
      self.peek = end_token()

class parser:
  def __init__(self):
    pass

  def match(self, ctx):
    raise NotImplementedError('Invalid parser')

class eq(parser):
  def __init__(self, token):
    self.token = token

  def match(self, ctx):
    if ctx.token == self.token:
      ctx.next()
      return self.token
    raise SyntaxError('Found {}, expected {}'.format(ctx.token, self))

  def peek(self, ctx):
    return ctx.token == self.token

  def __str__(self):
    return str(self.token)

class lt(parser):
  def __init__(self, kind):
    self.kind = kind

  def match(self, ctx):
    if isinstance(ctx.token, self.kind):
      ret = ctx.token
      ctx.next()
      return ret
    raise SyntaxError('Found {}, expected {}'.format(type(ctx.token), self))

  def peek(self, ctx):
    return isinstance(ctx.token, self.kind)

  def __str__(self):
    return str(self.kind)

class all(parser):
  def __init__(self, *subs):
    self.subs = subs

  def match(self, ctx):
    return [sub.match(ctx) for sub in self.subs]

  def peek(self, ctx):
    return self.subs[0].peek(ctx)

  def __str__(self):
    return ' '.join(str(x) for x in self.subs)

class aux_any(parser):
  def __init__(self, *subs):
    self.subs = subs

  def match(self, ctx):
    for sub in self.subs:
      if sub.peek(ctx):
        return sub.match(ctx)

    raise SyntaxError('Found {}, expected any of {}'.format(ctx.token, self))

  def peek(self, ctx):
    for sub in self.subs:
      if sub.peek(ctx):
        return True

    return False

  def __str__(self):
    return ' | '.join(str(x) for x in self.subs)

class any(parser):
  def __init__(self, *subs):
    self.subs = subs
    for sub in subs:
      if not isinstance(sub, all):
        raise TypeError('Subparser is not of type `all`: {!r}'.format(sub))

  def match(self, ctx):
    pass

###########
# Testing #
###########

def int_stream():
  i = 0
  while True:
    yield number_token(i)
    i = i % 3

ctx = context(int_stream())

m0 = eq(number_token(0))
m1 = eq(number_token(1))
m2 = eq(number_token(2))

jux = all(m0, m1, m2)
alt = aux_any(m0, m1, m2)
