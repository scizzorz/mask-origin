class MaskError(Exception):
  def __init__(self, msg, token):
    super().__init__(msg)
    self.token = token

class MaskSyntaxError(MaskError, SyntaxError):
  pass
