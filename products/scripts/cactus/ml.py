import tensorflow as tf

class CollaborativeFiltering(tf.keras.Model):
    def __init__(self, embedding_dim, num_users, num_items, **kwargs):
        super(CollaborativeFiltering, self).__init__(**kwargs)
        
        self.num_users = num_users
        self.num_items = num_items
        self.embedding_dim = embedding_dim
        
        self.user_embedding = tf.keras.layers.Embedding(
            num_users, 
            embedding_dim, 
            embeddings_initializer='he_normal',
            embeddings_regularizer=tf.keras.regularizers.l2(1e-6)
        )
        self.user_bias = tf.keras.layers.Embedding(num_users, 1)
        
        self.item_embedding = tf.keras.layers.Embedding(
            num_items, 
            embedding_dim, 
            embeddings_initializer='he_normal',
            embeddings_regularizer=tf.keras.regularizers.l2(1e-6)
        )
        self.item_bias = tf.keras.layers.Embedding(num_items, 1)
        

    def call(self, inputs):
        user_vector = self.user_embedding(inputs[:, 0])
        user_bias = self.user_bias(inputs[:,0])
        
        item_vector = self.item_embedding(inputs[:, 1])
        item_bias = self.item_bias(inputs[:, 1])
        
        dot_product = tf.tensordot(user_vector, item_vector, 2)
        x = dot_product + item_bias + user_bias
        return x
    
    def get_config(self):
        base_config = super().get_config()
        return {
            **base_config,
            "embedding_dim": self.embedding_dim,
            "num_users": self.num_users,
            "num_items": self.num_items  
        }
