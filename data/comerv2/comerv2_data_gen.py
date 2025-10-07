"""
Mock Data Generator for Comercializadora Al Sur
Generates realistic business data for a food distribution PYME in Villarrica, Chile
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import json

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

class AlSurDataGenerator:
    
    def __init__(self, start_date='2024-01-01', months=12):
        self.start_date = pd.to_datetime(start_date)
        self.end_date = self.start_date + timedelta(days=30*months)
        
        # Product categories and items
        self.categories = {
            'Sushi Supplies': ['Nori Sheets', 'Wasabi Powder', 'Sushi Rice', 'Rice Vinegar', 
                              'Bamboo Mats', 'Ginger Pickled', 'Soy Sauce Premium'],
            'Seafood Fresh': ['Salmon Fillet', 'Tuna Steak', 'Shrimp Raw', 'Crab Meat',
                             'Sea Bass', 'Octopus', 'Mussels'],
            'Seafood Frozen': ['Salmon Portions', 'Shrimp Frozen', 'Calamari Rings',
                              'Fish Mix', 'Crab Sticks', 'Seafood Mix'],
            'Asian Ingredients': ['Teriyaki Sauce', 'Sesame Oil', 'Miso Paste', 
                                 'Rice Noodles', 'Sriracha', 'Oyster Sauce'],
            'Frozen Specialties': ['Edamame', 'Gyoza', 'Spring Rolls', 'Tempura Mix']
        }
        
        # Customer types
        self.customer_types = {
            'Restaurant': 0.45,
            'Hotel': 0.20,
            'Cafe': 0.15,
            'Market': 0.10,
            'Catering': 0.10
        }
        
        # Villarrica business names
        self.business_names = {
            'Restaurant': ['Sushi Bar Villarrica', 'El Pescador', 'Sabor Oriental', 
                          'La Bahía', 'Restaurante Del Lago', 'Casa Kimchi'],
            'Hotel': ['Hotel Villarrica Park Lake', 'Hotel El Ciervo', 'Apart Hotel Los Volcanes'],
            'Cafe': ['Café Rincón', 'Coffee & Co', 'La Esquina Dulce'],
            'Market': ['Minimarket Central', 'Super Economico'],
            'Catering': ['Eventos Gourmet', 'Catering Premium']
        }
    
    def generate_products(self):
        """Generate product catalog with pricing"""
        products = []
        product_id = 1
        
        for category, items in self.categories.items():
            for item in items:
                # Price varies by category
                if 'Fresh' in category:
                    base_price = np.random.uniform(8000, 25000)
                elif 'Frozen' in category:
                    base_price = np.random.uniform(5000, 15000)
                else:
                    base_price = np.random.uniform(3000, 12000)
                
                # Cost is 60-75% of price
                cost = base_price * np.random.uniform(0.60, 0.75)
                
                products.append({
                    'product_id': f'PROD{product_id:04d}',
                    'name': item,
                    'category': category,
                    'price_clp': round(base_price, -2),  # Round to nearest 100
                    'cost_clp': round(cost, -2),
                    'unit': 'kg' if 'Fillet' in item or 'Steak' in item else 'unit',
                    'min_order_qty': 1 if 'Fresh' in category else 5
                })
                product_id += 1
        
        return pd.DataFrame(products)
    
    def generate_customers(self, n_customers=25):
        """Generate customer list"""
        customers = []
        
        for i in range(1, n_customers + 1):
            # Select customer type based on distribution
            cust_type = np.random.choice(
                list(self.customer_types.keys()),
                p=list(self.customer_types.values())
            )
            
            # Select business name
            name = random.choice(self.business_names[cust_type])
            
            # Customer attributes
            customers.append({
                'customer_id': f'CUST{i:04d}',
                'business_name': name,
                'type': cust_type,
                'contact_person': self._generate_name(),
                'phone': f'+56 9 {random.randint(7000, 9999)} {random.randint(1000, 9999)}',
                'email': f'{name.lower().replace(" ", "")[:10]}@gmail.com',
                'credit_limit_clp': random.choice([500000, 1000000, 2000000, 3000000]),
                'payment_terms_days': random.choice([15, 30, 45]),
                'since_date': self.start_date - timedelta(days=random.randint(30, 365*3))
            })
        
        return pd.DataFrame(customers)
    
    def generate_sales_transactions(self, products_df, customers_df, n_transactions=500):
        """Generate sales transactions"""
        transactions = []
        
        for i in range(n_transactions):
            # Random date within range
            days_offset = random.randint(0, (self.end_date - self.start_date).days)
            trans_date = self.start_date + timedelta(days=days_offset)
            
            # Select customer
            customer = customers_df.sample(1).iloc[0]
            
            # Number of items in order (restaurants order more)
            if customer['type'] == 'Restaurant':
                n_items = random.randint(3, 8)
            elif customer['type'] == 'Hotel':
                n_items = random.randint(4, 10)
            else:
                n_items = random.randint(1, 4)
            
            # Select products
            order_products = products_df.sample(n_items)
            
            for _, product in order_products.iterrows():
                quantity = random.randint(
                    product['min_order_qty'],
                    product['min_order_qty'] * 8
                )
                
                # Sometimes apply discount for large orders
                discount_pct = 0
                if quantity > 10:
                    discount_pct = random.choice([0, 0, 0, 5, 10])  # 40% no discount
                
                unit_price = product['price_clp']
                discount = unit_price * quantity * discount_pct / 100
                subtotal = (unit_price * quantity) - discount
                
                transactions.append({
                    'transaction_id': f'TRX{len(transactions)+1:06d}',
                    'date': trans_date,
                    'customer_id': customer['customer_id'],
                    'product_id': product['product_id'],
                    'quantity': quantity,
                    'unit_price_clp': unit_price,
                    'discount_pct': discount_pct,
                    'subtotal_clp': subtotal,
                    'cost_total_clp': product['cost_clp'] * quantity,
                    'profit_clp': subtotal - (product['cost_clp'] * quantity)
                })
        
        return pd.DataFrame(transactions)
    
    def generate_inventory_movements(self, products_df, days=30):
        """Generate inventory tracking data"""
        movements = []
        
        for _, product in products_df.iterrows():
            # Starting inventory
            current_stock = random.randint(20, 100)
            
            for day in range(days):
                date = self.end_date - timedelta(days=days-day)
                
                # Replenishment (every 5-7 days)
                if day % random.randint(5, 7) == 0:
                    restock = random.randint(30, 80)
                    current_stock += restock
                    movements.append({
                        'date': date,
                        'product_id': product['product_id'],
                        'movement_type': 'IN',
                        'quantity': restock,
                        'stock_after': current_stock,
                        'reason': 'Purchase Order'
                    })
                
                # Daily sales (reduce stock)
                daily_out = random.randint(2, 15)
                current_stock = max(0, current_stock - daily_out)
                movements.append({
                    'date': date,
                    'product_id': product['product_id'],
                    'movement_type': 'OUT',
                    'quantity': daily_out,
                    'stock_after': current_stock,
                    'reason': 'Sales'
                })
        
        return pd.DataFrame(movements)
    
    def _generate_name(self):
        """Generate Chilean names"""
        first_names = ['Carlos', 'María', 'José', 'Patricia', 'Luis', 'Carmen', 
                      'Miguel', 'Rosa', 'Juan', 'Andrea', 'Pedro', 'Claudia']
        last_names = ['González', 'Muñoz', 'Rojas', 'Silva', 'Pérez', 'Fernández',
                     'López', 'Martínez', 'Soto', 'Vargas']
        return f"{random.choice(first_names)} {random.choice(last_names)}"
    
    def export_all(self, output_dir='./alsur_data'):
        """Generate and export all datasets"""
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        print("Generating mock data for Comercializadora Al Sur...")
        
        # Generate datasets
        products = self.generate_products()
        customers = self.generate_customers()
        sales = self.generate_sales_transactions(products, customers)
        inventory = self.generate_inventory_movements(products)
        
        # Export to CSV
        products.to_csv(f'{output_dir}/products.csv', index=False)
        customers.to_csv(f'{output_dir}/customers.csv', index=False)
        sales.to_csv(f'{output_dir}/sales_transactions.csv', index=False)
        inventory.to_csv(f'{output_dir}/inventory_movements.csv', index=False)
        
        # Summary stats
        print(f"\n✓ Generated {len(products)} products")
        print(f"✓ Generated {len(customers)} customers")
        print(f"✓ Generated {len(sales)} sales transactions")
        print(f"✓ Generated {len(inventory)} inventory movements")
        print(f"\nFiles saved to: {output_dir}/")
        
        return products, customers, sales, inventory


# Run generator
if __name__ == "__main__":
    generator = AlSurDataGenerator(start_date='2024-01-01', months=12)
    products, customers, sales, inventory = generator.export_all()
    
    # Display samples
    print("\n=== PRODUCT SAMPLE ===")
    print(products.head())
    print("\n=== SALES SAMPLE ===")
    print(sales.head())