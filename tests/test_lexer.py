import pymask.lexer as L
import pytest

def test_conv():
  assert L.int_token('0').value == 0
  assert L.float_token('0.5').value == 0.5
  assert L.bool_token('true').value == True
  assert L.bool_token('false').value == False
  assert L.string_token('"false"').value == 'false'

def test_eq():
  assert L.end_token() == L.end_token()
  assert L.int_token(0) == L.int_token(0)
  assert L.int_token(0) != L.int_token(1)
  assert L.int_token(0) != L.name_token('name')

def test_str():
  assert str(L.int_token) == 'int_token'
  assert str(L.int_token(0)) == 'int_token(0)'

def test_repr():
  assert repr(L.int_token) == '<int_token>'
  assert repr(L.int_token(0)) == '<int_token(0)>'
