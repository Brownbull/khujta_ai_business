import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Import db data
from cerand_db import *

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

def generate_brewery_peak_hours():
    """Generate realistic peak hours for craft brewery"""
    # Taproom: busy evenings and weekends, B2B during business hours
    hour_weights = {
        11: 0.03, 12: 0.05, 13: 0.04, 14: 0.03, 15: 0.05, 16: 0.08,
        17: 0.12, 18: 0.15, 19: 0.18, 20: 0.15, 21: 0.10, 22: 0.02
    }
    return hour_weights

def apply_brewery_seasonal_effects(product_code, current_date):
    """Apply seasonal effects to brewery products"""
    base_popularity = products[product_code]['popularity']
    category = products[product_code]['category']
    month = current_date.month
    
    # Seasonal beer effects (Chilean seasons)
    if category == 'beer_seasonal':
        product_name = products[product_code]['name']
        
        # Autumn beer (March-May)
        if 'OTOÑO' in product_name and month in [3, 4, 5]:
            return base_popularity * 4.0
        # Winter beer (June-August)
        elif 'INVIERNO' in product_name and month in [6, 7, 8]:
            return base_popularity * 4.0
        # Spring beer (September-November)
        elif 'PRIMAVERA' in product_name and month in [9, 10, 11]:
            return base_popularity * 4.0
        # Summer beer (December-February)
        elif 'VERANO' in product_name and month in [12, 1, 2]:
            return base_popularity * 4.0
        else:
            return base_popularity * 0.2  # Out of season
    
    # Core beers get winter boost
    elif category == 'beer_core':
        if month in [6, 7, 8]:  # Winter
            return base_popularity * 1.3
        else:
            return base_popularity
    
    # Lighter beers popular in summer
    elif category == 'beer_core' and products[product_code]['abv'] < 5.0:
        if month in [12, 1, 2]:  # Summer
            return base_popularity * 1.5
        else:
            return base_popularity
    
    # Old seasonal items decline rapidly
    elif category == 'beer_old':
        return base_popularity * 0.1
    
    return base_popularity

def determine_sales_channel():
    """Determine if sale is taproom, B2B, or online"""
    return random.choices(channels, weights=[0.6, 0.3, 0.1])[0]

def generate_brewery_transactions(start_date, end_date, avg_transactions_per_day=75):
    """Generate realistic transaction data for Cerveza Artesanal Los Andes"""
    
    transactions = []
    transaction_id = 1
    
    current_date = start_date
    hour_weights = generate_brewery_peak_hours()
    
    while current_date <= end_date:
        # Much higher activity on weekends for taproom
        day_multiplier = 1.8 if current_date.weekday() >= 5 else 1.0  # Weekend vs Weekday
        daily_transactions = int(avg_transactions_per_day * day_multiplier * random.uniform(0.7, 1.3))
        
        for _ in range(daily_transactions):
            # Determine sales channel first
            channel = determine_sales_channel()
            
            # Different hour patterns by channel
            if channel == 'DISTRIBUTOR_B2B':
                # B2B during business hours only
                hour = random.choice([9, 10, 11, 14, 15, 16])
            else:
                # Taproom/online during evening hours
                hours = list(hour_weights.keys())
                probs = np.array(list(hour_weights.values()), dtype=float)
                probs = probs / probs.sum()  # normalize so probabilities sum to 1
                hour = np.random.choice(hours, p=probs)
            
            minute = random.randint(0, 59)
            
            # Different order patterns by channel
            if channel == 'DISTRIBUTOR_B2B':
                # B2B: larger orders, mainly core beers
                items_in_transaction = random.choices([4, 6, 8, 12, 24], weights=[0.3, 0.3, 0.2, 0.15, 0.05])[0]
                customer = random.choice(b2b_customers)
            else:
                # Taproom: smaller orders, more variety including food
                items_in_transaction = random.choices([1, 2, 3, 4], weights=[0.4, 0.35, 0.2, 0.05])[0]
                customer = 'TAPROOM_CUSTOMER'
            
            for item_num in range(items_in_transaction):
                # Apply seasonal effects
                seasonal_popularities = []
                product_codes = list(products.keys())
                
                for code in product_codes:
                    seasonal_pop = apply_brewery_seasonal_effects(code, current_date)
                    
                    # Channel-specific product filtering
                    if channel == 'DISTRIBUTOR_B2B':
                        # B2B mainly wants packaged beer, no tap or food
                        if products[code]['category'] in ['beer_tap', 'food']:
                            seasonal_pop *= 0.1
                        elif products[code]['category'] in ['beer_core', 'beer_pack']:
                            seasonal_pop *= 2.0  # B2B loves core products
                    
                    elif channel == 'TAPROOM_DIRECT':
                        # Taproom can sell everything, boost tap and food
                        if products[code]['category'] in ['beer_tap', 'food']:
                            seasonal_pop *= 1.5
                    
                    seasonal_popularities.append(seasonal_pop)
                
                # Normalize popularities
                total_pop = sum(seasonal_popularities)
                normalized_pop = [p/total_pop for p in seasonal_popularities]
                
                product_code = np.random.choice(product_codes, p=normalized_pop)
                product_info = products[product_code]
                
                # Quantity based on channel and product type
                if channel == 'DISTRIBUTOR_B2B':
                    # B2B orders in cases/bulk
                    if product_info['category'] in ['beer_core', 'beer_seasonal']:
                        quantity = random.choices([6, 12, 24], weights=[0.4, 0.4, 0.2])[0]  # Cases
                    else:
                        quantity = random.choices([1, 2, 3], weights=[0.6, 0.3, 0.1])[0]
                else:
                    # Taproom: individual servings
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
                    'channel': channel,
                    'customer': customer if channel == 'DISTRIBUTOR_B2B' else 'TAPROOM'
                }
                
                transactions.append(transaction)
            
            transaction_id += 1
        
        current_date += timedelta(days=1)
    
    return transactions

# Generate 2 months of data (June to July 2024) - Chilean winter season
start_date = datetime(2024, 6, 1)
end_date = datetime(2024, 7, 31)

print("Generating Cerveza Artesanal Los Andes transaction data...")
transactions = generate_brewery_transactions(start_date, end_date)

# Create DataFrame
df = pd.DataFrame(transactions)

print(f"Generated {len(transactions)} transaction records")
print(f"Date range: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
print(f"Unique products: {df['producto'].nunique()}")
print(f"Sales channels: {df['channel'].unique()}")

# Show sample data
print(f"\nSample transactions:")
print(df.head(10).to_string())

# Save to CSV
save_path = 'data/cerveza_losandes/cerveza_losandes_transactions.csv'
df.to_csv(save_path, index=False)
print(f"\nCSV file saved as '{save_path}'")
