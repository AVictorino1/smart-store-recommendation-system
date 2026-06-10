from app.recommender.content_based import preprocessing
from app.recommender.content_based import embeddings
from app.recommender.content_based import similarity
from app.recommender.content_based import filters
from app.services.product_service import get_products
from app.services.product_service import get_product_id
from app.recommender.rule_based import best_recommendations
from app.models import Product


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


if __name__ == "__main__":
    main()



