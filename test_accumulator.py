from accumulator import *
import unittest

class TestAccumulator(unittest.TestCase):

  def setUp(self):
    self.test_instance = Accumulator("Test Key", "Test Label")

  def test_constructor(self):
    t = self.test_instance
    self.assertEqual(t.key  , "Test Key")
    self.assertEqual(t.label, "Test Label")
    e = t.current_entry    
    self.assertEqual(e.gain , 0)
    self.assertEqual(e.total, 0)

  def test_gain(self):
    t = self.test_instance
    t.gain_amount(5)
    e = t.current_entry
    self.assertEqual(e.gain, 5)
    self.assertEqual(e.total, 0)

  def test_split(self):
    t = self.test_instance
    t.gain_amount(5)
    t.split()
    e0 = t.entries[0]
    self.assertEqual(e0.gain, 5)
    self.assertEqual(e0.total, 5)
    e1 = t.current_entry
    self.assertEqual(e1.gain, 0)
    self.assertEqual(e1.total, 5)


class TestListAccumulator(unittest.TestCase):

  def setUp(self):
    self.test_instance = ListAccumulator("Test Key", "Test Label")

  def test_constructor(self):
    t = self.test_instance
    self.assertEqual(t.key  , "Test Key")
    self.assertEqual(t.label, "Test Label")
    e = t.current_entry
    self.assertEqual(e.gain , 0)
    self.assertEqual(e.total, 0)
    assert(type(e.list) is list and not e.list)

  def test_gain(self):
    t = self.test_instance
    t.gain_amount(5)
    e = t.current_entry
    self.assertEqual(e.gain, 5)
    self.assertEqual(e.total, 0)
    assert(len(e.list) == 1)
    self.assertEqual(e.list[0], 5)    

  def test_split(self):
    t = self.test_instance
    t.gain_amount(5)
    t.split()
    e0 = t.entries[0]
    self.assertEqual(e0.gain, 5)
    self.assertEqual(e0.total, 5)
    assert(len(e0.list) == 1)
    self.assertEqual(e0.list[0], 5)    
    e1 = t.current_entry
    self.assertEqual(e1.gain, 0)
    self.assertEqual(e1.total, 5)
    assert(len(e1.list) == 0)


class TestCurrentAccumulator(unittest.TestCase):

  def setUp(self):
    self.test_instance = CurrentAccumulator("Test Key", "Test Label")

  def test_constructor(self):
    t = self.test_instance
    self.assertEqual(t.key  , "Test Key")
    self.assertEqual(t.label, "Test Label")
    e = t.current_entry    
    self.assertEqual(e.gain , 0)
    self.assertEqual(e.total, 0)

  def test_gain(self):
    t = self.test_instance
    t.gain_amount(5)
    e = t.current_entry
    self.assertEqual(e.gain, 5)
    self.assertEqual(e.total, 0)

  def test_set_current(self):
    t = self.test_instance
    t.set_current(6)
    self.assertEqual(t.current_entry.total, 6)

  def test_split(self):
    t = self.test_instance
    t.set_current(6)
    t.split()
    t.set_current(4)
    t.split()
    e0 = t.entries[0]
    self.assertEqual(e0.gain, 6)
    self.assertEqual(e0.total, 6)
    e1 = t.entries[1]
    self.assertEqual(e1.gain, -2)
    self.assertEqual(e1.total, 4)
    #e2 = t.current_entry


# class TestFunctionAccumulator(unittest.TestCase):

#   def setUp(self):
#     self.acc      = Accumulator("acc", "Plain Accumulator")
#     self.list_acc = ListAccumulator("list", "List Accumulator")
#     self.curr_acc = CurrentAccumulator("curr", "Current Accumulator")
#     acc_keys = {"acc" : self.acc, "list" : self.list_acc, "curr" : self.curr_acc}
#     def acc_function(value_dict):
#       val0 = value_dict["acc"]
#       val1 = value_dict["list"] 
#       val2 = value_dict["curr"] 
#       return val2 - val0 - val1
#     self.test_instance = FunctionAccumulator("Test Key", "Test Label", acc_keys, acc_function)

#   def test_constructor(self):
#     t = self.test_instance
#     self.assertEqual(t.key  , "Test Key")
#     self.assertEqual(t.label, "Test Label")
#     e = t.current_entry    
#     self.assertEqual(e.gain , 0)
#     self.assertEqual(e.total, 0)

#   def test_gain(self):
#     t = self.test_instance
#     t.gain_amount(5)
#     e = t.current_entry
#     self.assertEqual(e.gain, 5)
#     self.assertEqual(e.total, 0)

#   def test_split(self):
#     t = self.test_instance
#     a = self.acc
#     l = self.list_acc
#     c = self.curr_acc
#     a.gain_amount(5)
#     a.split()
#     l.gain_amount(7)
#     l.split()
#     c.set_current(15)
#     c.split()
#     t.split()
#     a.gain_amount(2)
#     a.split()
#     l.gain_amount(3)
#     l.split()
#     c.set_current(25)
#     c.split()
#     t.split()
#     e0 = t.entries[0]
#     self.assertEqual(e0.gain, 3)
#     self.assertEqual(e0.total, 3)
#     e1 = t.entries[1]
#     self.assertEqual(e1.gain, 5)
#     self.assertEqual(e1.total, 8)


class TestSumAccumulator(unittest.TestCase):

  def setUp(self):
    self.acc1      = Accumulator("acc1", "Plain Accumulator")
    self.acc2      = Accumulator("acc2", "Another Plain Accumulator")
    self.list_acc  = ListAccumulator("list", "List Accumulator")
    self.test_instance = SumAccumulator(
      'test', 
      "Test Sum Accumulator", 
      [self.acc1, self.list_acc], 
      [self.acc2]
    )

  def test_constructor(self):
    t = self.test_instance
    self.assertEqual(t.key  , "test")
    self.assertEqual(t.label, "Test Sum Accumulator")
    e = t.current_entry    
    self.assertEqual(e.gain , 0)
    self.assertEqual(e.total, 0)

    self.assertEqual(len(t.pos_accumulators), 2)
    self.assertEqual(len(t.neg_accumulators), 1)

  def test_gain(self):
    t = self.test_instance
    t.gain_amount(5)
    e = t.current_entry
    self.assertEqual(e.gain, 5)
    self.assertEqual(e.total, 0)

  def test_split(self):
    self.acc1.gain_amount(7)
    self.acc1.split()
    self.acc2.gain_amount(4)
    self.acc2.split()
    self.list_acc.gain_amount(6)
    self.list_acc.split()

    self.assertEqual(len(self.test_instance.entries), 0)
    self.test_instance.split()
    self.assertEqual(len(self.test_instance.entries), 1)
    e0 = self.test_instance.entries[0]
    self.assertEqual(e0.gain, 9)
    self.assertEqual(e0.total, 9)




class TestAccumulatorManager(unittest.TestCase):

  def setUp(self):
    # Construct test instance
    self.accumulator_manager = AccumulatorManager()
    m = self.accumulator_manager
    # add accumulators
    m.add_accumulator_category('test', "Test Category")
    acc = m.add_accumulator('test-test_1', "Test Accumulator")
    m.add_accumulator('test-test_2', "Other Test Accumulator")
    m.add_accumulator('other_test-test_1', "Accumulator in other category")
    list_acc = m.add_list_accumulator('test-test_list', "List Accumulator")
    curr_acc = m.add_current_accumulator('test-test_current', "Current Accumulator")
    #accs = [acc, list_acc, curr_acc]
    acc_keys = {'test-test_1', 'test-test_list', 'test-test_current'}
    def acc_function(acc_dict):
      val0 = acc_dict['test-test_1']
      val1 = acc_dict['test-test_list']
      val2 = acc_dict['test-test_current'] 
      return val2 - val0 - val1
    # m.add_function_accumulator('test-test_func', "Function Accumulator", acc_keys, acc_function)
    m.add_sum_accumulator(
      'test-test_sum', 
      "Sum Accumulator", 
      ['test-test_current'],
      ['test-test_1', 'test-test_list'])

  def test_add_accumulators(self):
    m = self.accumulator_manager
    cat_keys = m.accumulator_categories.keys()
    assert(len(cat_keys) == 2)
    assert('test' in cat_keys)
    assert('other_test' in cat_keys)
    test_cat = m.accumulator_categories['test']
    assert(len(test_cat.accumulators) == 5)
    other_cat = m.accumulator_categories['other_test']
    assert(len(other_cat.accumulators) == 1)
    acc = m.accumulator_categories['test'].accumulators['test_list']
    self.assertEqual(acc.label, "List Accumulator")

  def test_increment_accumulators(self):
    m = self.accumulator_manager
    cats = m.accumulator_categories
    acc = cats['test'].accumulators['test_1']
    list_acc = cats['test'].accumulators['test_list']
    curr_acc = cats['test'].accumulators['test_current']
    # func_acc = cats['test'].accumulators['test_func']
    sum_acc = cats['test'].accumulators['test_sum']
    m.gain_amount('test-test_1', 5)
    m.gain_amount('test-test_list', 7)
    m.set_current('test-test_current', 15)
    self.assertEqual(acc.current_entry.gain, 5)
    self.assertEqual(acc.current_entry.total, 0)
    self.assertEqual(m.split_number, 0)
    m.split()
    self.assertEqual(m.split_number, 1)
    self.assertEqual(acc.current_entry.gain, 0)
    self.assertEqual(acc.current_entry.total, 5)
    # self.assertEqual(func_acc.entries[0].gain, 3)
    self.assertEqual(sum_acc.entries[0].gain, 3)

  def test_save_and_load(self):
    m = self.accumulator_manager
    m.gain_amount('test-test_1', 5)
    m.gain_amount('test-test_list', 7)
    m.set_current('test-test_current', 15)
    m.split()
    m.save()

    new_m = AccumulatorManager.load()
    self.assertEqual(new_m.split_number, 1)
    acc = new_m.get_accumulator('test-test_1')
    self.assertEqual(acc.current_entry.gain, 0)
    self.assertEqual(acc.current_entry.total, 5)

  # def test_whatever(self):
  #   assert(1==1)






