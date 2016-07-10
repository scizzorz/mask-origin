import pymask.lexer as L
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
  ctx = L.context(num_stream(3))
  assert L.eq(L.number_token(0)).match(ctx) == L.number_token(0)
  assert L.eq(L.number_token(1)).match(ctx) == L.number_token(1)
  assert L.eq(L.number_token(2)).match(ctx) == L.number_token(2)

@xfail(raises=SyntaxError)
def test_eq_err1():
  ctx = L.context(num_stream(3))
  L.eq(L.number_token(1)).match(ctx)

@xfail(raises=SyntaxError)
def test_eq_err2():
  ctx = L.context(name_stream(3))
  L.eq(L.number_token(0)).match(ctx)


def test_lt():
  ctx = L.context(num_stream(3))
  assert L.lt(L.number_token).match(ctx) == L.number_token(0)
  assert L.lt(L.number_token).match(ctx) == L.number_token(1)
  assert L.lt(L.number_token).match(ctx) == L.number_token(2)

@xfail(raises=SyntaxError)
def test_lt_err1():
  ctx = L.context(num_stream(3))
  L.lt(L.name_token).match(ctx)

@xfail(raises=SyntaxError)
def test_lt_err2():
  ctx = L.context(name_stream(3))
  L.eq(L.number_token).match(ctx)


def test_all():
  ctx = L.context(num_stream(6))
  assert L.all(L.eq(L.number_token(0))).match(ctx) == [L.number_token(0)]
  assert L.all(L.eq(L.number_token(1)), L.eq(L.number_token(2))).match(ctx) == [L.number_token(1), L.number_token(2)]
  assert L.all(L.lt(L.number_token), L.lt(L.number_token), L.lt(L.number_token)).match(ctx) == [L.number_token(3), L.number_token(4), L.number_token(5)]

@xfail(raises=SyntaxError)
def test_all_err1():
  ctx = L.context(num_stream(3))
  L.all(L.lt(L.number_token), L.lt(L.number_token), L.lt(L.name_token)).match(ctx)

def test_any():
  ctx = L.context(num_stream(3))
  assert L.any(L.lt(L.number_token), L.lt(L.name_token)).match(ctx) == L.number_token(0)
  assert L.any(L.eq(L.number_token(1)), L.eq(L.number_token(2))).match(ctx) == L.number_token(1)
  assert L.any(L.eq(L.number_token(1)), L.eq(L.number_token(2))).match(ctx) == L.number_token(2)

  ctx = L.context(name_stream(2))
  assert L.any(L.lt(L.number_token), L.lt(L.name_token)).match(ctx) == L.name_token('name_0')
  assert L.any(L.lt(L.number_token), L.lt(L.name_token)).match(ctx) == L.name_token('name_1')
