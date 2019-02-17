class Accumulator:
  '''
  The Accumulator class accumulates numerical quantities.
  It keeps a list is Entry objects.
  '''
  class Entry:
    '''
    The Entry class keeps track of elementary data.
    '''
    def __init__(self, total):
      self.gain = 0
      self.total = total

    def gain_amount(self, amt):
      self.gain += amt

  def __init__(self, key, label):
    self.key = key
    self.label = label
    self.entries = []
    self.current_entry = self.new_entry()

  @classmethod
  def new_entry(cls, total=0):
    e = cls.Entry(total)
    return e

  def gain_amount(self, amt):
    self.current_entry.gain_amount(amt)

  def split(self):
    self.current_entry.total += self.current_entry.gain
    self.entries.append(self.current_entry)
    self.current_entry = self.new_entry(total)





class ListAccumulator(Accumulator):
  '''
  Like Accumulator except also keeps lists.
  '''
  class Entry(Accumulator.Entry):
    def __init__(self, total):
      super().__init__(total)
      self.list = []

  def gain(self, amt):
    super().gain(amt)
    self.list.append(amt)

#Do we need this one?
class CharacterAccumulator(Accumulator):
  '''
  Like Accumulator except also for characters.
  '''
  def __init__(self):
    pass


class FunctionAccumulator(Accumulator):
  '''
  Like Accumulator except its value is determined from the values of other accumulators.
  '''
  def __init__(self, accumulators, acc_function):
    #gotta think about this one. 
    pass
