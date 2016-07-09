class metatoken(type):
  def method(cls, func):
    setattr(cls, func.__name__, func)
    return func

  def __str__(self):
    return self.__name__

  def __repr__(self):
    return '<{}>'.format(self.__name__)

class token(metaclass=metatoken):
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

class name(value_token):
  pass

class number(value_token):
  pass


class metanode(type):
  pass

class node(metaclass=metanode):
  pass

class context:
  def __init__(self, stream):
    self.stream = stream
    self.token = next(stream)
    self.peek = next(stream)

  def next(self):
    self.token = self.peek
    self.peek = next(self.stream)


class parser:
  def __init__(self):
    pass

  def match(self, ctx):
    raise NotImplementedError('Invalid parser')

class one(parser):
  def __init__(self, token):
    self.token = token

  def match(self, ctx):
    if ctx.token == self.token:
      ctx.next()
      return True
    raise SyntaxError('Expected {}, found {}'.format(self.token, ctx.token))

class all(parser):
  def __init__(self, *subs):
    self.subs = subs

  def match(self, ctx):
    pass


def int_stream():
  i = 0
  while True:
    yield number(i)
    i += 1

ctx = context(int_stream())
