import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Import db data
from cafand_db import *

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

def generate_peak_hours():
    """Generate realistic peak hours for a coffee shop"""
    hour_weights = {
        6: 0.02, 7: 0.15, 8: 0.25, 9: 0.18, 10: 0.12, 11: 0.08,
        12: 0.15, 13: 0.12, 14: 0.08, 15: 0.06, 16: 0.05, 17: 0.04,
        18: 0.03, 19: 0.02, 20: 0.01, 21: 0.005
    }
    return hour_weights

def generate_transactions(start_date, end_date, avg_transactions_per_day=150):
    """Generate realistic transaction data for Café Andino"""
    
    transactions = []
    transaction_id = 1
    
    current_date = start_date
    hour_weights = generate_peak_hours()
    
    while current_date <= end_date:
        # Vary transactions by day of week (more on weekdays)
        day_multiplier = 1.2 if current_date.weekday() < 5 else 0.7  # Mon-Fri vs Weekend
        daily_transactions = int(avg_transactions_per_day * day_multiplier * random.uniform(0.8, 1.2))
        
        for _ in range(daily_transactions):
            # Select random hour based on weights
            hours = list(hour_weights.keys())
            probs = np.array(list(hour_weights.values()), dtype=float)
            probs = probs / probs.sum()  # normalize so probabilities sum to 1
            hour = np.random.choice(hours, p=probs)
            minute = random.randint(0, 59)
            
            # Select location
            location = random.choice(locations)
            
            # Generate 1-4 items per transaction (coffee shop typical)
            items_in_transaction = random.choices([1, 2, 3, 4], weights=[0.4, 0.35, 0.2, 0.05])[0]
            
            for item_num in range(items_in_transaction):
                # Select product based on popularity
                product_codes = list(products.keys())
                popularities = [products[code]['popularity'] for code in product_codes]
                
                # Normalize popularities
                total_pop = sum(popularities)
                normalized_pop = [p/total_pop for p in popularities]
                
                product_code = np.random.choice(product_codes, p=normalized_pop)
                product_info = products[product_code]
                
                # Generate quantity (mostly 1, sometimes 2)
                quantity = random.choices([1, 2], weights=[0.85, 0.15])[0]
                
                # Calculate total for this line item
                total_price = product_info['price'] * quantity
                
                # Create transaction record
                transaction = {
                    'trans_id': f"CA{transaction_id:06d}_{item_num+1}",
                    'fecha': current_date.strftime('%m/%d/%Y') + f" {hour:02d}:{minute:02d}:00 {'AM' if hour < 12 else 'PM'}",
                    'producto': product_code,
                    'glosa': product_info['name'],
                    'costo': product_info['cost'],
                    'total': total_price,
                    'cantidad': quantity,
                    'inith': hour,
                    'initm': minute,
                    'location': location
                }
                
                transactions.append(transaction)
            
            transaction_id += 1
        
        current_date += timedelta(days=1)
    
    return transactions

# Generate 3 months of data (September to November 2024)
start_date = datetime(2024, 9, 1)
end_date = datetime(2024, 11, 30)

print("Generating transaction data...")
transactions = generate_transactions(start_date, end_date)

# Create DataFrame
df = pd.DataFrame(transactions)

print(f"Generated {len(transactions)} transaction records")
print(f"Date range: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
print(f"Unique products: {df['producto'].nunique()}")
print(f"Locations: {df['location'].unique()}")

# Show sample data
print("\nSample transactions:")
print(df.head(10).to_string())

# Save to CSV
save_path = 'data/cafe_andino/cafe_andino_transactions.csv'
df.to_csv(save_path, index=False)
print(f"\nCSV file saved as '{save_path}'")

# Generate summary statistics
print(f"\nDataset Summary:")
print(f"Total transactions: {len(df)}")
print(f"Total revenue: ${df['total'].sum():,.0f}")
print(f"Average transaction value: ${df.groupby('trans_id')['total'].sum().mean():,.0f}")
print(f"Top 5 products by revenue:")
top_products = df.groupby(['producto', 'glosa'])['total'].sum().sort_values(ascending=False).head()
for (code, name), revenue in top_products.items():
    print(f"  {code}: {name} - ${revenue:,.0f}")