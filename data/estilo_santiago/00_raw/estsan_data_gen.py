import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Import db data
from estsan_db import *

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

def generate_fashion_peak_hours():
    """Generate realistic peak hours for fashion retail"""
    # Fashion: busy lunch, after work, and weekends
    hour_weights = {
        10: 0.05, 11: 0.08, 12: 0.12, 13: 0.15, 14: 0.08, 15: 0.06,
        16: 0.07, 17: 0.10, 18: 0.12, 19: 0.10, 20: 0.07
    }
    return hour_weights

def apply_fashion_seasonal_effects(product_code, current_date):
    """Apply seasonal effects to fashion popularity"""
    base_popularity = products[product_code]['popularity']
    season = products[product_code]['season']
    month = current_date.month
    
    # Current season items (AW2024) peak in autumn/winter
    if season == 'AW2024':
        if month in [3, 4, 5, 6]:  # Chilean autumn/winter
            return base_popularity * 1.5
        elif month in [7, 8]:  # Peak winter
            return base_popularity * 2.0
        else:
            return base_popularity * 0.8
    
    # Previous season clearance (SS2024) - declining sales
    elif season == 'SS2024':
        if month in [3, 4]:  # Early clearance
            return base_popularity * 0.6
        else:  # Deep clearance
            return base_popularity * 0.3
    
    # Old inventory (AW2023) - almost dead
    elif season == 'AW2023':
        return base_popularity * 0.2
    
    return base_popularity

def add_size_color_variations():
    """Add realistic size/color variations to fashion items"""
    sizes = ['XS', 'S', 'M', 'L', 'XL']
    colors = ['NEGRO', 'BLANCO', 'AZUL', 'GRIS', 'BEIGE', 'CAFE', 'ROJO']
    
    # Randomly assign if item has size/color variations
    has_size = random.choice([True, False])
    has_color = random.choice([True, False])
    
    variations = []
    if has_size:
        variations.append(random.choice(sizes))
    if has_color:
        variations.append(random.choice(colors))
    
    return ' '.join(variations) if variations else ''

def generate_fashion_transactions(start_date, end_date, avg_transactions_per_day=85):
    """Generate realistic transaction data for Estilo Santiago"""
    
    transactions = []
    transaction_id = 1
    
    current_date = start_date
    hour_weights = generate_fashion_peak_hours()
    
    while current_date <= end_date:
        # Much higher activity on weekends for fashion retail
        day_multiplier = 1.6 if current_date.weekday() >= 5 else 1.0  # Weekend vs Weekday
        daily_transactions = int(avg_transactions_per_day * day_multiplier * random.uniform(0.8, 1.2))
        
        for _ in range(daily_transactions):
            # Select random hour based on weights
            hours = list(hour_weights.keys())
            probs = np.array(list(hour_weights.values()), dtype=float)
            probs = probs / probs.sum()  # normalize so probabilities sum to 1
            hour = np.random.choice(hours, p=probs)
            minute = random.randint(0, 59)
            
            # Select location
            location = random.choices(locations, weights=[0.4, 0.35, 0.25])[0]
            
            # Fashion: usually 1-3 items per transaction
            items_in_transaction = random.choices([1, 2, 3], weights=[0.55, 0.35, 0.1])[0]
            
            for item_num in range(items_in_transaction):
                # Apply seasonal effects
                seasonal_popularities = []
                product_codes = list(products.keys())
                
                for code in product_codes:
                    seasonal_pop = apply_fashion_seasonal_effects(code, current_date)
                    seasonal_popularities.append(seasonal_pop)
                
                # Normalize popularities
                total_pop = sum(seasonal_popularities)
                normalized_pop = [p/total_pop for p in seasonal_popularities]
                
                product_code = np.random.choice(product_codes, p=normalized_pop)
                product_info = products[product_code]
                
                # Fashion: almost always quantity 1 (except accessories)
                if product_info['category'] == 'accessory':
                    quantity = random.choices([1, 2], weights=[0.9, 0.1])[0]
                else:
                    quantity = 1
                
                # Add size/color variations to product name
                variations = add_size_color_variations()
                full_product_name = f"{product_info['name']} {variations}".strip()
                
                # Calculate total for this line item
                total_price = product_info['price'] * quantity
                
                # Create transaction record
                transaction = {
                    'trans_id': f"ES{transaction_id:06d}_{item_num+1}",
                    'fecha': current_date.strftime('%m/%d/%Y') + f" {hour:02d}:{minute:02d}:00 {'AM' if hour < 12 else 'PM'}",
                    'producto': product_code,
                    'glosa': full_product_name,
                    'costo': product_info['cost'],
                    'total': total_price,
                    'cantidad': quantity,
                    'inith': hour,
                    'initm': minute,
                    'location': location,
                    'season': product_info['season']
                }
                
                transactions.append(transaction)
            
            transaction_id += 1
        
        current_date += timedelta(days=1)
    
    return transactions

# Generate 2 months of data (March to April 2024) - Chilean autumn season transition
start_date = datetime(2024, 3, 1)
end_date = datetime(2024, 4, 30)

print("Generating Estilo Santiago fashion transaction data...")
transactions = generate_fashion_transactions(start_date, end_date)

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
save_path = 'data/estilo_santiago/estilo_santiago_transactions.csv'
df.to_csv(save_path, index=False)
print(f"\nCSV file saved as '{save_path}'")
