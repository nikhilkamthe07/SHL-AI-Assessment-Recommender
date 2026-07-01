import json
import faiss
from sentence_transformers import SentenceTransformer

# Load FAISS index
index = faiss.read_index("vectorstore/faiss.index")

# Load catalog
with open("data/catalog.json", "r", encoding="utf-8") as f:
    catalog = json.load(f)

# Model is loaded only when needed
model = None


def get_model():
    global model

    if model is None:
        model = SentenceTransformer("all-MiniLM-L6-v2")

    return model


def search_assessments(query, top_k=5):

    embedding_model = get_model()

    query_embedding = embedding_model.encode([query])

    distances, indices = index.search(query_embedding, top_k)

    results = []

    for idx in indices[0]:
        if idx < len(catalog):
            results.append(catalog[idx])

    return results


if __name__ == "__main__":

    from app.chatbot import generate_response

    query = input("Recruiter Query: ")

    results = search_assessments(query)

    answer = generate_response(query, results)

    print("\n=============================\n")
    print(answer)