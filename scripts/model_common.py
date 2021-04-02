import pandas as pd

from store.models import Store
from products.models import ProductAttributes

DOT = 'dot'
COSINE = 'cos'
EUCLIDEAN = 'euc'

def get_top_k_for_each(embeddings, ids, k, method='DOT'):
    '''
    Gets top k results for each id provided in the ids parameter (its a list)
    '''
    #define query and items embeddings
    
    data = []
    for id_ in tqdm(ids):
        df = get_top_k(embeddings, id_, k, method)
        df['ORIGINAL_PRODUCT_CODE'] = item_encoded2item[id_]
        df['ORIGINAL_PRODUCT_NAME'] = df['ORIGINAL_PRODUCT_CODE'].apply(lambda x: item2item_name[x])
        data.append(df.copy())
    
    return pd.concat(data)

def get_top_k(embeddings, query_id, k, method=DOT):
    '''
    Gets top K results for a query_id (closest product vectors)
    '''
    #define query and items embeddings
    query = embeddings[query_id]
    items = embeddings
    #print(f"Querying {k} products most similar to: {item2item_name[item_encoded2item[query_id]]}")

    #Compute distance
    if method == DOT:
        all_distances = pd.DataFrame({'PRODUCT_DISTANCE_TO_QUERY': items.dot(query)})
    elif method == COSINE:
        #items = items / np.linalg.norm(items[:, np.newaxis], axis=1)
        items = items / np.linalg.norm(items[:, np.newaxis], axis=1, keepdims=True)
        query = query / np.linalg.norm(query)
        items = items[items != np.inf]
        print(items.shape)
        all_distances = pd.DataFrame({'PRODUCT_DISTANCE_TO_QUERY': items.dot(query)})
    elif method == EUCLIDEAN:
        query = np.array([query]*len(items))
        print(query.shape)
        print(items.shape)
        all_distances = pd.DataFrame({'PRODUCT_DISTANCE_TO_QUERY': np.linalg.norm(query - items, axis=1)})
    else:
        raise ValueError(f'Method {method} is not defined. Please use DOT, COS or EUCLIDEAN')

    #Transform Dataset
    all_distances = all_distances.sort_values('PRODUCT_DISTANCE_TO_QUERY', ascending=False)
    all_distances = all_distances[all_distances.index != query_id]
    all_distances.index = all_distances.index.map(item_encoded2item)
    all_distances['RECOMMENDED_PRODUCT_ID'] = all_distances.index
    all_distances['RECOMMENDED_PRODUCT_NAME'] = all_distances.index.map(item2item_name) 

    return all_distances.iloc[:min(k, len(all_distances))]

def send_to_db(df, company_name, django_model):
    deleted_ids = []
    company = Store.objects.get(company=company_name)
    for _, row in df.iterrows():
        product = ProductAttributes.objects.get(name=row.name, company__company=row.company)
        recommendation = ProductAttributes.objects.get(name=row.name, company__company=row.company)
            
        if product.id not in deleted_ids:
            deleted_ids.append(product.id)
            django_model.objects.filter(
                product_code=product
            ).delete()
        
        django_model.objects.create(
            product_code=product,
            recommended_code=recommendation,
            company=company,
            distance=row.distance
        )

def get_products_df(client):
    products_data = ProductAttributes.objects.filter(company__company=client).all()
    products_json = [product.as_dict() for product in products_data]
    products_df = pd.DataFrame().from_records(products_json)
    return products_df