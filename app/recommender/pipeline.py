from app.recommender.content_based import preprocessing
from app.recommender.content_based import embeddings
from app.recommender.content_based import similarity
from app.recommender.content_based import filters
from app.services.product_service import get_products
from app.services.product_service import get_product_id
from app.recommender.rule_based import best_recommendations
from app.models import Product
import pandas as pd


def main():
    print("")


def recomm(product_id):
    
    k = 4
    df, processed, pipeline = preprocessing.preprocess_database(get_products())
    product_index = df.index[df["id"] == product_id][0]
    filtered = filters.price_filter(product_index,df)
    filtered_indices = filtered.index
    filtered_processed = processed[filtered_indices]
    similarity_matrix = similarity.compute_similarity(filtered_processed)

    new_index = list(filtered_indices).index(product_index)
    
    recommendations = similarity.similar_products(similarity_matrix, new_index, k)
    indices_with_scores = [(filtered_indices[int(i)], score) for i, score in recommendations]
    recommendations = [int(filtered_indices[int(i)]) for i, score in recommendations]
    
    print("filtered_indices:", filtered_indices.tolist())
    print("recommendations:", recommendations)
    
    #SCORES
    for idx, score in indices_with_scores:
        real_id = df[df.index == idx]["id"].values[0]
        print(f"Buscando id: {real_id}, score: {round(score, 3)}")
        product = get_product_id(int(real_id))
        print(f"Score: {round(score, 3)} | {product["id"]}")

    #RECOMMENDATIONS REQUEST
    recomm_ids = [x for x in df.loc[recommendations]["id"]]
    print("recomm_ids:", recomm_ids)
    products_recomm = []
    for id in recomm_ids:
        products_recomm.append(get_product_id(id))
    
    print(df[["id"]].head(5))
    return products_recomm


    #print([get_product_id(n) for n in best_recommendations(get_product_id(product_id),get_products())])

#Add variable to recognize between product search and recommendations
def search_by_text(query: str, k: int = 3, filters: dict = None):
    df, processed, _ = preprocessing.preprocess_database(get_products())

    filtered_df = df.copy()

    if filters:
        if filters.get("gender"):
            filtered_df = filtered_df[
                filtered_df["gender"].isin([filters["gender"], "unisex"])
            ]
        if filters.get("category"):
            filtered_df = filtered_df[
                filtered_df["category"] == filters["category"]
            ]

        if filters.get("color"):
            filtered_df = filtered_df[
                filtered_df["color"] == filters["color"]
            ]
        if filters.get("price_max"):
            filtered_df = filtered_df[
                filtered_df["price"] <= filters["price_max"]
            ]
    
    if filtered_df.empty:
        return pd.DataFrame()

    filtered_indices = filtered_df.index.tolist()

    query_embedding = embeddings.get_query_embedding(query)
    catalog_embeddings = embeddings.load_embeddings()

    if catalog_embeddings is None:
        return pd.DataFrame()
    
    filtered_embeddings = catalog_embeddings[filtered_indices]


    recommendations = similarity.similar_to_query(query_embedding, filtered_embeddings, k)

    top_positions = [filtered_indices[int(i)] for i, score in recommendations if score >= 0.5]
    
    if not top_positions:
        return pd.DataFrame()
    
    for i, (idx, score) in enumerate(recommendations):
        real_idx = filtered_indices[int(idx)]
        real_id = df.loc[real_idx]["id"]
        print(f"Score: {round(score, 3)} | id: {real_id}")
    
    return df.loc[top_positions]

if __name__ == "__main__":
    main()



