import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Import db data
from comer_db import *

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Add remaining mid-tier customers
for i in range(6, 26):  # B006-B025 for demo
    location = random.choice(['Villarrica', 'Pucón', 'Temuco', 'Lican Ray'])
    seasonal = location in ['Pucón', 'Lican Ray'] and random.random() < 0.6
    customers[f'B{i:03d}'] = {
        'name': f"{random.choice(mid_tier_names)} {random.choice(['CENTRAL', 'SUR', 'NORTE', 'LAGO', 'VOLCAN'])}",
        'type': 'business_mid',
        'location': location,
        'seasonal': seasonal
    }

# Add small customers
for i in range(4, 21):  # S004-S020 for demo
    location = random.choice(['Villarrica', 'Pucón', 'Temuco', 'Lican Ray'])
    is_individual = random.random() < 0.3
    customer_type = 'individual' if is_individual else 'small'
    customers[f'S{i:03d}'] = {
        'name': f"{random.choice(small_names)} {random.choice(['MARTINEZ', 'GONZALEZ', 'RODRIGUEZ', 'SILVA', 'LOPEZ'])}",
        'type': customer_type,
        'location': location,
        'seasonal': False
    }

def generate_food_distributor_peak_hours():
    """Generate realistic peak hours for B2B food distributor"""
    # B2B food service: busy Monday-Tuesday (weekly ordering), morning peak
    hour_weights = {
        8: 0.15, 9: 0.18, 10: 0.20, 11: 0.15, 12: 0.08, 13: 0.05,
        14: 0.10, 15: 0.06, 16: 0.03
    }
    return hour_weights

def apply_chilean_seasonal_effects(product_code, current_date, customer_id):
    """Apply Chilean tourism seasonality and product-specific effects"""
    base_popularity = products[product_code]['popularity']
    category = products[product_code]['category']
    month = current_date.month
    customer_info = customers.get(customer_id, {})
    is_seasonal_customer = customer_info.get('seasonal', False)
    
    # Chilean seasonal factors
    seasonal_multiplier = 1.0
    if month == 12:  # December peak (Christmas + summer tourism)
        seasonal_multiplier = 1.4
    elif month == 9:  # September (Fiestas Patrias)
        seasonal_multiplier = 1.2
    elif month in [1, 2]:  # January-February (summer tourism)
        seasonal_multiplier = 1.15
    elif month in [5, 6]:  # May-June (low season)
        seasonal_multiplier = 0.85
    elif month in [7, 8]:  # July-August (winter)
        seasonal_multiplier = 0.9
    
    # Fresh seafood peaks in summer
    if category == 'fresh_seafood' and month in [12, 1, 2]:
        seasonal_multiplier *= 1.3
    elif category == 'fresh_seafood' and month in [6, 7, 8]:
        seasonal_multiplier *= 0.7
    
    # Seasonal customer effects
    if is_seasonal_customer and month in [5, 6, 7, 8]:
        seasonal_multiplier *= 0.3  # Many Pucón businesses close/reduce in winter
    
    # Dead inventory gets worse over time
    if category == 'dead_inventory':
        seasonal_multiplier *= 0.1
    
    return base_popularity * seasonal_multiplier

def determine_customer_order_pattern(customer_id):
    """Determine order frequency and size based on customer type"""
    customer_info = customers.get(customer_id, {})
    customer_type = customer_info.get('type', 'small')
    
    if customer_type == 'restaurant_top':
        # Large restaurants: weekly orders, 8-15 items, $150K-500K CLP
        frequency_days = random.choice([7, 10, 14])
        items_per_order = random.choices([8, 10, 12, 15], weights=[0.2, 0.3, 0.3, 0.2])[0]
        base_order_value = random.uniform(150000, 500000)
    elif customer_type == 'business_mid':
        # Mid-tier: bi-weekly orders, 5-10 items, $50K-150K CLP
        frequency_days = random.choice([10, 14, 21])
        items_per_order = random.choices([5, 7, 8, 10], weights=[0.3, 0.3, 0.2, 0.2])[0]
        base_order_value = random.uniform(50000, 150000)
    else:
        # Small/individual: sporadic orders, 1-4 items, $10K-50K CLP
        frequency_days = random.choice([14, 21, 30, 45])
        items_per_order = random.choices([1, 2, 3, 4], weights=[0.4, 0.3, 0.2, 0.1])[0]
        base_order_value = random.uniform(10000, 50000)
    
    return frequency_days, items_per_order, base_order_value

def generate_food_distributor_transactions(start_date, end_date, avg_transactions_per_day=60):
    """Generate realistic transaction data for Comercializadora Al Sur"""
    
    transactions = []
    transaction_id = 1
    
    current_date = start_date
    hour_weights = generate_food_distributor_peak_hours()
    
    while current_date <= end_date:
        # Lower activity on weekends (B2B focus)
        day_multiplier = 0.3 if current_date.weekday() >= 5 else 1.0
        
        # Chilean seasonal effects on overall activity
        month = current_date.month
        if month == 12:
            day_multiplier *= 1.4
        elif month == 9:
            day_multiplier *= 1.2
        elif month in [1, 2]:
            day_multiplier *= 1.15
        elif month in [5, 6]:
            day_multiplier *= 0.85
        
        daily_transactions = int(avg_transactions_per_day * day_multiplier * random.uniform(0.7, 1.3))
        
        for _ in range(daily_transactions):
            # Select customer based on revenue distribution (65% top, 25% mid, 10% small)
            customer_tier = random.choices(['restaurant_top', 'business_mid', 'small'], 
                                         weights=[0.65, 0.25, 0.10])[0]
            
            # Select random customer from appropriate tier
            eligible_customers = [cid for cid, info in customers.items() 
                                if info['type'] == customer_tier or 
                                (customer_tier == 'small' and info['type'] == 'individual')]
            
            if not eligible_customers:
                continue
                
            customer_id = random.choice(eligible_customers)
            customer_info = customers[customer_id]
            
            # Skip seasonal customers during off-season
            if customer_info.get('seasonal', False) and current_date.month in [5, 6, 7, 8]:
                if random.random() < 0.7:  # 70% chance to skip
                    continue
            
            # Select hour based on business patterns
            hour = np.random.choice(list(hour_weights.keys()), p=list(hour_weights.values()))
            minute = random.randint(0, 59)
            
            # Determine order size based on customer type
            _, items_per_order, base_order_value = determine_customer_order_pattern(customer_id)
            
            for item_num in range(items_per_order):
                # Apply seasonal effects to product selection
                seasonal_popularities = []
                product_codes = list(products.keys())
                
                for code in product_codes:
                    seasonal_pop = apply_chilean_seasonal_effects(code, current_date, customer_id)
                    
                    # Customer type preferences
                    if customer_info['type'] == 'restaurant_top':
                        if products[code]['category'] in ['sushi_supplies', 'fresh_seafood']:
                            seasonal_pop *= 2.0
                    elif customer_info['type'] == 'business_mid':
                        if products[code]['category'] in ['frozen', 'dry_goods']:
                            seasonal_pop *= 1.5
                    elif customer_info['type'] in ['small', 'individual']:
                        if products[code]['category'] in ['dry_goods', 'frozen']:
                            seasonal_pop *= 1.2
                    
                    seasonal_popularities.append(seasonal_pop)
                
                # Normalize popularities
                total_pop = sum(seasonal_popularities)
                if total_pop == 0:
                    continue
                normalized_pop = [p/total_pop for p in seasonal_popularities]
                
                product_code = np.random.choice(product_codes, p=normalized_pop)
                product_info = products[product_code]
                
                # Quantity based on customer type and product
                if customer_info['type'] == 'restaurant_top':
                    if product_info['category'] in ['fresh_seafood', 'frozen']:
                        quantity = random.choices([2, 3, 5, 10], weights=[0.3, 0.3, 0.3, 0.1])[0]
                    else:
                        quantity = random.choices([1, 2, 3], weights=[0.5, 0.3, 0.2])[0]
                elif customer_info['type'] == 'business_mid':
                    quantity = random.choices([1, 2, 3], weights=[0.6, 0.3, 0.1])[0]
                else:
                    quantity = random.choices([1, 2], weights=[0.8, 0.2])[0]
                
                # Apply customer-specific pricing (volume discounts)
                price = product_info['price']
                if customer_info['type'] == 'restaurant_top':
                    price *= random.uniform(0.85, 0.95)  # 5-15% discount
                elif customer_info['type'] == 'business_mid':
                    price *= random.uniform(0.90, 0.98)  # 2-10% discount
                
                total_price = price * quantity
                
                # Create transaction record
                transaction = {
                    'trans_id': f"AS{transaction_id:06d}_{item_num+1}",
                    'fecha': current_date.strftime('%m/%d/%Y') + f" {hour:02d}:{minute:02d}:00 {'AM' if hour < 12 else 'PM'}",
                    'producto': product_code,
                    'glosa': product_info['name'],
                    'costo': product_info['cost'],
                    'total': int(total_price),
                    'cantidad': quantity,
                    'inith': hour,
                    'initm': minute,
                    'customer_id': customer_id,
                    'customer_name': customer_info['name'],
                    'customer_location': customer_info['location']
                }
                
                transactions.append(transaction)
            
            transaction_id += 1
        
        current_date += timedelta(days=1)
    
    return transactions

# Generate 3 months of data (December 2024 to February 2025) - includes peak season
start_date = datetime(2024, 12, 1)
end_date = datetime(2025, 2, 28)

print("Generating Comercializadora Al Sur transaction data...")
transactions = generate_food_distributor_transactions(start_date, end_date)

# Create DataFrame
df = pd.DataFrame(transactions)

print(f"Generated {len(transactions)} transaction records")
print(f"Date range: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
print(f"Unique products: {df['producto'].nunique()}")
print(f"Unique customers: {df['customer_id'].nunique()}")

# Show sample data
print(f"\nSample transactions:")
print(df.head(10).to_string())

# Save to CSV
save_path = 'data/comercializadora/comercializadora_transactions.csv'
df.to_csv(save_path, index=False)
print(f"\nCSV file saved as '{save_path}'")
