from app.recommender.content_based import embeddings
from sklearn.preprocessing import OneHotEncoder, normalize, StandardScaler, KBinsDiscretizer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from app.models import Product
from dotenv import load_dotenv
import pandas as pd
import numpy as np
import scipy.sparse as sp

def preprocess_database(database):

    df = pd.DataFrame(database)
    
    string_columns = list(Product.model_fields.keys())
    string_columns_simple = [x for x in string_columns if x not in ["name","tags","description", "price"]]

    #ONE HOT ENCODING
    preprocessor = ColumnTransformer(
        transformers=[
            ("string", OneHotEncoder(handle_unknown="ignore"), string_columns_simple)
        ])
    pipeline = Pipeline(steps=[("preprocessor", preprocessor)])
    
    structured_matrix = pipeline.fit_transform(df)

    #EMBEDDINGS
    embeddings_ = embeddings.load_embeddings()
    if embeddings_ is None or len(embeddings_) != len(df):
        embeddings_ = embeddings.generate_db_embeddings(df) 
        embeddings.save_embeddings(embeddings_) 

    #COMBINE
    if sp.issparse(structured_matrix):
        structured_matrix = structured_matrix.toarray()
    combined = np.hstack([structured_matrix, embeddings_])

    feature_names = pipeline.named_steps["preprocessor"].get_feature_names_out()
    weight_vector = build_weights_vector(feature_names)
    combined = combined * weight_vector
    combined = normalize(combined, norm="l2")
    return df, combined, pipeline


def build_weights_vector (feature_names, n_embeddings_dims=1024):
    category_weights={
        "subcategory": 4.0,
        "style":2.5,
        "gender":3.0,
        "usage":2.0,
        "fit":2.0,
        "fabric":3.0,
        "age_group":3.0,
        "category":3.0,
        "brand":0.5,
        "color":0.5,

    }

    weights = []
    for name in feature_names:
        part = name.split("__")[1]
        category = None
        for cat in category_weights.keys():
            if part.startswith(cat):
                category = cat
                break
        
        weight = category_weights.get(category, 1.0) if category else 1.0
        weights.append(weight)

    embedding_weight = 2.0
    embedding_weights = [embedding_weight] * n_embeddings_dims
    weights.extend(embedding_weights)

    return np.array(weights)

def get_product_index_in_df(product_id, df):
    product_index = df.index[df["id"] == product_id][0]
    return product_index

    
