class Result:
  def __init__(self, string_result):
    self.button_returned = None
    self.text_returned = None

    # go through results string and set attributes accordingly
    for data in string_result.split(','):
      data = data.strip()
      key, value = data.split(':')

      # dynamically set attribute of class
      setattr(self, key.replace(' ', '_'), value)