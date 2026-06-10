import numpy
from sklearn.metrics.pairwise import cosine_similarity

def compute_similarity(matrix):
    return cosine_similarity(matrix)

def similar_products(similarity_matrix, product_index, k):
    products = similarity_matrix[product_index]
    sorted_list = numpy.argsort(products)[::-1]
    sorted_list = sorted_list[sorted_list != product_index]
    top_indices = sorted_list[:k]
    top_scores = products[top_indices]
    return list(zip(top_indices, top_scores))

