import os
import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
import fitz  # PyMuPDF

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Paths
INDEX_PATH = "embeddings/faiss_index.bin"
DOCS_PATH = "embeddings/docs.pkl"

# -----------------------------
# 📄 Load PDFs and Extract Text
# -----------------------------
def load_documents_from_pdf(folder_path="data/"):
    docs = []

    for file in os.listdir(folder_path):
        if file.endswith(".pdf"):
            pdf_path = os.path.join(folder_path, file)
            doc = fitz.open(pdf_path)

            for page in doc:
                text = page.get_text()

                # Simple cleaning
                text = text.strip()
                if len(text) > 50:  # avoid small noisy chunks
                    docs.append(text)

    return docs


# -----------------------------
# 🔢 Create Vector Store
# -----------------------------
def create_vector_store():
    docs = load_documents_from_pdf()

    print(f"📄 Loaded {len(docs)} document chunks")

    print("🔄 Creating embeddings...")
    embeddings = model.encode(docs)

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings))

    # Save
    os.makedirs("embeddings", exist_ok=True)
    faiss.write_index(index, INDEX_PATH)

    with open(DOCS_PATH, "wb") as f:
        pickle.dump(docs, f)

    print("✅ Vector store created successfully!")


# -----------------------------
# 📂 Load Vector Store
# -----------------------------
def load_vector_store():
    if not os.path.exists(INDEX_PATH):
        raise Exception("❌ Run create_vector_store() first")

    index = faiss.read_index(INDEX_PATH)

    with open(DOCS_PATH, "rb") as f:
        docs = pickle.load(f)

    return index, docs


# -----------------------------
# 🔍 Retrieve Docs
# -----------------------------
def retrieve_docs(query, top_k=3):
    index, docs = load_vector_store()

    query_embedding = model.encode([query])
    distances, indices = index.search(np.array(query_embedding), top_k)

    results = [docs[i] for i in indices[0]]
    return results


# -----------------------------
# 🧪 Test
# -----------------------------
if __name__ == "__main__":
    create_vector_store()

    query = "best fertilizer for rice"
    results = retrieve_docs(query)

    print("\n🔎 Query:", query)
    for r in results:
        print("-", r[:200])