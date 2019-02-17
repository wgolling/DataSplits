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
    return cls.Entry(total)

  def gain_amount(self, amt):
    self.current_entry.gain_amount(amt)

  def split(self):
    c = self.current_entry
    c.total += c.gain
    self.entries.append(c)
    self.current_entry = self.new_entry(c.total)


class ListAccumulator(Accumulator):
  '''
  Like Accumulator except the Entries also keep lists of the individual gains.
  '''
  class Entry(Accumulator.Entry):
    def __init__(self, total):
      super().__init__(total)
      self.list = []
    
    def gain_amount(self, amt):
        super().gain_amount(amt)
        self.list.append(amt)

  
class FunctionAccumulator(Accumulator):
  '''
  Like Accumulator except its value is determined from the values of other accumulators.
  '''
  def __init__(self, accumulators, acc_function):
    #gotta think about this one. 
    pass
