from .lexer import end_token
from .error import MaskError
from .error import MaskSyntaxError

class context:
  def __init__(self, stream, exc=MaskSyntaxError):
    self.stream = stream
    self.exc = exc
    self.peek = next(stream)
    self.next()

  def next(self):
    self.token = self.peek
    try:
      self.peek = next(self.stream)
    except StopIteration:
      self.peek = end_token()

  def panic(self, msg, exc=None):
    if exc is None:
      exc = self.exc

    if MaskError in exc.mro():
      raise exc(msg, self.token)
    else:
      raise exc(msg)


class parser:
  def match(self, ctx):
    ctx.panic('Invalid parser: no `match` method', exc=NotImplementedError)

  def peek(self, ctx):
    ctx.panic('Invalid parser: no `peek` method', exc=NotImplementedError)

class eq(parser):
  def __init__(self, token):
    self.token = token

  def match(self, ctx):
    if ctx.token == self.token:
      ctx.next()
      return self.token
    ctx.panic('Found {}, expected {}'.format(ctx.token, self))

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
    ctx.panic('Found {}, expected {}'.format(type(ctx.token), self))

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

class any(parser):
  def __init__(self, *subs):
    self.subs = subs

  def match(self, ctx):
    for sub in self.subs:
      if sub.peek(ctx):
        return sub.match(ctx)

    ctx.panic('Found {}, expected any of {}'.format(ctx.token, self))

  def peek(self, ctx):
    for sub in self.subs:
      if sub.peek(ctx):
        return True

    return False

  def __str__(self):
    return ' | '.join(str(x) for x in self.subs)

class many(parser):
  def __init__(self, sub):
    self.sub = sub

class star(many):
  def match(self, ctx):
    ret = []
    while self.sub.peek(ctx):
      ret.append(self.sub.match(ctx))

    return ret

  def peek(self, ctx):
    return True

  def __str__(self):
    return '{}*'.format(self.sub)

class plus(many):
  def match(self, ctx):
    ret = [self.sub.match(ctx)]
    while self.sub.peek(ctx):
      ret.append(self.sub.match(ctx))

    return ret

  def peek(self, ctx):
    return self.sub.peek(ctx)

  def __str__(self):
    return '{}+'.format(self.sub)

class opt(many):
  def match(self, ctx):
    if self.sub.peek(ctx):
      return self.sub.match(ctx)

  def peek(self, ctx):
    return True

  def __str__(self):
    return '{}?'.format(self.sub)
