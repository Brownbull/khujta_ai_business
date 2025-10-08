import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random


# Import db data
from farsal_db import *

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

def generate_pharmacy_peak_hours():
    """Generate realistic peak hours for a pharmacy"""
    # Pharmacies: busy morning (chronic meds), lunch, and evening
    hour_weights = {
        8: 0.08, 9: 0.12, 10: 0.10, 11: 0.08, 12: 0.15, 13: 0.12, 
        14: 0.08, 15: 0.06, 16: 0.05, 17: 0.06, 18: 0.08, 19: 0.10, 
        20: 0.06, 21: 0.04
    }
    return hour_weights

def apply_seasonal_effects(product_code, current_date):
    """Apply seasonal effects to popularity (flu season, allergies, etc.)"""
    base_popularity = products[product_code]['popularity']
    category = products[product_code]['category']
    month = current_date.month
    
    # Winter flu season (June-August in Chile)
    if category == 'cold' and month in [6, 7, 8]:
        return base_popularity * 2.5
    elif category == 'cold' and month in [5, 9]:
        return base_popularity * 1.5
    
    # Spring allergy season (September-November)
    elif category == 'allergy' and month in [9, 10, 11]:
        return base_popularity * 1.8
    
    # Summer beauty products (December-February)
    elif category == 'beauty' and month in [12, 1, 2]:
        return base_popularity * 1.4
    
    # Vitamin C boost in winter
    elif product_code == 'VIT001' and month in [6, 7, 8]:
        return base_popularity * 1.6
    
    return base_popularity

def generate_pharmacy_transactions(start_date, end_date, avg_transactions_per_day=120):
    """Generate realistic transaction data for Farmacia Salud+"""
    
    transactions = []
    transaction_id = 1
    
    current_date = start_date
    hour_weights = generate_pharmacy_peak_hours()
    
    while current_date <= end_date:
        # More transactions on weekdays (people getting prescriptions)
        day_multiplier = 1.1 if current_date.weekday() < 5 else 0.8  # Weekday vs Weekend
        daily_transactions = int(avg_transactions_per_day * day_multiplier * random.uniform(0.8, 1.2))
        
        for _ in range(daily_transactions):
            # Select random hour based on weights
            hours = list(hour_weights.keys())
            probs = np.array(list(hour_weights.values()), dtype=float)
            probs = probs / probs.sum()  # normalize so probabilities sum to 1
            hour = np.random.choice(hours, p=probs)
            minute = random.randint(0, 59)
            
            # Select location (online gets some traffic)
            location = random.choices(locations, weights=[0.3, 0.25, 0.25, 0.2])[0]
            
            # Pharmacy: usually 1-3 items per transaction
            items_in_transaction = random.choices([1, 2, 3], weights=[0.5, 0.35, 0.15])[0]
            
            for item_num in range(items_in_transaction):
                # Apply seasonal effects
                seasonal_popularities = []
                product_codes = list(products.keys())
                
                for code in product_codes:
                    seasonal_pop = apply_seasonal_effects(code, current_date)
                    seasonal_popularities.append(seasonal_pop)
                
                # Normalize popularities
                total_pop = sum(seasonal_popularities)
                normalized_pop = [p/total_pop for p in seasonal_popularities]
                
                product_code = np.random.choice(product_codes, p=normalized_pop)
                product_info = products[product_code]
                
                # Quantity: mostly 1, sometimes 2 for OTC meds
                if product_info['category'] in ['analgesic', 'vitamin', 'baby']:
                    quantity = random.choices([1, 2], weights=[0.7, 0.3])[0]
                else:
                    quantity = 1
                
                # Calculate total for this line item
                total_price = product_info['price'] * quantity
                
                # Create transaction record
                transaction = {
                    'trans_id': f"FS{transaction_id:06d}_{item_num+1}",
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

# Generate 2 months of data (September to October 2024) - includes seasonal changes
start_date = datetime(2024, 9, 1)
end_date = datetime(2024, 10, 31)

print("Generating Farmacia Salud+ transaction data...")
transactions = generate_pharmacy_transactions(start_date, end_date)

# Create DataFrame
df = pd.DataFrame(transactions)

print(f"Generated {len(transactions)} transaction records")
print(f"Date range: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
print(f"Unique products: {df['producto'].nunique()}")
print(f"Locations: {df['location'].unique()}")

# Show sample data
print(f"\nSample transactions:")
print(df.head(10).to_string())

# Save to CSV
save_path = 'data/farmacia_salud/farmacia_salud_transactions.csv'
df.to_csv(save_path, index=False)
print(f"\nCSV file saved as '{save_path}'")
