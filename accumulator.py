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

  def new_entry(self, total=0):
    return self.Entry(total)

  def append_current_entry(self):
    c = self.current_entry
    self.entries.append(c)
    self.current_entry = self.new_entry(c.total)

  def gain_amount(self, amt):
    self.current_entry.gain_amount(amt)

  def split(self):
    c = self.current_entry
    c.total += c.gain
    self.append_current_entry()


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

  
class CurrentAccumulator(Accumulator):
  '''
  Like Accumulator but keeps track of the current value of something that can fluctuate.
  A CurrentAccumulator's current value is set, and its gain is computed upon split().
  '''
  def set_current(self, amt):
    self.current_entry.total = amt

  def split(self):
    last_current = 0 if not self.entries else self.entries[-1].total
    c = self.current_entry
    c.gain = c.total - last_current
    self.append_current_entry()


class FunctionAccumulator(Accumulator):
  '''
  Like Accumulator except its value is determined from the values of other accumulators.
  Try #1: 
      - the constructor takes a list if accumulators and a lambda function to apply to those accumulators.
      - it is assumed that all of the accumulators in the list get split before self.
  '''
  def __init__(self, key, label, accumulators, acc_function):
    super().__init__(key, label)
    self.accumulators = accumulators
    self.function = acc_function

  def split(self):
    c = self.current_entry
    c.gain = self.function(self.accumulators)
    c.total += c.gain
    self.append_current_entry()




class AccumulatorManager:
  '''
  The controller class for the Accumulator model.
  '''
  def __init__(self):
    self.accumulator_categories = dict()



