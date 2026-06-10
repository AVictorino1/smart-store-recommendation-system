import os
from dotenv import load_dotenv
import time
import numpy as np
import cohere

load_dotenv()
cohere_api_key = os.getenv("COHERE_API_KEY")
MODEL = "embed-multilingual-v3.0"
client = cohere.Client(cohere_api_key)


def generate_db_embeddings(df) -> np.ndarray:
    texts = [build_semantic_text(row) for _, row in df.iterrows()]
    embeddings = []
    batch_size = 96

    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        try:
            response = client.embed(
                texts=batch,
                model=MODEL,
                input_type="search_document"
            )
            embeddings.extend(response.embeddings)
            print(f"Procesados {min(i + batch_size, len(texts))}/{len(texts)}")

        except Exception as e:
            print(f"Error en item {i}: {e}")
            for _ in batch:
                embeddings.append(np.zeros(1024).tolist())

        time.sleep(0.5)

    return np.vstack(embeddings)


def add_product_embedding(row, path: str = "embeddings.npy") -> np.ndarray:
    embeddings = load_embeddings(path)
    
    text = build_semantic_text(row)
    new_embedding = get_embedding(text, input_type="search_document")
    new_embedding = new_embedding.reshape(1,-1)
    
    if embeddings is not None:
        updated = np.vstack([embeddings, new_embedding])
    else:
        updated = new_embedding

    save_embeddings(updated, path)

    return updated




def build_semantic_text(row):
    name = row["name"] or ""
    description = row["description"] or ""
    tags = row["tags"]
    if isinstance(tags, list):
        tags = " ". join(tags)
    elif tags is None:
        tags = ""
    
    

    return f"{name} {tags} {description}".strip()

def get_embedding(text: str, input_type: str) -> np.ndarray:
    response = client.embed(
        texts=[text],
        model=MODEL,
        input_type=input_type
    )
    return np.array(response.embeddings[0])

def get_query_embedding(query: str) -> np.ndarray:
    response = client.embed(
        texts=[query],
        model=MODEL,
        input_type="search_query"
    )
    return np.array(response.embeddings[0])

def save_embeddings(embeddings: np.ndarray, path: str = "embeddings.npy"):
    np.save(path,embeddings)
    print(f"Embeddings guardados en {path}")

def load_embeddings(path: str = "embeddings.npy") -> np.ndarray:
    if os.path.exists(path):
        return np.load(path)
    
    return None
    
def delete_embedding(product_index, path: str = "embeddings.npy"):
    embeddings = load_embeddings(path)
    if embeddings is None:
        return None
    
    updated = np.delete(embeddings, product_index, axis=0)
    save_embeddings(updated, path)
    return updated

def update_embedding(product_index, row, path: str = "embeddings.npy"):
    embeddings = load_embeddings(path)
    if embeddings is None:
        return None
    
    text = build_semantic_text(row)
    new_embedding = get_embedding(text, input_type="search_document")
    embeddings[product_index] = new_embedding
    save_embeddings(embeddings, path)

    return embeddings
