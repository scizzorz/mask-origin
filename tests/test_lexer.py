import pymask.lexer as L
import pymask.token as K
import pytest

def test_factory():
  assert L.factory('print') == K.keyword_token('print')
  assert L.factory('this') == K.name_token('this')
  assert L.factory('and') == K.operator_token('and')
