import pandas as pd
from contextlib import redirect_stdout
from pathlib import Path

# Import db data
from cafand_db import *

# Read data
df = pd.read_csv('data/cafe_andino/cafe_andino_transactions.csv')

# Ensure output directory exists and open file to capture prints
output_path = Path('data/cafe_andino/cafe_andino_stats.txt')
output_path.parent.mkdir(parents=True, exist_ok=True)

with output_path.open('w', encoding='utf-8') as out:
    with redirect_stdout(out):

        # Generate summary statistics
        print(f"\nDataset Summary:")
        print(f"Total transactions: {len(df)}")
        print(f"Total revenue: ${df['total'].sum():,.0f}")
        print(f"Average transaction value: ${df.groupby('trans_id')['total'].sum().mean():,.0f}")
        print(f"Top 5 products by revenue:")
        top_products = df.groupby(['producto', 'glosa'])['total'].sum().sort_values(ascending=False).head()
        for (code, name), revenue in top_products.items():
            print(f"  {code}: {name} - ${revenue:,.0f}")
            
print(f"Statistics saved to '{output_path}'")
