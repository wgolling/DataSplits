from accumulator import *

class BreathOfFire3Splits(AccumulatorManager):

  def __init__(self):
    super().__init__()
    self.add_accumulator_category('char', "Character")
    self.add_character_accumulator("char-ryu", "Ryu")
    # zenny accumulators
    self.add_accumulator_category("zenny", "Zenny")
    zenny_pickups   = self.add_list_accumulator("zenny-pickups"   , "Pickups")
    zenny_bossdrops = self.add_list_accumulator("zenny-bossdrops" , "Boss Drops")
    zenny_spends    = self.add_list_accumulator("zenny-spends"    , "Expenditures")
    zenny_sales     = self.add_list_accumulator("zenny-sales"     , "Sales")
    zenny_current   = self.add_current_accumulator("zenny-current", "Current")
    ## add sum accumulator for zenny from enctounters
    self.add_sum_accumulator(
      "zenny-encounters", 
      "Encounters", 
      [zenny_current, zenny_spends],
      [zenny_pickups, zenny_bossdrops, zenny_sales] 
    )
    # skill ink accumulators
    self.add_accumulator_category("skill_ink", "Skill Ink")
    sk_pickups  = self.add_accumulator("skill_ink-pickups",  "Pickups")
    sk_uses     = self.add_accumulator("skill_ink-uses"   ,  "Uses")
    sk_buys     = self.add_accumulator("skill_ink-buys"   ,  "Buys")
    ## add sum accumulator for current skill ink
    self.add_sum_accumulator(
      "skill_ink-current", 
      "Current", 
      [sk_pickups, sk_buys],
      [sk_uses] 
    )

  # Interface functions.

  ## Gaining and leveling up characters

  ## Zenny

  ## Skill Ink



