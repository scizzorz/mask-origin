class metatoken(type):
  def __str__(self):
    return self.__name__

  def __repr__(self):
    return '<{}>'.format(self.__name__)

class token(metaclass=metatoken):
  def __eq__(self, other):
    return type(self) is type(other)

  def __str__(self):
    return str(type(self))

  def __repr__(self):
    return '<{}>'.format(self)

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
    return '<{}>'.format(self)

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
