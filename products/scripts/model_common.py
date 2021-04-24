import pandas as pd
import time
import os
import tensorflow as tf
from store.models import Store, Customers
from tqdm import tqdm
from products.scripts.cactus.ml import CollaborativeFiltering
from products.models import ProductAttributes, OrderAttributes, CustomerPredictions
import logging 

DOT = 'dot'
COSINE = 'cos'
EUCLIDEAN = 'euc'

ITEM = 'product_id'
BILL = 'bill'
USER = 'customer'
ITEM_NAME = 'product_name'
QTY = 'product_qty'

logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.StreamHandler()
        ]
    )

logger = logging.getLogger(__name__)

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
    logger.info(f"Querying {k} products most similar to encoded id: {query_id}")

    #Compute distance
    if method == DOT:
        all_distances = pd.DataFrame({'distance': items.dot(query)})
    elif method == COSINE:
        #items = items / np.linalg.norm(items[:, np.newaxis], axis=1)
        items = items / np.linalg.norm(items[:, np.newaxis], axis=1, keepdims=True)
        query = query / np.linalg.norm(query)
        items = items[items != np.inf]
        logger.info(items.shape)
        all_distances = pd.DataFrame({'distance': items.dot(query)})
    elif method == EUCLIDEAN:
        query = np.array([query]*len(items))
        logger.info(query.shape)
        logger.info(items.shape)
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
            prod = ProductAttributes.objects.get(id=row.product_id, company=company)
            recommendation = ProductAttributes.objects.get(id=row.recommended_id, company=company)
        except ProductAttributes.DoesNotExist as dne:
            logger.error(dne)
            continue
        except ProductAttributes.MultipleObjectsReturned as mor:
            logger.error(mor)
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

def send_personalization_to_db(df, store_name):
    deleted_ids = []
    store = Store.objects.get(company=store_name)
    for _, row in tqdm(df.iterrows(), total=len(df)):
        try:
            customer = Customers.objects.get(email=row.customer, store=store)
            recommendation = ProductAttributes.objects.get(id=row.product_id, company=store)
        except ProductAttributes.DoesNotExist as dne:
            logger.error(dne)
            continue
        except ProductAttributes.MultipleObjectsReturned as mor:
            logger.error(mor)
            continue


        if customer.id not in deleted_ids:
            deleted_ids.append(customer.id)
            CustomerPredictions.objects.filter(
                recommended_code=recommendation
            ).delete()
        
        CustomerPredictions.objects.create(
            customer=customer,
            recommended_code=recommendation,
            rate=row.rates,
            company=store
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
    logger.info(products_json)
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
    
    logger.info(f"Users: {N}, Items: {M}")
    run_logdir = get_run_logdir()
    tensorboard_cb = tf.keras.callbacks.TensorBoard(run_logdir)
    model = CollaborativeFiltering(12, N, M)
    
    logger.info(f"Compiling model")
    model.compile(
        loss=tf.keras.losses.BinaryCrossentropy(),
        optimizer=tf.optimizers.Adam(lr=0.001),
        metrics=[tf.keras.metrics.MeanAbsolutePercentageError()]
    )
    
    train_df, val_df, _ = split_dataframe(ratings)

    logger.info(f"Training model")
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

def rate_items_for_user(model, user_id, item_ids):
    rates = []
    for id_ in item_ids:
        rates.append(model.predict(user_id))
    return rates
