from bof3_splits import *
import unittest

class TestBreathOfFire3Splits(unittest.TestCase):

  def setUp(self):
    self.test_instance = BreathOfFire3Splits()

  def test_constructor(self):
    s = self.test_instance
    cats = s.accumulator_categories
    self.assertEqual( cats.keys(), 
                      set(['char', 'zenny', 'skill_ink']) )
    z_cat = cats['zenny']
    self.assertEqual(z_cat.key, 'zenny')
    self.assertEqual(z_cat.label, 'Zenny')
    z_accs = z_cat.accumulators 
    fixed_keys = set(["pickups",
                      "bossdrops", 
                      "spends", 
                      "sales", 
                      "current", 
                      "encounters"])
    self.assertEqual(z_accs.keys(), fixed_keys)

    
