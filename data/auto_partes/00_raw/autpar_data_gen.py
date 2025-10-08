import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Import db data
from autpar_db import products, customers

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

def generate_automotive_peak_hours():
    """Generate realistic peak hours for B2B automotive parts"""
    # B2B: busy during work hours, especially morning and early afternoon
    hour_weights = {
        8: 0.12, 9: 0.15, 10: 0.18, 11: 0.15, 12: 0.08, 13: 0.05,
        14: 0.12, 15: 0.10, 16: 0.08, 17: 0.05, 18: 0.02
    }
    return hour_weights

def apply_seasonal_automotive_effects(product_code, current_date):
    """Apply seasonal effects to automotive parts popularity"""
    base_popularity = products[product_code]['popularity']
    category = products[product_code]['category']
    month = current_date.month
    
    # Winter tire season (May-August in Chile)
    if category == 'tire' and 'INVIERNO' in products[product_code]['name'] and month in [5, 6, 7, 8]:
        return base_popularity * 3.0
    elif category == 'tire' and 'VERANO' in products[product_code]['name'] and month in [10, 11, 12, 1]:
        return base_popularity * 2.0
    
    # Battery failures increase in winter
    elif category == 'battery' and month in [6, 7, 8]:
        return base_popularity * 1.8
    
    # Brake maintenance before winter
    elif category == 'brake' and month in [4, 5]:
        return base_popularity * 1.5
    
    # Oil changes more frequent in summer heat
    elif category == 'oil' and month in [12, 1, 2]:
        return base_popularity * 1.3
    
    return base_popularity

def generate_automotive_transactions(start_date, end_date, avg_transactions_per_day=45):
    """Generate realistic transaction data for AutoPartes Chile"""
    
    transactions = []
    transaction_id = 1
    
    current_date = start_date
    hour_weights = generate_automotive_peak_hours()
    
    while current_date <= end_date:
        # Much lower activity on weekends for B2B
        day_multiplier = 1.0 if current_date.weekday() < 5 else 0.2  # Weekday vs Weekend
        daily_transactions = int(avg_transactions_per_day * day_multiplier * random.uniform(0.7, 1.3))
        
        for _ in range(daily_transactions):
            # Select random hour based on weights (only business hours)
            if current_date.weekday() < 5:  # Weekday
                hours = list(hour_weights.keys())
                probs = np.array(list(hour_weights.values()), dtype=float)
                probs = probs / probs.sum()  # normalize so probabilities sum to 1
                hour = np.random.choice(hours, p=probs)
            else:  # Weekend - limited hours
                hour = random.choice([9, 10, 11, 12])
            
            minute = random.randint(0, 59)
            
            # Select customer (B2B)
            customer = random.choice(customers)
            
            # B2B: Can have larger orders (1-8 items)
            items_in_transaction = random.choices([1, 2, 3, 4, 5, 6, 7, 8], 
                                                weights=[0.3, 0.25, 0.2, 0.12, 0.08, 0.03, 0.015, 0.005])[0]
            
            for item_num in range(items_in_transaction):
                # Apply seasonal effects
                seasonal_popularities = []
                product_codes = list(products.keys())
                
                for code in product_codes:
                    seasonal_pop = apply_seasonal_automotive_effects(code, current_date)
                    seasonal_popularities.append(seasonal_pop)
                
                # Normalize popularities
                total_pop = sum(seasonal_popularities)
                normalized_pop = [p/total_pop for p in seasonal_popularities]
                
                product_code = np.random.choice(product_codes, p=normalized_pop)
                product_info = products[product_code]
                
                # B2B quantities: can be higher for consumables
                if product_info['category'] in ['oil', 'filter', 'fluid']:
                    quantity = random.choices([1, 2, 3, 4, 5], weights=[0.4, 0.3, 0.2, 0.08, 0.02])[0]
                elif product_info['category'] in ['tire', 'brake']:
                    quantity = random.choices([1, 2, 4], weights=[0.3, 0.5, 0.2])[0]  # Often sold in pairs/sets
                else:
                    quantity = random.choices([1, 2], weights=[0.8, 0.2])[0]
                
                # Calculate total for this line item
                total_price = product_info['price'] * quantity
                
                # Create transaction record
                transaction = {
                    'trans_id': f"AP{transaction_id:06d}_{item_num+1}",
                    'fecha': current_date.strftime('%m/%d/%Y') + f" {hour:02d}:{minute:02d}:00 {'AM' if hour < 12 else 'PM'}",
                    'producto': product_code,
                    'glosa': product_info['name'],
                    'costo': product_info['cost'],
                    'total': total_price,
                    'cantidad': quantity,
                    'inith': hour,
                    'initm': minute,
                    'customer': customer
                }
                
                transactions.append(transaction)
            
            transaction_id += 1
        
        current_date += timedelta(days=1)
    
    return transactions

# Generate 2 months of data (May to June 2024) - includes seasonal tire changes
start_date = datetime(2024, 5, 1)
end_date = datetime(2024, 6, 30)

print("Generating AutoPartes Chile transaction data...")
transactions = generate_automotive_transactions(start_date, end_date)

# Create DataFrame
df = pd.DataFrame(transactions)

print(f"Generated {len(transactions)} transaction records")
print(f"Date range: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
print(f"Unique products: {df['producto'].nunique()}")
print(f"B2B Customers: {df['customer'].unique()}")

# Show sample data
print(f"\nSample transactions:")
print(df.head(10).to_string())

# Save to CSV
save_path = 'data/auto_partes/auto_partes_transactions.csv'
df.to_csv(save_path, index=False)
print(f"\nCSV file saved as '{save_path}'")

# Generate summary statistics
print(f"\nDataset Summary:")
print(f"Total transactions: {len(df)}")
print(f"Total revenue: ${df['total'].sum():,.0f}")
print(f"Average transaction value: ${df.groupby('trans_id')['total'].sum().mean():,.0f}")
print(f"Price range: ${df['total'].min():,.0f} - ${df['total'].max():,.0f}")

print(f"\nTop 10 products by revenue:")
top_products = df.groupby(['producto', 'glosa'])['total'].sum().sort_values(ascending=False).head(10)
for (code, name), revenue in top_products.items():
    print(f"  {code}: {name[:40]}... - ${revenue:,.0f}")

print(f"\nCategory breakdown by revenue:")
category_revenue = df.merge(
    pd.DataFrame([(k, v['category']) for k, v in products.items()], 
                columns=['producto', 'category']), 
    on='producto'
).groupby('category')['total'].sum().sort_values(ascending=False)

for category, revenue in category_revenue.items():
    print(f"  {category}: ${revenue:,.0f}")

print(f"\nB2B Customer analysis:")
customer_revenue = df.groupby('customer')['total'].sum().sort_values(ascending=False)
for customer, revenue in customer_revenue.items():
    print(f"  {customer}: ${revenue:,.0f}")