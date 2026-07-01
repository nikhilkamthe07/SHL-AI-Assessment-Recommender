import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load catalog
with open("data/catalog.json", "r", encoding="utf-8") as f:
    catalog = json.load(f)

texts = []

for item in catalog:
    text = (
        item.get("name", "") +
        " " +
        item.get("description", "")
    )
    texts.append(text)

# Generate embeddings
embeddings = model.encode(texts)

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(np.array(embeddings))

faiss.write_index(index, "vectorstore/faiss.index")

print("✅ FAISS Index Created")

print("Total Assessments:", len(texts))