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

class value_token(token):
  def __init__(self, value):
    self.value = value

  def __eq__(self, other):
    return type(self) is type(other) and self.value == other.value

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
