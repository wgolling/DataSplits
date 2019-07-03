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
      self.add_character_accumulator(character.key(), character.value)
      self.gain_amount(character.key(), starting_levels[character.name]) # initialize at starting level

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



