import pymask.lexer as L
import pymask.parser as P
import pytest
xfail = pytest.mark.xfail
ni = xfail(raises=NotImplementedError)
syntax = xfail(raises=SyntaxError)

def num_stream(lim=0):
  i = 0
  while lim == 0 or i < lim:
    yield L.number_token(i)
    i += 1

def name_stream(lim=0):
  i = 0
  while lim == 0 or i < lim:
    yield L.name_token('name_' + str(i))
    i += 1

def dual_stream(lim=0, names=1, nums=1):
  a = name_stream()
  b = num_stream()
  i = 0
  while lim == 0 or i < lim:
    for x in range(names):
      yield next(a)

    for x in range(nums):
      yield next(b)

    i += 1


@ni
def test_ni1():
  ctx = P.context(num_stream())
  P.parser().match(ctx)

@ni
def test_ni2():
  ctx = P.context(num_stream())
  P.parser().peek(ctx)

def test_eq():
  ctx = P.context(num_stream(3))
  assert P.eq(L.number_token(0)).match(ctx) == L.number_token(0)
  assert P.eq(L.number_token(1)).match(ctx) == L.number_token(1)
  assert P.eq(L.number_token(2)).match(ctx) == L.number_token(2)

@syntax
def test_eq_err1():
  ctx = P.context(num_stream(3))
  P.eq(L.number_token(1)).match(ctx)

@syntax
def test_eq_err2():
  ctx = P.context(name_stream(3))
  P.eq(L.number_token(0)).match(ctx)


def test_lt():
  ctx = P.context(num_stream(3))
  assert P.lt(L.number_token).match(ctx) == L.number_token(0)
  assert P.lt(L.number_token).match(ctx) == L.number_token(1)
  assert P.lt(L.number_token).match(ctx) == L.number_token(2)

@syntax
def test_lt_err1():
  ctx = P.context(num_stream(3))
  P.lt(L.name_token).match(ctx)

@syntax
def test_lt_err2():
  ctx = P.context(name_stream(3))
  P.eq(L.number_token).match(ctx)


def test_all():
  ctx = P.context(num_stream(6))
  assert P.all(P.eq(L.number_token(0))).match(ctx) == [L.number_token(0)]
  assert P.all(P.eq(L.number_token(1)), P.eq(L.number_token(2))).match(ctx) == [L.number_token(1), L.number_token(2)]
  assert P.all(P.lt(L.number_token), P.lt(L.number_token), P.lt(L.number_token)).match(ctx) == [L.number_token(3), L.number_token(4), L.number_token(5)]

@syntax
def test_all_err1():
  ctx = P.context(num_stream(3))
  P.all(P.lt(L.number_token), P.lt(L.number_token), P.lt(L.name_token)).match(ctx)

def test_any():
  ctx = P.context(num_stream(3))
  assert P.any(P.lt(L.number_token), P.lt(L.name_token)).match(ctx) == L.number_token(0)
  assert P.any(P.eq(L.number_token(1)), P.eq(L.number_token(2))).match(ctx) == L.number_token(1)
  assert P.any(P.eq(L.number_token(1)), P.eq(L.number_token(2))).match(ctx) == L.number_token(2)

  ctx = P.context(name_stream(2))
  assert P.any(P.lt(L.number_token), P.lt(L.name_token)).match(ctx) == L.name_token('name_0')
  assert P.any(P.lt(L.number_token), P.lt(L.name_token)).match(ctx) == L.name_token('name_1')

@syntax
def test_any_err1():
  ctx = P.context(num_stream(3))
  P.any(P.eq(L.number_token(0)), P.eq(L.number_token(1))).match(ctx)
  P.any(P.eq(L.number_token(0)), P.eq(L.number_token(1))).match(ctx)
  P.any(P.eq(L.number_token(0)), P.eq(L.number_token(1))).match(ctx)

def test_opt():
  ctx = P.context(dual_stream(2))
  assert P.opt(P.lt(L.number_token)).match(ctx) == None
  assert P.opt(P.lt(L.name_token)).match(ctx) == L.name_token('name_0')
  assert P.opt(P.lt(L.number_token)).match(ctx) == L.number_token(0)

def test_star():
  ctx = P.context(dual_stream(2, names=2))
  assert P.star(P.lt(L.name_token)).match(ctx) == [L.name_token('name_0'), L.name_token('name_1')]
  assert P.star(P.lt(L.name_token)).match(ctx) == []

def test_plus():
  ctx = P.context(dual_stream(2, names=2))
  assert P.plus(P.lt(L.name_token)).match(ctx) == [L.name_token('name_0'), L.name_token('name_1')]
  assert P.plus(P.lt(L.number_token)).match(ctx) == [L.number_token(0)]

@syntax
def test_plus_err1():
  ctx = P.context(dual_stream(2))
  P.plus(P.lt(L.number_token)).match(ctx)
