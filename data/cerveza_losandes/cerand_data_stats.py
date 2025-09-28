import pandas as pd
from contextlib import redirect_stdout
from pathlib import Path

# Import db data
from cerand_db import *

# Read data
df = pd.read_csv('data/cerveza_losandes/cerveza_losandes_transactions.csv')

# Ensure output directory exists and open file to capture prints
output_path = Path('data/cerveza_losandes/cerveza_losandes_stats.txt')
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

        print(f"\nSales channel breakdown:")
        channel_revenue = df.groupby('channel')['total'].sum().sort_values(ascending=False)
        for channel, revenue in channel_revenue.items():
            print(f"  {channel}: ${revenue:,.0f}")

        print(f"\nCategory breakdown by revenue:")
        category_revenue = df.merge(
            pd.DataFrame([(k, v['category']) for k, v in products.items()], 
                        columns=['producto', 'category']), 
            on='producto'
        ).groupby('category')['total'].sum().sort_values(ascending=False)

        for category, revenue in category_revenue.items():
            print(f"  {category}: ${revenue:,.0f}")

        print(f"\nB2B customers analysis:")
        if 'customer' in df.columns:
            b2b_revenue = df[df['channel'] == 'DISTRIBUTOR_B2B'].groupby('customer')['total'].sum().sort_values(ascending=False)
            for customer, revenue in b2b_revenue.items():
                print(f"  {customer}: ${revenue:,.0f}")

        print(f"\nFailed experiments and dead inventory:")
        failed_products = df[df['producto'].str.startswith(('FAIL', 'OLD'))].groupby(['producto', 'glosa'])['total'].sum().sort_values(ascending=True)
        for (code, name), revenue in failed_products.items():
            print(f"  {code}: {name[:30]}... - ${revenue:,.0f}")

print(f"Statistics saved to '{output_path}'")
