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

starting_levels = {
  Character.ryu.name : 1,
  Character.rei_kid.name : 1,
  Character.teepo.name : 1,
  Character.nina.name : 5,
  Character.momo.name : 10,
  Character.peco.name : 1,
  Character.garr.name : 13,
  Character.rei.name : 20
}

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
      self.add_character_accumulator(char_cat.name + "-" + char_key, character.value)
      self.gain_amount(char_cat.name + '-' + char_key, starting_levels[character.name]) # initialize at starting level

    # zenny accumulators
    zenny = Category.zenny
    self.add_accumulator_category(zenny.name, zenny.value)
    # self.add_accumulator_category("zenny", "Zenny")
    zenny_pickups   = self.add_list_accumulator(zenny.name + "-pickups"   , "Pickups")
    zenny_bossdrops = self.add_list_accumulator(zenny.name + "-bossdrops" , "Boss Drops")
    zenny_spends    = self.add_list_accumulator(zenny.name + "-spends"    , "Expenditures")
    zenny_sales     = self.add_list_accumulator(zenny.name + "-sales"     , "Sales")
    zenny_current   = self.add_current_accumulator(zenny.name + "-current", "Current")

    ## add sum accumulator for zenny from encounters
    self.add_sum_accumulator(
      zenny.name + "-encounters", 
      "Encounters", 
      [zenny.name + "-current", zenny.name + "-spends"],
      [zenny.name + "-pickups", zenny.name + "-bossdrops", zenny.name + "-sales"] 
    )

    # skill ink accumulators
    skill_ink = Category.skill_ink
    self.add_accumulator_category(skill_ink.name, skill_ink.value)
    sk_pickups  = self.add_accumulator(skill_ink.name + "-pickups",  "Pickups")
    sk_uses     = self.add_accumulator(skill_ink.name + "-uses"   ,  "Uses")
    sk_buys     = self.add_accumulator(skill_ink.name + "-buys"   ,  "Buys")

    ## add sum accumulator for current skill ink
    self.add_sum_accumulator(
      skill_ink.name + "-current", 
      "Current", 
      [skill_ink.name + "-pickups", skill_ink.name + "-buys"],
      [skill_ink.name + "-uses"] 
    )

  # Interface functions.

  ## Gaining and leveling up characters
  def gain_char(self, char_key):
    self.party[char_key] = True
  def lose_char(self, char_key):
    self.party[char_key] = False

  def level_up(self, char_key, amount=1):
    self.gain_amount(Category.char.name + '-' + char_key, amount)

  def get_character_level(self, char_key):
    acc = self.get_accumulator(Category.char.name + '-' + char_key)
    c = acc.current_entry
    return c.total + c.gain

  ## Zenny interface
  def pickup_zenny(self, amt):
    self.gain_amount(Category.zenny.name + '-pickups', amt)
  def zenny_from_boss(self, amt):
    self.gain_amount(Category.zenny.name + '-bossdrops', amt)
  def spend_zenny(self, amt):
    self.gain_amount(Category.zenny.name + '-spends', amt)
  def zenny_from_sale(self, amt):
    self.gain_amount(Category.zenny.name + '-sales', amt)
  def set_current_zenny(self, amt):
    self.set_current(Category.zenny.name + '-current', amt)
  def get_current_zenny(self):
    return self.get_accumulator(Category.zenny.name + '-current').get_current()

  ## Skill Ink
  def pickup_skill_ink(self):
    self.gain_amount(Category.skill_ink.name + '-pickups', 1)
  def use_skill_ink(self):
    self.gain_amount(Category.skill_ink.name + '-uses', 1)
  def buy_skill_ink(self):
    self.gain_amount(Category.skill_ink.name + '-buys', 1)



