from .parser import parser
from .parser import plus
from .parser import eq
from .parser import lt
from .lexer import symbol_token
from .lexer import value_token
from .lexer import name_token
from .lexer import number_token

class metanode(type):
  def method(cls, func):
    setattr(cls, func.__name__, func)
    return func

  def __str__(self):
    return self.__name__

  def __repr__(self):
    return '<{}>'.format(self.__name__)

class node(parser, metaclass=metanode):
  pass

# Mask

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

class decl_node(node):
  pass

@decl_node.method
def match(ctx):
  self = decl_node()
  self.names = plus(lt(name_token)).match(ctx)
  eq(symbol_token(':')).match(ctx)
  self.type = lt(number_token).match(ctx)
  return self

@decl_node.method
def peek(self, ctx):
  return lt(name_token).match(ctx)
