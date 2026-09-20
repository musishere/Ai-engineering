# What it does:
# Takes a small corpus (20-50 short documents)
# Embeds each document using an embedding model
# Stores the embeddings in memory (a list is fine)
# Takes a user query
# Embeds the query with the same model
# Computes cosine similarity between the query and every document
# Returns the top 3 most similar documents

from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

DOCS_DIR = Path(__file__).parent / "documents"

paths = sorted(DOCS_DIR.glob("*.txt"))
documents = [p.read_text() for p in paths]
print(f"[load] read {len(documents)} documents from {DOCS_DIR}")

vectorizer = TfidfVectorizer(stop_words="english")
doc_embeddings = [row.toarray()[0] for row in vectorizer.fit_transform(documents)]
print(f"[embed] stored {len(doc_embeddings)} embeddings, dim={len(doc_embeddings[0])}")


def search(query: str, top_k: int = 3):
    query_embedding = vectorizer.transform([query]).toarray()[0]
    print(f"[embed] query embedded, dim={len(query_embedding)}")
    scores = cosine_similarity([query_embedding], doc_embeddings)[0]
    print(f"[similarity] scores computed for {len(scores)} documents")
    top_indices = scores.argsort()[::-1][:top_k]
    print(f"[search] top {top_k}: {[paths[i].name for i in top_indices]}")
    return [(paths[i].name, scores[i], documents[i]) for i in top_indices]


if __name__ == "__main__":
    query = input("Query: ")
    for name, score, text in search(query):
        print(f"\n[{name}] score={score:.3f}")
        print(text[:200].strip())