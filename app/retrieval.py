import json
import faiss
from sentence_transformers import SentenceTransformer

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load FAISS index
index = faiss.read_index("vectorstore/faiss.index")

# Load catalog
with open("data/catalog.json", "r", encoding="utf-8") as f:
    catalog = json.load(f)


def search_assessments(query, top_k=5):
    # Convert query to embedding
    query_embedding = model.encode([query])

    # Search FAISS
    distances, indices = index.search(query_embedding, top_k)

    results = []

    for idx in indices[0]:
        if idx < len(catalog):
            results.append(catalog[idx])

    return results

from app.chatbot import generate_response

if __name__ == "__main__":

    query = input("Recruiter Query: ")

    results = search_assessments(query)

    answer = generate_response(query, results)

    print("\n==============================\n")
    print(answer)