import pandas as pd
from contextlib import redirect_stdout
from pathlib import Path

# Import db data
from autpar_db import products

# Read data
df = pd.read_csv('data/auto_partes/auto_partes_transactions.csv')

# Ensure output directory exists and open file to capture prints
output_path = Path('data/auto_partes/auto_partes_stats.txt')
output_path.parent.mkdir(parents=True, exist_ok=True)

with output_path.open('w', encoding='utf-8') as out:
    with redirect_stdout(out):

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
            
print(f"Statistics saved to '{output_path}'")