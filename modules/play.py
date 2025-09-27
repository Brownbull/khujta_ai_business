# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from tabulate import tabulate
from datetime import datetime, timedelta
pd.set_option('display.float_format', '{:.0f}'.format)

def executive_summary(twenty_percent:int, revenue_from_top_prcnt:float, dead_stock:list, total_dead_money:float, peak_day:str, peak_hour:int, valley_day:str):
  print("=" * 50)
  print("DISTRIBUIDORA INSIGHTS SUMMARY")
  print("=" * 50)
  print(f"\n1. 🎯 FOCUS: Your top {twenty_percent} products generate {revenue_from_top_prcnt:.0f}% of revenue")
  print(f"   → Action: Focus inventory and marketing on these winners\n")

  if 'total_dead_money' in locals() and total_dead_money is not np.nan:
      print(f"2. 💰 CASH TRAP: ${total_dead_money:,.0f} stuck in dead inventory")
      print(f"   → Action: Liquidate these {len(dead_stock)} products ASAP\n")

  print(f"3. ⏰ OPTIMAL HOURS: Peak business on {peak_day}s @ {peak_hour}:00")
  print(f"   → Action: Staff accordingly, consider closing early on {valley_day}s\n")
  print("=" * 50)