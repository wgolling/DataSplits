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
  class AccumulatorCategory:
    def __init__(self, key, label):
      self.key = key
      self.label = label
      self.accumulators = dict()

    def add_accumulator(self, accumulator):
      key = accumulator.key
      if key in self.accumulators:
        # throw some exception because the key's already in use
        pass
      else:
        self.accumulators[key] = accumulator

    def split(self):
      for key in self.accumulators:
        self.accumulators[key].split()

  def __init__(self):
    self.split_number = 0
    self.accumulator_categories = dict()

  def add_accumulator_category(self, key, label):
    if key in self.accumulator_categories:
      #throw exception
      pass
    else:
      self.accumulator_categories[key] = AccumulatorManager.AccumulatorCategory(key, label)

  def parse_compound_key(self, compound_key):
    '''
    Helper method for parsing compound keys.
    '''
    keys = compound_key.split('-')
    # ...
    return keys


  # Methods for adding accumulators.

  def add_general_accumulator(self, compound_key, label, accumulator_constructor):
    keys = self.parse_compound_key(compound_key)
    cat_key = keys[0]
    acc_key = keys[1]
    if cat_key not in self.accumulator_categories:
      self.add_accumulator_category(cat_key, cat_key.title())
    acc = accumulator_constructor(acc_key, label)
    self.accumulator_categories[cat_key].add_accumulator(acc)
    return acc

  def add_accumulator(self, compound_key, label):
    return self.add_general_accumulator(compound_key, label, Accumulator)

  def add_list_accumulator(self, compound_key, label):
    return self.add_general_accumulator(compound_key, label, ListAccumulator)

  def add_current_accumulator(self, compound_key, label):
    return self.add_general_accumulator(compound_key, label, CurrentAccumulator)

  def add_function_accumulator(self, compound_key, label, accumulators, accumulator_function):
    keys = self.parse_compound_key(compound_key)
    cat_key = keys[0]
    acc_key = keys[1]
    if cat_key not in self.accumulator_categories:
      self.add_accumulator_category(cat_key, cat_key.title())    
    acc = FunctionAccumulator(acc_key, label, accumulators, accumulator_function)
    self.accumulator_categories[cat_key].add_accumulator(acc)
    return acc


  # Methods for incrementing accumulators.
  def validate_keys(self, keys):
    return (keys[0] in self.accumulator_categories \
            and keys[1] in self.accumulator_categories[keys[0]].accumulators)

  def gain_amount(self, compound_key, amt):
    keys = self.parse_compound_key(compound_key)
    if not self.validate_keys(keys):
      #throw exception
      pass
    cat_key = keys[0]
    acc_key = keys[1]
    acc = self.accumulator_categories[cat_key].accumulators[acc_key]
    acc.gain_amount(amt)

  def set_current(self, compound_key, amt):
    keys = self.parse_compound_key(compound_key)
    if not self.validate_keys(keys):
      #throw exception
      pass
    cat_key = keys[0]
    acc_key = keys[1]
    acc = self.accumulator_categories[cat_key].accumulators[acc_key]
    if not (type(acc) is CurrentAccumulator):
      #throw exception
      pass
    acc.set_current(amt)

  def split(self):
    cats = self.accumulator_categories
    for cat_key in cats:
      cats[cat_key].split()
    self.split_number += 1
