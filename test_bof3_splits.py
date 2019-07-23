from bof3_splits import *
from accumulator import SplitsLoader
import unittest

class TestBreathOfFire3Splits(unittest.TestCase):

  def setUp(self):
    self.test_instance = BreathOfFire3Splits()
    self.new_splits = "temp-splits"
    while os.path.isfile('./data/' + self.new_splits):
      self.new_splits += 'a'

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
    garr = s.get_accumulator(Character.garr.key())
    assert(not garr.in_party)


  def test_gaining_and_losing_characters(self):
    s = self.test_instance
    ryu = s.get_accumulator(Character.ryu.key())
    garr = s.get_accumulator(Character.garr.key())
    assert(ryu.in_party)
    assert(not garr.in_party)
    s.gain_character(Character.garr)
    s.lose_character(Character.ryu)
    assert(not ryu.in_party)
    assert(garr.in_party)

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

  def test_saving_and_loading(self):
    sl = SplitsLoader()
    sl.new_splits(self.new_splits, BreathOfFire3Splits)
    splits = sl.splits
    splits.level_up('ryu', 5)
    splits.level_up('garr', 2)
    splits.split()
    splits.pickup_zenny(500)
    splits.set_current_zenny(600)
    splits.split()
    splits.pickup_skill_ink()
    splits.buy_skill_ink()
    splits.use_skill_ink()
    splits.split()

    sl.save_current_splits()

    new_sl = SplitsLoader()
    new_sl.load_splits(self.new_splits)
    new_splits = new_sl.splits

    ryu = new_splits.get_accumulator('char-ryu')
    self.assertEqual(ryu.current_entry.total, 6)
    garr = new_splits.get_accumulator('char-garr')
    self.assertEqual(garr.current_entry.total, 15)
    enc_zenny = new_splits.get_accumulator('zenny-encounters')
    self.assertEqual(enc_zenny.current_entry.total, 100)
    sk_current = new_splits.get_accumulator('skill_ink-current')
    self.assertEqual(sk_current.current_entry.total, 1)

    os.remove('./data/' + self.new_splits)


  def test_print_data(self):
    s = self.test_instance
    ryu = s.get_accumulator('char-ryu')
    s.level_up('ryu', 3)
    s.pickup_zenny(40)
    s.set_current_zenny(50)
    s.buy_skill_ink()
    self.assertEqual(ryu.current_entry.gain, 3)
    s.split("First Split")
    s.level_up('ryu',2)
    s.gain_character(Character.nina)
    s.level_up('nina', 3)
    s.pickup_zenny(3)
    s.set_current_zenny(60)
    s.buy_skill_ink()
    s.buy_skill_ink()
    s.split()
    self.assertEqual(s.split_number, 2)
    data = s.make_print_data()
    self.assertEqual(len(data.entries), 2)
    first_entry = data.entries[0]
    self.assertEqual(first_entry.name, "First Split")
    self.assertEqual(first_entry.character_data['ryu']['label'], 'Ryu')
    self.assertEqual(first_entry.character_data['ryu']['gain'], 3)
    self.assertEqual(first_entry.character_data['ryu']['total'], 4)
    self.assertEqual(first_entry.zenny_data['pickups']['gain'], 40)
    self.assertEqual(first_entry.zenny_data['pickups']['total'], 40)
    self.assertEqual(first_entry.zenny_data['encounters']['gain'], 10)
    self.assertEqual(first_entry.zenny_data['encounters']['total'], 10)
    self.assertEqual(first_entry.skill_ink_data['buys']['gain'], 1)
    self.assertEqual(first_entry.skill_ink_data['buys']['total'], 1)
    second_entry = data.entries[1]
    self.assertEqual(second_entry.name, "1")
    self.assertEqual(second_entry.character_data['ryu']['gain'], 2)
    self.assertEqual(second_entry.character_data['ryu']['total'], 6)
    self.assertEqual(second_entry.zenny_data['pickups']['gain'], 3)
    self.assertEqual(second_entry.zenny_data['pickups']['total'], 43)
    self.assertEqual(second_entry.zenny_data['encounters']['gain'], 7)
    self.assertEqual(second_entry.zenny_data['encounters']['total'], 17)
    self.assertEqual(second_entry.skill_ink_data['buys']['gain'], 2)
    self.assertEqual(second_entry.skill_ink_data['buys']['total'], 3)

    print_string = s.print()
    with open("data/print_test", 'w+') as outfile:
      outfile.write(print_string)


class TestCLI(unittest.TestCase):
  def setUp(self):
    self.cli = SplitsCLI()
    self.sl = self.cli.splits_loader

    self.new_splits = "temp-splits"
    while os.path.isfile('./data/' + self.new_splits):
      self.new_splits += 'a'


  def test_new_splits(self):
    with open("data/" + self.new_splits, "w") as file:
        file.write("Dummy file.")
    self.sl.new_splits(self.new_splits)
    assert(self.sl.splits is None)
    assert(self.sl.splits_name == "")

    os.remove('./data/' + self.new_splits)
    
    self.sl.new_splits(self.new_splits)
    assert(type(self.sl.splits) == AccumulatorManager)
    assert(self.sl.splits_name == self.new_splits)


  def test_save(self):
    self.sl.new_splits(self.new_splits)
    self.sl.save_current_splits()
    assert(os.path.isfile('./data/' + self.new_splits))
    os.remove('./data/' + self.new_splits)


  def test_save_and_load(self):
    with self.assertRaises(FileNotFoundError):
      self.sl.load_splits(self.new_splits)
    assert(self.sl.splits is None)
    self.sl.new_splits(self.new_splits)
    self.sl.save_current_splits()
    fresh_splits_loader = SplitsLoader()
    fresh_splits_loader.load_splits(self.new_splits)
    assert(type(fresh_splits_loader.splits) == AccumulatorManager)
    os.remove('./data/' + self.new_splits)

  def test_bad_constructor(self):
    with self.assertRaises(AssertionError):
      self.sl.new_splits(self.new_splits, SplitsLoader)

  def test_bof3_splits(self):
    self.sl.new_splits(self.new_splits, BreathOfFire3Splits)
    assert(type(self.sl.splits) == BreathOfFire3Splits)
    self.sl.save_current_splits()
    fresh_splits_loader = SplitsLoader()
    fresh_splits_loader.load_splits(self.new_splits)
    assert(type(fresh_splits_loader.splits) == BreathOfFire3Splits)
    os.remove('./data/' + self.new_splits)


