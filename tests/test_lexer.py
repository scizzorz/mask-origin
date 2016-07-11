import pymask.lexer as L
import pytest

def test_eq():
  assert L.number_token(0) == L.number_token(0)
  assert L.number_token(0) != L.number_token(1)
  assert L.number_token(0) != L.name_token('name')

def test_str():
  assert str(L.number_token) == 'number_token'
  assert str(L.number_token(0)) == 'number_token(0)'

def test_repr():
  assert repr(L.number_token) == '<number_token>'
  assert repr(L.number_token(0)) == '<number_token(0)>'
