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

    garr_level = s.get_character_level('garr')
    self.assertEqual(garr_level, 13)
    assert(not s.party['garr'])

  def levelling_up_characters(self):
    s = self.test_instance
    ryu_level = s.get_character_level('ryu')
    self.assertEqual(ryu_level, 1)
    s.level_up('ryu')
    ryu_level = s.get_character_level('ryu')
    self.assertEqual(ryu_level, 2)
    s.level_up('ryu', 4)
    ryu_level = s.get_character_level('ryu')
    self.assertEqual(ryu_level, 6)

  def test_zenny_interface(self):
    s = self.test_instance
    self.assertEqual(s.get_current_zenny(), 0)
    s.pickup_zenny(10)
    acc = s.get_accumulator('zenny-pickups')
    self.assertEqual(acc.current_entry.gain, 10)
    s.spend_zenny(3)
    acc = s.get_accumulator('zenny-spends')
    self.assertEqual(acc.current_entry.gain, 3)
    s.zenny_from_sale(5)
    acc = s.get_accumulator('zenny-sales')
    self.assertEqual(acc.current_entry.gain, 5)
    s.set_current_zenny(20)
    acc = s.get_accumulator('zenny-current')
    self.assertEqual(acc.current_entry.total, 20)
    s.split()
    acc = s.get_accumulator('zenny-encounters')
    self.assertEqual(acc.current_entry.total, 8)

  def test_skill_ink_interface(self):
    s = self.test_instance
    s.pickup_skill_ink()
    s.pickup_skill_ink()
    acc = s.get_accumulator('skill_ink-pickups')
    self.assertEqual(acc.current_entry.gain, 2)
    s.use_skill_ink()
    acc = s.get_accumulator('skill_ink-uses')
    self.assertEqual(acc.current_entry.gain, 1)
    s.buy_skill_ink()
    acc = s.get_accumulator('skill_ink-buys')
    self.assertEqual(acc.current_entry.gain, 1)
    s.pickup_skill_ink()
    s.split()
    acc = s.get_accumulator('skill_ink-current')
    self.assertEqual(acc.current_entry.total, 3)


