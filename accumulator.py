import pickle
import os

class Accumulator:
  '''
  The Accumulator class accumulates numerical quantities.
  It keeps a list of Entry objects.
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

  def __init__(self, key, label, initial_value=0):
    self.key = key
    self.label = label
    self.entries = []
    self.current_entry = self.new_entry(initial_value)

  def new_entry(self, total=0):
    return self.Entry(total)

  def gain_amount(self, amt):
    self.current_entry.gain_amount(amt)

  def get_current_value(self):
    c = self.current_entry
    return c.total + c.gain

  # Splitting methods.

  def split(self):
    self.finalize_data()
    self.append_current_entry()

  def finalize_data(self):
    '''
    Prepare the entry to be saved.
    Overwrite in subclasses.
    '''
    c = self.current_entry
    c.total += c.gain

  def append_current_entry(self):
    c = self.current_entry
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


class CharacterAccumulator(Accumulator):
  '''
  Like Accumulator but keeps track of character data.
  Has a bool that indicates if they are in the party.
  '''
  class Entry(Accumulator.Entry):
    def __init__(self, total):
      super().__init__(total)
      self.in_party = False

  def __init__(self, key, label, starting_level):
    super().__init__(key, label, initial_value=starting_level)
    self.in_party = False

  def add_to_party(self):
    self.in_party = True

  def lose_from_party(self):
    self.in_party = False

  def finalize_data(self):
    super().finalize_data()
    c = self.current_entry
    c.in_party = self.in_party
    
  
class CurrentAccumulator(Accumulator):
  '''
  Like Accumulator but keeps track of the current value of something that can fluctuate.
  A CurrentAccumulator's current value is set, and its gain is computed upon split().
  '''
  def set_current(self, amt):
    self.current_entry.total = amt

  def get_current(self):
    return self.current_entry.total

  def finalize_data(self):
    last_current = 0 if not self.entries else self.entries[-1].total
    c = self.current_entry
    c.gain = c.total - last_current


## Depricated class, but it was kind of cool so I kept it.
# class FunctionAccumulator(Accumulator):
#   '''
#   Like Accumulator except its value is determined from the values of other accumulators.
#   Try #1: 
#       - the constructor takes a list if accumulators and a lambda function to apply to those accumulators.
#       - it is assumed that all of the accumulators in the list get split before self.
#   Try #2:
#       - the constructor takes a set of keys, and a lambda function whose argument is a dict.
#       - it is assumed that the dict's key set agrees with accumulators, and its values are ints.
#   '''
#   def __init__(self, key, label, accumulators, acc_function):
#     super().__init__(key, label)
#     # Validate the function's signature.
#     test_dict = dict()
#     for key in accumulators:
#       test_dict[key] = 0
#     acc_function(test_dict)
#     # If everything's ok, set fields.
#     self.accumulators = accumulators
#     self.function = acc_function

#   def finalize_data(self):
#     # Convert dict of Accumulators to a dict of values.
#     input_dict = dict()
#     for key in self.accumulators:
#       input_dict[key] = self.accumulators[key].entries[-1].gain
#     c = self.current_entry
#     c.gain = self.function(input_dict)
#     c.total += c.gain


class SumAccumulator(Accumulator):
  '''
  Like Accumulator but forms a sum (with plus or minus coefficients) of other accumulators.
  A SumAccumulator's gain value is computed upon split().
  '''
  def __init__(self, key, label, pos_accumulators, neg_accumulators, initial_value=0):
    super().__init__(key, label, initial_value)
    self.pos_accumulators = pos_accumulators
    self.neg_accumulators = neg_accumulators

  def finalize_data(self):
    total_gain = 0
    for acc in self.pos_accumulators:
      total_gain += acc.entries[-1].gain
    for acc in self.neg_accumulators:
      total_gain -= acc.entries[-1].gain
    c = self.current_entry
    c.gain = total_gain
    c.total += c.gain


class AccumulatorManager:
  '''
  The controller class for the Accumulator model.
  '''
  def __init__(self):
    self.split_number = 0
    self.split_names = list()
    self.accumulator_categories = dict()

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

    def get_accumulator(self, key):
      return self.accumulators[key]

    def split(self):
      for key in self.accumulators:
        self.accumulators[key].split()



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


  # Methods for getting accumulators.
  # Throws KeyError
  def get_accumulator(self, compound_key):
    keys = self.parse_compound_key(compound_key)
    cat_key = keys[0]
    acc_key = keys[1]
    return self.accumulator_categories[cat_key].get_accumulator(acc_key)
    

  # Methods for adding accumulators.

  def add_general_accumulator(self, 
      compound_key, 
      label, 
      initial_value=0,
      **kwargs):
    keys = self.parse_compound_key(compound_key)
    cat_key = keys[0]
    acc_key = keys[1]
    if cat_key not in self.accumulator_categories:
      self.add_accumulator_category(cat_key, cat_key.title())
    if {'accumulators', 'accumulator_function'} <= kwargs.keys():
      acc = FunctionAccumulator(
        acc_key, 
        label, 
        kwargs['accumulators'], 
        kwargs['accumulator_function'] )
    elif {'pos_accumulators', 'neg_accumulators'} <= kwargs.keys():
      acc = SumAccumulator(
        acc_key, 
        label, 
        kwargs['pos_accumulators'], 
        kwargs['neg_accumulators'],
        initial_value )
    elif 'accumulator_constructor' in kwargs:
      acc = kwargs['accumulator_constructor'](acc_key, label, initial_value)
    else:
      # throw some exception
      return
    self.accumulator_categories[cat_key].add_accumulator(acc)
    return acc

  def add_accumulator(self, compound_key, label):
    return self.add_general_accumulator(compound_key, label, accumulator_constructor=Accumulator)

  def add_list_accumulator(self, compound_key, label):
    return self.add_general_accumulator(compound_key, label, accumulator_constructor=ListAccumulator)

  def add_character_accumulator(self, compound_key, label, starting_level=0):
    return self.add_general_accumulator(
        compound_key, 
        label, 
        initial_value=starting_level, 
        accumulator_constructor=CharacterAccumulator)

  def add_current_accumulator(self, compound_key, label):
    return self.add_general_accumulator(compound_key, label, accumulator_constructor=CurrentAccumulator)

  def add_sum_accumulator(self, compound_key, label, pos_accumulator_keys, neg_accumulator_keys):
    # Turn keys into objects
    pos_accumulators = list()
    for key in pos_accumulator_keys:
      pos_accumulators.append(self.get_accumulator(key))
    neg_accumulators = list()
    for key in neg_accumulator_keys:
      neg_accumulators.append(self.get_accumulator(key))

    return self.add_general_accumulator(
      compound_key, 
      label, 
      pos_accumulators=pos_accumulators,
      neg_accumulators=neg_accumulators )

  ## Depricated function
  # def add_function_accumulator(self, compound_key, label, accumulator_keys, accumulator_function):
  #   # Convert set of keys into dict of Accumulators to pass to FunctionAccumulator constructor.
  #   acc_dict = dict()
  #   for key in accumulator_keys:
  #     keys = self.validate_compound_key(key)
  #     acc = self.accumulator_categories[keys[0]].accumulators[keys[1]]
  #     acc_dict[key] = acc
  #   return self.add_general_accumulator(
  #     compound_key, 
  #     label,  
  #     accumulators=acc_dict, 
  #     accumulator_function=accumulator_function )


  # Methods for incrementing accumulators.

  def validate_compound_key(self, compound_key):
    keys = self.parse_compound_key(compound_key)    
    if not (keys[0] in self.accumulator_categories) \
        or not (keys[1] in self.accumulator_categories[keys[0]].accumulators):
      #throw exception
      return False
    else:
      return keys

  def gain_amount(self, compound_key, amt):
    keys = self.validate_compound_key(compound_key)
    cat_key = keys[0]
    acc_key = keys[1]
    acc = self.accumulator_categories[cat_key].accumulators[acc_key]
    acc.gain_amount(amt)

  def set_current(self, compound_key, amt):
    keys = self.validate_compound_key(compound_key)
    cat_key = keys[0]
    acc_key = keys[1]
    acc = self.accumulator_categories[cat_key].accumulators[acc_key]
    if not (type(acc) is CurrentAccumulator):
      #throw exception
      pass
    acc.set_current(amt)

  def split(self, name=None):
    cats = self.accumulator_categories
    for cat_key in cats:
      cats[cat_key].split()
    if name is None:
      name = str(self.split_number)
    self.split_names.append(name)
    self.split_number += 1


class SplitsLoader():
  def __init__(self):
    self.splits = None
    self.splits_name = ""

  def new_splits(self, name, subclass=None):
    filename = "data/" + name
    if os.path.isfile('./' + filename):
      return #ERROR name already in use
    self.splits_name = name
    if subclass is None:
      self.splits = AccumulatorManager()
    else :
      assert issubclass(subclass, AccumulatorManager)
      self.splits = subclass()

  def save_current_splits(self):
    with open("data/" + self.splits_name, 'wb') as outfile:
      pickle.dump(self.splits, outfile)

  def load_splits(self, name):
    filename = "data/" + name
    with open(filename, 'rb') as infile:
      self.splits = pickle.load(infile)
      self.splits_name = name




