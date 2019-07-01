from accumulator import *
from enum import Enum

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

class BreathOfFire3Splits(AccumulatorManager):

  def __init__(self):
    super().__init__()
    # character accumulators
    char_cat = Category.char
    self.add_accumulator_category(char_cat.name, char_cat.value)
    for char_key, character in Character.__members__.items():
      self.add_character_accumulator(char_cat.name + "-" + char_key, character.value)
    # self.add_accumulator_category('char', "Character")
    # self.add_character_accumulator(char + "-ryu"     , "Ryu")
    # self.add_character_accumulator(char + "-rei_kid" , "Rei")
    # self.add_character_accumulator(char + "-teepo"   , "Teepo")
    # self.add_character_accumulator(char + "-nina"    , "Nina")
    # self.add_character_accumulator(char + "-momo"    , "Momo")
    # self.add_character_accumulator(char + "-peco"    , "Peco")
    # self.add_character_accumulator(char + "-garr"    , "Garr")
    # self.add_character_accumulator(char + "-rei"     , "Rei")

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
    # self.add_sum_accumulator(
    #   zenny.name + "-encounters", 
    #   "Encounters", 
    #   [zenny_current, zenny_spends],
    #   [zenny_pickups, zenny_bossdrops, zenny_sales] 
    # )
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
    # self.add_sum_accumulator(
    #   skill_ink.name + "-current", 
    #   "Current", 
    #   [sk_pickups, sk_buys],
    #   [sk_uses] 
    # )
    self.add_sum_accumulator(
      skill_ink.name + "-current", 
      "Current", 
      [skill_ink.name + "-pickups", skill_ink.name + "-buys"],
      [skill_ink.name + "-uses"] 
    )

  # Interface functions.

  ## Gaining and leveling up characters
#  def gain_char(self, char_key):


  ## Zenny

  ## Skill Ink



