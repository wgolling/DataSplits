from accumulator import *

class BreathOfFire3Splits(AccumulatorManager):

  def __init__(self):
    super().__init__()
    self.add_accumulator_category('char', "Character")
    ## zenny accumulators
    self.add_accumulator_category("zenny", "Zenny")
    z_pickup    = self.add_list_accumulator("zenny-pickups",   "Pickups")
    z_bossdrop  = self.add_list_accumulator("zenny-bossdrops", "Boss Drops")
    z_spends    = self.add_list_accumulator("zenny-spends",    "Expenditures")
    z_sales     = self.add_list_accumulator("zenny-sales",     "Sales")
    z_current   = self.add_current_accumulator("zenny-current", "Current")
    accs = [z_pickup, z_bossdrop, z_spends, z_sales, z_current]
    keys_list = ["zenny-pickups", "zenny-bossdrops", "zenny-spends", "zenny-sales", "zenny-current"]
    def compute_encounters(acc_list):
      pickup = acc_list[0].entries[-1].gain
      bossdrop = acc_list[1].entries[-1].gain
      spends = acc_list[2].entries[-1].gain
      sales = acc_list[3].entries[-1].gain
      current = acc_list[4].entries[-1].gain
      return current - pickup - bossdrop + spends - sales
    self.add_function_accumulator("zenny-encounters", "Encounters", accs, compute_encounters)
    ## skill ink accumulators
    self.add_accumulator_category("skill_ink", "Skill Ink")
    self.add_accumulator("skill_ink-pickups",  "Pickups")
    self.add_accumulator("skill_ink-uses",     "Uses")
    self.add_accumulator("skill_ink-buys",     "Buys")
    self.add_current_accumulator("skill_ink-current", "Current")
