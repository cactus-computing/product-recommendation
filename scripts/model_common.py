import pandas as pd
import time
import os
import tensorflow as tf
from store.models import Store
from tqdm import tqdm
from scripts.cactus.ml import CollaborativeFiltering
from products.models import ProductAttributes, OrderAttributes

DOT = 'dot'
COSINE = 'cos'
EUCLIDEAN = 'euc'

ITEM = 'product_name'
BILL = 'bill'
USER = 'user'
QTY = 'product_qty'


def split_dataframe(df, holdout_fraction=0.2, val_fraction = 0.5):
    '''
    Splits the dataset into 3 datasets: train, val and test datasets
    '''
    test = df.sample(frac=holdout_fraction, replace=False)
    val = df.sample(frac=val_fraction, replace=False)
    train = df[~df.index.isin(test.index)]
    test = test[~test.index.isin(val.index)]
    return train, val, test

def get_top_k_for_each(embeddings, ids, k, method='DOT'):
    '''
    Gets top k results for each id provided in the ids parameter (its a list)
    '''
    #define query and items embeddings
    
    data = []
    for id_ in ids:
        df = get_top_k(embeddings, id_, k, method)
        df['product_id'] = id_
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
        all_distances = pd.DataFrame({'distance': items.dot(query)})
    elif method == COSINE:
        #items = items / np.linalg.norm(items[:, np.newaxis], axis=1)
        items = items / np.linalg.norm(items[:, np.newaxis], axis=1, keepdims=True)
        query = query / np.linalg.norm(query)
        items = items[items != np.inf]
        print(items.shape)
        all_distances = pd.DataFrame({'distance': items.dot(query)})
    elif method == EUCLIDEAN:
        query = np.array([query]*len(items))
        print(query.shape)
        print(items.shape)
        all_distances = pd.DataFrame({'distance': np.linalg.norm(query - items, axis=1)})
    else:
        raise ValueError(f'Method {method} is not defined. Please use DOT, COS or EUCLIDEAN')

    #Transform Dataset
    all_distances = all_distances.sort_values('distance', ascending=False)
    all_distances = all_distances[all_distances.index != query_id]
    
    all_distances['recommended_id'] = all_distances.index

    return all_distances.iloc[:min(k, len(all_distances))]

def send_to_db(df, company_name, django_model):
    deleted_ids = []
    company = Store.objects.get(company=company_name)
    for _, row in tqdm(df.iterrows(), total=len(df)):
        try:
            prod = ProductAttributes.objects.get(name=row.product_name, company=company)
            recommendation = ProductAttributes.objects.get(name=row.recommended_name, company=company)
        except ProductAttributes.DoesNotExist:
            continue
        except ProductAttributes.MultipleObjectsReturned:
            continue


        if prod.id not in deleted_ids:
            deleted_ids.append(prod.id)
            django_model.objects.filter(
                product_code=prod
            ).delete()
        
        django_model.objects.create(
            product_code=prod,
            recommended_code=recommendation,
            company=company,
            distance=row.distance
        )

def get_products_df(client):
    products_data = ProductAttributes.objects.filter(company__company=client).all()
    products_json = [product.as_dict() for product in products_data]
    products_df = pd.DataFrame().from_records(products_json)
    return products_df

def get_run_logdir():
    '''
    Create run file name
    '''
    root_logdir = os.path.join(os.curdir, "tf_logs")
    run_id = time.strftime("run_%Y_%m_%d_-%H_%M_%S")
    return os.path.join(root_logdir, run_id)

def get_orders(client):
    products_data = OrderAttributes.objects.filter(company__company=client).all()
    products_json = [product.as_dict() for product in products_data]
    products_df = pd.DataFrame().from_records(products_json)
    return products_df

def train_collaborative_filters(ratings, n, m, client, build=False):
    '''
    Model training lifecycle
    '''
    if not build:
        model = tf.keras.models.load_model(f"trained_models/{client}/collaborative_filtering")
        history = None
        return model, history
    
    N = n
    M = m
    
    print(f"Users: {N}, Items: {M}")
    run_logdir = get_run_logdir()
    tensorboard_cb = tf.keras.callbacks.TensorBoard(run_logdir)
    model = CollaborativeFiltering(64, N, M)
    
    print(f"Compiling model")
    model.compile(
        loss=tf.keras.losses.BinaryCrossentropy(),
        optimizer=tf.optimizers.Adam(lr=0.001),
        metrics=[tf.keras.metrics.MeanAbsolutePercentageError()]
    )
    
    train_df, val_df, _ = split_dataframe(ratings)

    print(f"Training model")
    history = model.fit(
        x=train_df[[USER, ITEM]].values,
        y=train_df[[QTY]].values,
        batch_size=64,
        epochs=6,
        verbose=1,
        validation_data=(val_df[[USER, ITEM]].values, val_df[[QTY]].values),
        callbacks=[
            tf.keras.callbacks.EarlyStopping(),
            tensorboard_cb,
        ]
    )
    
    return model, history
