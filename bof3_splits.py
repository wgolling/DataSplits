from accumulator import *
from enum import Enum
import itertools

class Category(Enum):
  char      = "Character"
  zenny     = "Zenny"
  skill_ink = "Skill Ink"

class Character(Enum):
  ryu     = "Ryu"
  rei_kid = "Rei"
  teepo   = "Teepo"
  nina    = "Nina"
  momo    = "Momo"
  peco    = "Peco"
  garr    = "Garr"
  rei     = "Rei"

  def key(self):
    return compound_key(Category.char.name, self.name)

starting_levels = {
  Character.ryu.name      : 1,
  Character.rei_kid.name  : 1,
  Character.teepo.name    : 1,
  Character.nina.name     : 5,
  Character.momo.name     : 10,
  Character.peco.name     : 1,
  Character.garr.name     : 13,
  Character.rei.name      : 20
}

class Zenny(Enum):
  pickups     = "Pickups"
  bossdrops   = "Boss Drops"
  spends      = "Expenditures"
  sales       = "Sales"
  current     = "Current"
  encounters  = "Encounters"
  
  def key(self):
    return compound_key(Category.zenny.name, self.name)

class SkillInk(Enum):
  pickups = "Pickups"
  uses    = "Uses"
  buys    = "Buys"
  current = "Current"

  def key(self):
    return compound_key(Category.skill_ink.name, self.name)

def compound_key(cat_key, acc_key):
  return cat_key + '-' + acc_key


class BreathOfFire3Splits(AccumulatorManager):

  def __init__(self):
    super().__init__()
    # dictionary to keep track of the characters in your party
    self.party = dict()
    for char_key, character in Character.__members__.items():
      self.party[char_key] = False
    self.party[Character.ryu.name] = True
    # character accumulators
    char_cat = Category.char
    self.add_accumulator_category(char_cat.name, char_cat.value)
    for char_key, character in Character.__members__.items():
      self.add_character_accumulator(
          character.key(), 
          character.value, 
          starting_level=starting_levels[character.name])

    # zenny accumulators
    zenny = Category.zenny
    self.add_accumulator_category(zenny.name, zenny.value)
    self.add_list_accumulator(Zenny.pickups.key()  , Zenny.pickups.value)
    self.add_list_accumulator(Zenny.bossdrops.key(), Zenny.bossdrops.value)
    self.add_list_accumulator(Zenny.spends.key()   , Zenny.spends.value)
    self.add_list_accumulator(Zenny.sales.key()    , Zenny.sales.value)
    self.add_current_accumulator(Zenny.current.key(), Zenny.current.value)
    ## add sum accumulator for zenny from encounters
    self.add_sum_accumulator(
      Zenny.encounters.key(), 
      Zenny.encounters.value, 
      [Zenny.current.key(), Zenny.spends.key()],
      [Zenny.pickups.key(), Zenny.bossdrops.key(), Zenny.sales.key()] 
    )

    # skill ink accumulators
    skill_ink = Category.skill_ink
    self.add_accumulator_category(skill_ink.name, skill_ink.value)
    self.add_accumulator(SkillInk.pickups.key(), SkillInk.pickups.value)
    self.add_accumulator(SkillInk.uses.key()   , SkillInk.uses.value)
    self.add_accumulator(SkillInk.buys.key()   , SkillInk.buys.value)
    ## add sum accumulator for current skill ink
    self.add_sum_accumulator(
      SkillInk.current.key(), 
      SkillInk.current.value, 
      [SkillInk.pickups.key(), SkillInk.buys.key()],
      [SkillInk.uses.key()] 
    )

  # Interface functions.

  ## Gaining and leveling up characters
  def gain_character(self, char_key):
    self.party[char_key] = True
  def lose_character(self, char_key):
    self.party[char_key] = False

  def level_up(self, char_key, amount=1):
    self.gain_amount(Character[char_key].key(), amount)

  def get_character_level(self, char_key):
    acc = self.get_accumulator(Character[char_key].key())
    c = acc.current_entry
    return c.total + c.gain

  ## Zenny interface
  def pickup_zenny(self, amt):
    self.gain_amount(Zenny.pickups.key(), amt)
  def zenny_from_boss(self, amt):
    self.gain_amount(Zenny.bossdrops.key(), amt)
  def spend_zenny(self, amt):
    self.gain_amount(Zenny.spends.key(), amt)
  def zenny_from_sale(self, amt):
    self.gain_amount(Zenny.sales.key(), amt)
  def set_current_zenny(self, amt):
    self.set_current(Zenny.current.key(), amt)
  def get_current_zenny(self):
    return self.get_accumulator(Zenny.current.key()).get_current()

  ## Skill Ink
  def pickup_skill_ink(self):
    self.gain_amount(SkillInk.pickups.key(), 1)
  def use_skill_ink(self):
    self.gain_amount(SkillInk.uses.key(), 1)
  def buy_skill_ink(self):
    self.gain_amount(SkillInk.buys.key(), 1)


  # Printing Functions
  class PrintData():
    def __init__(self, amt=0):
      self.entries = list()
      for i in range(0, amt):
        self.entries.append(self.Entry(i))

    def add_accumulator_data(self, acc, acc_type):
      entries_amt = len(self.entries)
      assert(entries_amt == len(acc.entries))
      acc_key = acc.key
      for i in range(0, entries_amt):
        if (acc_type == "character"):
          data_dict = self.entries[i].character_data
        elif (acc_type == "zenny"):
          data_dict = self.entries[i].zenny_data
        elif (acc_type == "skill_ink"):
          data_dict = self.entries[i].skill_ink_data
        data_dict[acc_key] = dict()
        data_dict[acc_key]['label'] = acc.label
        data_dict[acc_key]['total'] = acc.entries[i].total
        data_dict[acc_key]['gain']  = acc.entries[i].gain

    def add_character_accumulator_data(self, acc):
      self.add_accumulator_data(acc, "character")

    def add_zenny_accumulator_data(self, acc):
      self.add_accumulator_data(acc, "zenny")

    def add_skill_ink_accumulator_data(self, acc):
      self.add_accumulator_data(acc, 'skill_ink')

    class Entry():
      def __init__(self, name):
        self.name = name
        self.character_data = dict()
        self.zenny_data     = dict()
        self.skill_ink_data = dict()

  def make_print_data(self):
    data = self.PrintData(self.split_number)
    data = self.add_character_data(data)
    data = self.add_zenny_data(data)
    data = self.add_skill_ink_data(data)
    return data

  def add_character_data(self, print_data):
    for char_key, character in Character.__members__.items():
      acc = self.get_accumulator(character.key())
      print_data.add_character_accumulator_data(acc)
    return print_data
  def add_zenny_data(self, print_data):
    for zenny_key, zenny_enum in Zenny.__members__.items():
      acc = self.get_accumulator(zenny_enum.key())
      print_data.add_zenny_accumulator_data(acc)
    return print_data
  def add_skill_ink_data(self, print_data):
    for skill_ink_key, skill_ink_enum in SkillInk.__members__.items():
      acc = self.get_accumulator(skill_ink_enum.key())
      print_data.add_skill_ink_accumulator_data(acc)
    return print_data
