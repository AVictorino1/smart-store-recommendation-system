import numpy
from sklearn.metrics.pairwise import cosine_similarity

def compute_similarity(matrix):
    return cosine_similarity(matrix)


def search_product(similarity_matrix, product_index, k):
    products = similarity_matrix[product_index]
    sorted_list = numpy.argsort(products)[::-1]
    sorted_list = sorted_list[sorted_list == product_index]
    top_indices = sorted_list[:k]
    top_scores = products[top_indices]
    return list(zip(top_indices, top_scores))


def similar_products(similarity_matrix, product_index, k):
    products = similarity_matrix[product_index]
    sorted_list = numpy.argsort(products)[::-1]
    sorted_list = sorted_list[sorted_list != product_index]
    top_indices = sorted_list[:k]
    top_scores = products[top_indices]
    return list(zip(top_indices, top_scores))

def similar_to_query(query_embedding, catalog_embeddings, k):
    similarities = cosine_similarity(
        query_embedding.reshape(1,-1),
        catalog_embeddings
    )[0]
    
    top_indices = numpy.argsort(similarities)[::-1][:k]
    top_scores = similarities[top_indices]
    if top_scores[0] < 0.5:
        return list()
    return list(zip(top_indices, top_scores))

