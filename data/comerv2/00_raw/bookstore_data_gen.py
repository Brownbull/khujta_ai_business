import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Import db data
from bookstore_db import products, locations, customer_types

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

def generate_bookstore_peak_hours():
    """Generate realistic peak hours for academic bookstore"""
    # Bookstore: busy during day, especially lunch and after classes
    hour_weights = {
        9: 0.05, 10: 0.08, 11: 0.10, 12: 0.15, 13: 0.12, 14: 0.08,
        15: 0.10, 16: 0.12, 17: 0.10, 18: 0.08, 19: 0.02
    }
    return hour_weights

def apply_academic_seasonal_effects(product_code, current_date):
    """Apply academic calendar effects to book sales"""
    base_popularity = products[product_code]['popularity']
    category = products[product_code]['category']
    month = current_date.month
    day = current_date.day
    
    # Chilean academic calendar effects
    # Semester start (March, August) - huge textbook demand
    if category == 'textbook_current':
        if month == 3 and day <= 15:  # First semester start
            return base_popularity * 8.0
        elif month == 8 and day <= 15:  # Second semester start
            return base_popularity * 6.0
        elif month in [3, 4, 8, 9]:  # During semester
            return base_popularity * 2.0
        elif month in [1, 2, 7]:  # Vacation periods
            return base_popularity * 0.3
        else:
            return base_popularity
    
    # Stationery peaks at semester start and throughout academic year
    elif category == 'stationery':
        if month == 3 and day <= 20:  # Start of academic year
            return base_popularity * 4.0
        elif month == 8 and day <= 15:  # Second semester
            return base_popularity * 2.5
        elif month in [3, 4, 5, 8, 9, 10, 11]:  # Academic months
            return base_popularity * 1.5
        else:
            return base_popularity * 0.6
    
    # Gift books peak in December (holidays)
    elif category in ['coffee_table', 'cookbook']:
        if month == 12:
            return base_popularity * 3.0
        elif month in [11, 1]:  # Holiday season spillover
            return base_popularity * 1.5
        else:
            return base_popularity
    
    # Old textbooks decline rapidly
    elif category == 'textbook_old':
        return base_popularity * 0.2
    
    # General books steady throughout year
    else:
        return base_popularity

def determine_customer_type():
    """Determine customer type based on probabilities"""
    return random.choices(customer_types, weights=[0.45, 0.25, 0.25, 0.05])[0]

def generate_bookstore_transactions(start_date, end_date, avg_transactions_per_day=65):
    """Generate realistic transaction data for Libros & Más"""
    
    transactions = []
    transaction_id = 1
    
    current_date = start_date
    hour_weights = generate_bookstore_peak_hours()
    
    while current_date <= end_date:
        # Lower activity on weekends (academic bookstore)
        day_multiplier = 0.4 if current_date.weekday() >= 5 else 1.0  # Weekend vs Weekday
        daily_transactions = int(avg_transactions_per_day * day_multiplier * random.uniform(0.8, 1.2))
        
        for _ in range(daily_transactions):
            # Select random hour based on weights
            hours = list(hour_weights.keys())
            probs = np.array(list(hour_weights.values()), dtype=float)
            probs = probs / probs.sum()  # normalize so probabilities sum to 1
            hour = np.random.choice(hours, p=probs)
            minute = random.randint(0, 59)
            
            # Select location
            location = random.choices(locations, weights=[0.5, 0.35, 0.15])[0]
            
            # Determine customer type
            customer_type = determine_customer_type()
            
            # Different purchase patterns by customer type
            if customer_type == 'ESTUDIANTE':
                items_in_transaction = random.choices([1, 2, 3, 4], weights=[0.4, 0.35, 0.2, 0.05])[0]
            elif customer_type == 'PROFESIONAL':
                items_in_transaction = random.choices([1, 2, 3], weights=[0.6, 0.3, 0.1])[0]
            elif customer_type == 'PROFESOR':
                items_in_transaction = random.choices([1, 2, 3, 4, 5], weights=[0.3, 0.3, 0.2, 0.15, 0.05])[0]
            else:  # GENERAL
                items_in_transaction = random.choices([1, 2], weights=[0.8, 0.2])[0]
            
            for item_num in range(items_in_transaction):
                # Apply seasonal effects
                seasonal_popularities = []
                product_codes = list(products.keys())
                
                for code in product_codes:
                    seasonal_pop = apply_academic_seasonal_effects(code, current_date)
                    
                    # Customer type preferences
                    if customer_type == 'ESTUDIANTE':
                        if products[code]['category'] in ['textbook_current', 'stationery']:
                            seasonal_pop *= 3.0
                        elif products[code]['category'] == 'fiction':
                            seasonal_pop *= 1.5
                    elif customer_type == 'PROFESIONAL':
                        if products[code]['category'] in ['reference', 'business']:
                            seasonal_pop *= 2.0
                    elif customer_type == 'PROFESOR':
                        if products[code]['category'] in ['textbook_current', 'reference', 'specialty']:
                            seasonal_pop *= 2.5
                    elif customer_type == 'GENERAL':
                        if products[code]['category'] in ['fiction', 'selfhelp', 'cookbook']:
                            seasonal_pop *= 2.0
                    
                    seasonal_popularities.append(seasonal_pop)
                
                # Normalize popularities
                total_pop = sum(seasonal_popularities)
                normalized_pop = [p/total_pop for p in seasonal_popularities]
                
                product_code = np.random.choice(product_codes, p=normalized_pop)
                product_info = products[product_code]
                
                # Quantity: mostly 1, sometimes 2 for stationery
                if product_info['category'] == 'stationery':
                    quantity = random.choices([1, 2, 3], weights=[0.6, 0.3, 0.1])[0]
                else:
                    quantity = random.choices([1, 2], weights=[0.9, 0.1])[0]
                
                # Calculate total for this line item
                total_price = product_info['price'] * quantity
                
                # Create transaction record
                transaction = {
                    'trans_id': f"LM{transaction_id:06d}_{item_num+1}",
                    'fecha': current_date.strftime('%m/%d/%Y') + f" {hour:02d}:{minute:02d}:00 {'AM' if hour < 12 else 'PM'}",
                    'producto': product_code,
                    'glosa': product_info['name'],
                    'costo': product_info['cost'],
                    'total': total_price,
                    'cantidad': quantity,
                    'inith': hour,
                    'initm': minute,
                    'location': location,
                    'customer_type': customer_type
                }
                
                transactions.append(transaction)
            
            transaction_id += 1
        
        current_date += timedelta(days=1)
    
    return transactions

if __name__ == "__main__":
    # Generate 2 months of data (March to April 2024) - includes semester start spike
    start_date = datetime(2024, 3, 1)
    end_date = datetime(2024, 4, 30)

    print("Generating Libros & Más bookstore transaction data...")
    transactions = generate_bookstore_transactions(start_date, end_date)

    # Create DataFrame
    df = pd.DataFrame(transactions)

    # Save to CSV
    save_path = 'data/bookstore/bookstore_transactions.csv'
    df.to_csv(save_path, index=False)
    print(f"\nCSV file saved as '{save_path}'")

    print(f"Generated {len(transactions)} transaction records")
    print(f"Date range: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    print(f"Unique products: {df['producto'].nunique()}")
    print(f"Locations: {df['location'].unique()}")
    print(f"Customer types: {df['customer_type'].unique()}")

    # Show sample data
    print(f"\nSample transactions:")
    print(df.head(10).to_string())