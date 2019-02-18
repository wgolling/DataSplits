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


class TestFunctionAccumulator(unittest.TestCase):

  def setUp(self):
    self.acc      = Accumulator("acc", "Plain Accumulator")
    self.list_acc = ListAccumulator("list", "List Accumulator")
    self.curr_acc = CurrentAccumulator("curr", "Current Accumulator")
    accs = [self.acc, self.list_acc, self.curr_acc]
    def acc_function(acc_list):
      val0 = acc_list[0].entries[-1].gain
      val1 = acc_list[1].entries[-1].gain 
      val2 = acc_list[2].entries[-1].gain 
      return val2 - val0 - val1
    self.test_instance = FunctionAccumulator("Test Key", "Test Label", accs, acc_function)

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
    a = self.acc
    l = self.list_acc
    c = self.curr_acc
    a.gain_amount(5)
    a.split()
    l.gain_amount(7)
    l.split()
    c.set_current(15)
    c.split()
    t.split()
    a.gain_amount(2)
    a.split()
    l.gain_amount(3)
    l.split()
    c.set_current(25)
    c.split()
    t.split()
    e0 = t.entries[0]
    self.assertEqual(e0.gain, 3)
    self.assertEqual(e0.total, 3)
    e1 = t.entries[1]
    self.assertEqual(e1.gain, 5)
    self.assertEqual(e1.total, 8)
