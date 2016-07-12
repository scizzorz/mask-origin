import pymask.token as K
import pymask.parser as P
import pytest
xfail = pytest.mark.xfail
ni = xfail(raises=NotImplementedError)
syntax = xfail(raises=SyntaxError)

def int_stream(lim=0):
  i = 0
  while lim == 0 or i < lim:
    yield K.int_token(i)
    i += 1

def name_stream(lim=0):
  i = 0
  while lim == 0 or i < lim:
    yield K.name_token('name_' + str(i))
    i += 1

def dual_stream(lim=0, names=1, nums=1):
  a = name_stream()
  b = int_stream()
  i = 0
  while lim == 0 or i < lim:
    for x in range(names):
      yield next(a)

    for x in range(nums):
      yield next(b)

    i += 1


@ni
def test_ni1():
  ctx = P.context(int_stream())
  P.parser().match(ctx)

@ni
def test_ni2():
  ctx = P.context(int_stream())
  P.parser().peek(ctx)

def test_eq():
  ctx = P.context(int_stream(3))
  assert str(P.eq(K.int_token(0))) == 'int_token(0)'

  assert P.eq(K.int_token(0)).peek(ctx)
  assert not P.eq(K.int_token(1)).peek(ctx)

  assert P.eq(K.int_token(0)).match(ctx) == K.int_token(0)
  assert P.eq(K.int_token(1)).match(ctx) == K.int_token(1)
  assert P.eq(K.int_token(2)).match(ctx) == K.int_token(2)

@syntax
def test_eq_err1():
  ctx = P.context(int_stream(3))
  P.eq(K.int_token(1)).match(ctx)

@syntax
def test_eq_err2():
  ctx = P.context(name_stream(3))
  P.eq(K.int_token(0)).match(ctx)


def test_lt():
  ctx = P.context(int_stream(3))
  assert str(P.lt(K.int_token)) == 'int_token'

  assert P.lt(K.int_token).peek(ctx)
  assert not P.lt(K.name_token).peek(ctx)

  assert P.lt(K.int_token).match(ctx) == K.int_token(0)
  assert P.lt(K.int_token).match(ctx) == K.int_token(1)
  assert P.lt(K.int_token).match(ctx) == K.int_token(2)

@syntax
def test_lt_err1():
  ctx = P.context(int_stream(3))
  P.lt(K.name_token).match(ctx)

@syntax
def test_lt_err2():
  ctx = P.context(name_stream(3))
  P.eq(K.int_token).match(ctx)


def test_all():
  ctx = P.context(int_stream(6))
  assert str(P.all(P.lt(K.int_token), P.lt(K.name_token))) == 'int_token name_token'

  assert P.all(P.eq(K.int_token(0))).peek(ctx)
  assert P.all(P.eq(K.int_token(0)), P.eq(K.int_token(1))).peek(ctx)

  assert P.all(P.eq(K.int_token(0))).match(ctx) == [K.int_token(0)]
  assert P.all(P.eq(K.int_token(1)), P.eq(K.int_token(2))).match(ctx) == [K.int_token(1), K.int_token(2)]
  assert P.all(P.lt(K.int_token), P.lt(K.int_token), P.lt(K.int_token)).match(ctx) == [K.int_token(3), K.int_token(4), K.int_token(5)]

@syntax
def test_all_err1():
  ctx = P.context(int_stream(3))
  P.all(P.lt(K.int_token), P.lt(K.int_token), P.lt(K.name_token)).match(ctx)

def test_any():
  ctx = P.context(int_stream(3))
  assert str(P.any(P.lt(K.int_token), P.lt(K.name_token))) == 'int_token | name_token'

  assert P.any(P.lt(K.int_token), P.lt(K.name_token)).peek(ctx)
  assert P.any(P.lt(K.name_token), P.lt(K.int_token)).peek(ctx)
  assert not P.any(P.lt(K.symbol_token)).peek(ctx)

  assert P.any(P.lt(K.int_token), P.lt(K.name_token)).match(ctx) == K.int_token(0)
  assert P.any(P.eq(K.int_token(1)), P.eq(K.int_token(2))).match(ctx) == K.int_token(1)
  assert P.any(P.eq(K.int_token(1)), P.eq(K.int_token(2))).match(ctx) == K.int_token(2)

  ctx = P.context(name_stream(2))
  assert P.any(P.lt(K.int_token), P.lt(K.name_token)).match(ctx) == K.name_token('name_0')
  assert P.any(P.lt(K.int_token), P.lt(K.name_token)).match(ctx) == K.name_token('name_1')

@syntax
def test_any_err1():
  ctx = P.context(int_stream(3))
  P.any(P.eq(K.int_token(0)), P.eq(K.int_token(1))).match(ctx)
  P.any(P.eq(K.int_token(0)), P.eq(K.int_token(1))).match(ctx)
  P.any(P.eq(K.int_token(0)), P.eq(K.int_token(1))).match(ctx)

def test_opt():
  ctx = P.context(dual_stream(2))
  assert str(P.opt(P.lt(K.int_token))) == 'int_token?'

  assert P.opt(P.lt(K.int_token)).peek(ctx)
  assert P.opt(P.lt(K.name_token)).peek(ctx)

  assert P.opt(P.lt(K.int_token)).match(ctx) == None
  assert P.opt(P.lt(K.name_token)).match(ctx) == K.name_token('name_0')
  assert P.opt(P.lt(K.int_token)).match(ctx) == K.int_token(0)

def test_star():
  ctx = P.context(dual_stream(2, names=2))
  assert str(P.star(P.lt(K.int_token))) == 'int_token*'

  assert P.star(P.lt(K.int_token)).peek(ctx)
  assert P.star(P.lt(K.name_token)).peek(ctx)

  assert P.star(P.lt(K.name_token)).match(ctx) == [K.name_token('name_0'), K.name_token('name_1')]
  assert P.star(P.lt(K.name_token)).match(ctx) == []

def test_plus():
  ctx = P.context(dual_stream(2, names=2))
  assert str(P.plus(P.lt(K.int_token))) == 'int_token+'

  assert P.plus(P.lt(K.name_token)).peek(ctx)
  assert not P.plus(P.lt(K.int_token)).peek(ctx)

  assert P.plus(P.lt(K.name_token)).match(ctx) == [K.name_token('name_0'), K.name_token('name_1')]
  assert P.plus(P.lt(K.int_token)).match(ctx) == [K.int_token(0)]

@syntax
def test_plus_err1():
  ctx = P.context(dual_stream(2))
  P.plus(P.lt(K.int_token)).match(ctx)
