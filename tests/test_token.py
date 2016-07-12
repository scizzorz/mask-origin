import pymask.token as K
import pytest

def test_conv():
  assert K.int_token('0').value == 0
  assert K.float_token('0.5').value == 0.5
  assert K.bool_token('true').value == True
  assert K.bool_token('false').value == False
  assert K.string_token('"false"').value == 'false'

def test_eq():
  assert K.end_token() == K.end_token()
  assert K.int_token(0) == K.int_token(0)
  assert K.int_token(0) != K.int_token(1)
  assert K.int_token(0) != K.name_token('name')

def test_str():
  assert str(K.end_token()) == 'end_token'
  assert str(K.int_token) == 'int_token'
  assert str(K.int_token(0)) == 'int_token(0)'

def test_repr():
  assert repr(K.end_token()) == '<end_token>'
  assert repr(K.int_token) == '<int_token>'
  assert repr(K.int_token(0)) == '<int_token(0)>'
