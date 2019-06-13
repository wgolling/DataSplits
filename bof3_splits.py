from accumulator import *

class BreathOfFire3Splits(AccumulatorManager):

  def __init__(self):
    super().__init__()
    self.add_accumulator_category('char', "Character")
    self.add_character_accumulator("char-ryu", "Ryu")
    # zenny accumulators
    self.add_accumulator_category("zenny", "Zenny")
    self.add_list_accumulator("zenny-pickups"   , "Pickups")
    self.add_list_accumulator("zenny-bossdrops" , "Boss Drops")
    self.add_list_accumulator("zenny-spends"    , "Expenditures")
    self.add_list_accumulator("zenny-sales"     , "Sales")
    self.add_current_accumulator("zenny-current", "Current")
    ## add function accumulator for zenny from enctounters
    keys_list = ["zenny-pickups", "zenny-bossdrops", "zenny-spends", "zenny-sales", "zenny-current"]
    def compute_encounters(gain_dict):
      pickup    = gain_dict["zenny-pickups"]
      bossdrops = gain_dict["zenny-bossdrops"]
      spends    = gain_dict["zenny-spends"]
      sales     = gain_dict["zenny-sales"]
      current   = gain_dict["zenny-current"]
      return current - pickup - bossdrops + spends - sales
    self.add_function_accumulator("zenny-encounters", "Encounters", keys_list, compute_encounters)
    # skill ink accumulators
    self.add_accumulator_category("skill_ink", "Skill Ink")
    self.add_accumulator("skill_ink-pickups",  "Pickups")
    self.add_accumulator("skill_ink-uses",     "Uses")
    self.add_accumulator("skill_ink-buys",     "Buys")
    ## add function accumulator for current skill ink
    keys_list = ["skill_ink-pickups", "skill_ink-uses", "skill_ink-buys"]
    def compute_current_skill_ink(gain_dict):
      pickup  = gain_dict["skill_ink-pickups"]
      uses    = gain_dict["skill_ink-uses"]
      buys    = gain_dict["skill_ink-buys"]
      return pickup + buys - uses
    self.add_function_accumulator("skill_ink-current", "Current", keys_list, compute_current_skill_ink)

  # Interface functions.

  ## Gaining and leveling up characters

  ## Zenny

  ## Skill Ink



