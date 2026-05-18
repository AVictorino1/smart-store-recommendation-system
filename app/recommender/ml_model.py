from sklearn.preprocessing import OneHotEncoder, Normalizer, StandardScaler, KBinsDiscretizer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics.pairwise import cosine_similarity
from app.services.product_service import get_products
from app.services.product_service import get_product_id
from app.recommender.rule_based import best_recommendations
from app.models import Product
import numpy
import pandas as pd

def main():
    product_id = 3
    df, processed, pipeline = preprocess_database(get_products())
    product_index = df.index[df["id"] == product_id][0]
    k = 4
    filtered = price_filter(product_index,df)
    filtered_indices = filtered.index
    filtered_processed = processed[filtered_indices]
    similarity_matrix = cosine_similarity(filtered_processed)

    new_index = list(filtered_indices).index(product_index)
    
    recommendations = similar_products(similarity_matrix, new_index, k)

    recommendations = [filtered_indices[i] for i in recommendations]
    print(get_product_id(product_id))
    print(df.iloc[recommendations])
    print([get_product_id(n) for n in best_recommendations(get_product_id(product_id),get_products())])



def preprocess_database(database):

    df = pd.DataFrame(database)
    
    string_columns = list(Product.model_fields.keys())
    
    num_columns = ["price"]

    
    preprocessor = ColumnTransformer(
        transformers=[
            ("string", OneHotEncoder(handle_unknown="ignore"), string_columns)
        ])
    pipeline = Pipeline(steps=[("preprocessor", preprocessor)])
    
    processed = pipeline.fit_transform(df)

    return df, processed, pipeline

def price_filter(product_index, df):
    product = df.iloc[product_index]
    filtered = df[(df["price"] >= 0.7 * product["price"]) & (df["price"] <= 1.3 * product["price"])]
    return filtered

def similar_products(similarity_matrix, product_index, k):
    products = similarity_matrix[product_index]
    sorted_list = numpy.argsort(products)[::-1]
    sorted_list = sorted_list[sorted_list != product_index]
    
    return sorted_list[:(k+1)]

    


if __name__ == "__main__":
    main()
