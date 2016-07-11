import pymask.lexer as L
import pymask.parser as P
import pytest
xfail = pytest.mark.xfail

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

def test_eq():
  ctx = P.context(num_stream(3))
  assert P.eq(L.number_token(0)).match(ctx) == L.number_token(0)
  assert P.eq(L.number_token(1)).match(ctx) == L.number_token(1)
  assert P.eq(L.number_token(2)).match(ctx) == L.number_token(2)

@xfail(raises=SyntaxError)
def test_eq_err1():
  ctx = P.context(num_stream(3))
  P.eq(L.number_token(1)).match(ctx)

@xfail(raises=SyntaxError)
def test_eq_err2():
  ctx = P.context(name_stream(3))
  P.eq(L.number_token(0)).match(ctx)


def test_lt():
  ctx = P.context(num_stream(3))
  assert P.lt(L.number_token).match(ctx) == L.number_token(0)
  assert P.lt(L.number_token).match(ctx) == L.number_token(1)
  assert P.lt(L.number_token).match(ctx) == L.number_token(2)

@xfail(raises=SyntaxError)
def test_lt_err1():
  ctx = P.context(num_stream(3))
  P.lt(L.name_token).match(ctx)

@xfail(raises=SyntaxError)
def test_lt_err2():
  ctx = P.context(name_stream(3))
  P.eq(L.number_token).match(ctx)


def test_all():
  ctx = P.context(num_stream(6))
  assert P.all(P.eq(L.number_token(0))).match(ctx) == [L.number_token(0)]
  assert P.all(P.eq(L.number_token(1)), P.eq(L.number_token(2))).match(ctx) == [L.number_token(1), L.number_token(2)]
  assert P.all(P.lt(L.number_token), P.lt(L.number_token), P.lt(L.number_token)).match(ctx) == [L.number_token(3), L.number_token(4), L.number_token(5)]

@xfail(raises=SyntaxError)
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
