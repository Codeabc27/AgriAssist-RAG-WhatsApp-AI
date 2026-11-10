try:
    from app.llm import generate_response
except ImportError:
    from llm import generate_response

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Dummy documents (replace with real agricultural data)
docs = [
    "Use drip irrigation to save water",
    "Apply urea fertilizer in small quantities",
    "Best crop for summer is maize",
]

# Generate embeddings and ensure FAISS receives float32 NumPy arrays
embeddings = np.asarray(
    model.encode(docs, convert_to_numpy=True),
    dtype=np.float32,
)

# Create the FAISS index
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)


def retrieve(query: str) -> list[str]:
    """Retrieve the two most relevant documents for a query."""
    q_embed = np.asarray(
        model.encode([query], convert_to_numpy=True),
        dtype=np.float32,
    )

    distances, indices = index.search(q_embed, k=2)

    results = []
    for i in indices[0]:
        if 0 <= int(i) < len(docs):
            results.append(docs[int(i)])

    return results


def rag_answer(query: str) -> str:
    """Generate an answer using retrieved agricultural context."""
    context = retrieve(query)

    prompt = f"""
Answer the user's question using the agricultural context below.

Context:
{chr(10).join(context)}

Question: {query}

Instructions:
- Give a clear, practical answer.
- If the context does not contain enough information, say so.
- Do not invent agricultural facts unsupported by the context.
"""

    return generate_response(prompt)
