import pandas as pd
from contextlib import redirect_stdout
from pathlib import Path

# Import db data
from comer_db import *

# Read data
df = pd.read_csv('data/comercializadora/comercializadora_transactions.csv')

# Ensure output directory exists and open file to capture prints
output_path = Path('data/comercializadora/comercializadora_stats.txt')
output_path.parent.mkdir(parents=True, exist_ok=True)

with output_path.open('w', encoding='utf-8') as out:
    with redirect_stdout(out):

        # Generate summary statistics
        print(f"\nDataset Summary:")
        print(f"Total transactions: {len(df)}")
        print(f"Total revenue: ${df['total'].sum():,.0f} CLP")
        print(f"Average transaction value: ${df.groupby('trans_id')['total'].sum().mean():,.0f} CLP")
        print(f"Price range: ${df['total'].min():,.0f} - ${df['total'].max():,.0f} CLP")

        print(f"\nTop 10 products by revenue:")
        top_products = df.groupby(['producto', 'glosa'])['total'].sum().sort_values(ascending=False).head(10)
        for (code, name), revenue in top_products.items():
            print(f"  {code}: {name[:35]}... - ${revenue:,.0f}")

        print(f"\nTop 10 customers by revenue:")
        top_customers = df.groupby(['customer_id', 'customer_name'])['total'].sum().sort_values(ascending=False).head(10)
        for (cid, name), revenue in top_customers.items():
            print(f"  {cid}: {name[:35]}... - ${revenue:,.0f}")

        print(f"\nCategory breakdown by revenue:")
        category_revenue = df.merge(
            pd.DataFrame([(k, v['category']) for k, v in products.items()], 
                        columns=['producto', 'category']), 
            on='producto'
        ).groupby('category')['total'].sum().sort_values(ascending=False)

        for category, revenue in category_revenue.items():
            print(f"  {category}: ${revenue:,.0f}")

        print(f"\nLocation breakdown by revenue:")
        location_revenue = df.groupby('customer_location')['total'].sum().sort_values(ascending=False)
        for location, revenue in location_revenue.items():
            print(f"  {location}: ${revenue:,.0f}")

        print(f"\nDead inventory items:")
        dead_items = df[df['producto'].str.startswith('DEAD')].groupby(['producto', 'glosa'])['total'].sum().sort_values(ascending=True)
        if len(dead_items) > 0:
            for (code, name), revenue in dead_items.items():
                print(f"  {code}: {name[:30]}... - ${revenue:,.0f}")
        else:
            print("  No dead inventory sales in this period")

        # Save to CSV
        df_output = df[['trans_id', 'fecha', 'producto', 'glosa', 'costo', 'total', 'cantidad', 'inith', 'initm']]
        df_output.to_csv('comercializadora_alsur_transactions.csv', index=False)
        print(f"\nCSV file saved as 'comercializadora_alsur_transactions.csv'")

        print(f"\nPeak season analysis (December):")
        december_data = df[df['fecha'].str.contains('12/')]
        if len(december_data) > 0:
            print(f"December revenue: ${december_data['total'].sum():,.0f}")
            print(f"December transactions: {len(december_data)}")
            print(f"Average December order: ${december_data.groupby('trans_id')['total'].sum().mean():,.0f}")
        
print(f"Statistics saved to '{output_path}'")