import pymask.lexer as L
import pytest

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
  ctx = L.context(num_stream(5))
  assert L.eq(L.number_token(0)).match(ctx) == L.number_token(0)
  assert L.eq(L.number_token(1)).match(ctx) == L.number_token(0)
