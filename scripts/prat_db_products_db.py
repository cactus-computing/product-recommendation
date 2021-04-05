import pandas as pd
from django.db.utils import IntegrityError
from datetime import datetime 
from tqdm import tqdm
from store.models import Store
from products.models import ProductAttributes

file_name = 'gs://cactus_recommender/prat/prat_product_db.csv'

df = pd.read_csv(file_name)
df = df[df['company'] == 'prat']
company = Store.objects.get(company='prat')
skus = []
skus_in_db = ProductAttributes.objects.all().filter(company=company)
for obj in skus_in_db:
    skus.append(obj.sku)

for e, row in tqdm(df.iterrows()):
    print(row["sku"])
    if row["sku"] not in skus:
        print(row["sku"])
        try:
            print(ProductAttributes.objects.update_or_create(
                sku=row["sku"],
                company=company,
                defaults={
                    'product_code':row["product_code"],
                    'name':row["name"],
                    'permalink': row['permalink'],
                    'img_url': row['href'],
                    'stock_quantity': True if row['stock_quantity'] == 1.0 else False,
                    'status': 'active',
                    'price': row['price'],
                    'product_created_at': datetime.now()
                }
            ))
        except IntegrityError as f:
            print(f)
            continue
