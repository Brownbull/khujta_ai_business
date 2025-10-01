import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Import db data
from tecmax_db import *

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

def generate_electronics_peak_hours():
    """Generate realistic peak hours for electronics retail"""
    # Electronics stores: busy lunch time, after work, weekends
    hour_weights = {
        10: 0.05, 11: 0.08, 12: 0.12, 13: 0.15, 14: 0.10, 15: 0.08,
        16: 0.06, 17: 0.08, 18: 0.12, 19: 0.10, 20: 0.06
    }
    return hour_weights

def generate_electronics_transactions(start_date, end_date, avg_transactions_per_day=80):
    """Generate realistic transaction data for TechnoMax"""
    
    transactions = []
    transaction_id = 1
    
    current_date = start_date
    hour_weights = generate_electronics_peak_hours()
    
    while current_date <= end_date:
        # More transactions on weekends for electronics
        day_multiplier = 1.4 if current_date.weekday() >= 5 else 1.0  # Weekend vs Weekday
        daily_transactions = int(avg_transactions_per_day * day_multiplier * random.uniform(0.7, 1.3))
        
        for _ in range(daily_transactions):
            # Select random hour based on weights
            hour = np.random.choice(list(hour_weights.keys()), p=list(hour_weights.values()))
            minute = random.randint(0, 59)
            
            # Select store (online gets more traffic)
            store = random.choices(stores, weights=[0.35, 0.25, 0.40])[0]
            
            # Electronics: usually 1-3 items per transaction
            items_in_transaction = random.choices([1, 2, 3], weights=[0.6, 0.3, 0.1])[0]
            
            for item_num in range(items_in_transaction):
                # Select product based on popularity
                product_codes = list(products.keys())
                popularities = [products[code]['popularity'] for code in product_codes]
                
                # Normalize popularities
                total_pop = sum(popularities)
                normalized_pop = [p/total_pop for p in popularities]
                
                product_code = np.random.choice(product_codes, p=normalized_pop)
                product_info = products[product_code]
                
                # Electronics: almost always quantity 1 (except accessories)
                if product_info['category'] == 'accessory':
                    quantity = random.choices([1, 2], weights=[0.8, 0.2])[0]
                else:
                    quantity = 1
                
                # Calculate total for this line item
                total_price = product_info['price'] * quantity
                
                # Create transaction record
                transaction = {
                    'trans_id': f"TX{transaction_id:06d}_{item_num+1}",
                    'fecha': current_date.strftime('%m/%d/%Y') + f" {hour:02d}:{minute:02d}:00 {'AM' if hour < 12 else 'PM'}",
                    'producto': product_code,
                    'glosa': product_info['name'],
                    'costo': product_info['cost'],
                    'total': total_price,
                    'cantidad': quantity,
                    'inith': hour,
                    'initm': minute,
                    'store': store
                }
                
                transactions.append(transaction)
            
            transaction_id += 1
        
        current_date += timedelta(days=1)
    
    return transactions

# Generate 2 months of data (October to November 2024)
start_date = datetime(2024, 10, 1)
end_date = datetime(2024, 11, 30)

print("Generating TechnoMax transaction data...")
transactions = generate_electronics_transactions(start_date, end_date)

# Create DataFrame
df = pd.DataFrame(transactions)

print(f"Generated {len(transactions)} transaction records")
print(f"Date range: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
print(f"Unique products: {df['producto'].nunique()}")
print(f"Stores: {df['store'].unique()}")

# Show sample data
print(f"\nSample transactions:")
print(df.head(10).to_string())

# Save to CSV
save_path = 'data/techno_max/techno_max_transactions.csv'
df.to_csv(save_path, index=False)
print(f"\nCSV file saved as '{save_path}'")
