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
