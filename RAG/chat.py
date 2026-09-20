# Build: A complete RAG system from scratch.
# What it does:
# Ingest: Load 10–20 documents
# Chunk: Split into chunks (start with fixed-size, ~200 tokens)
# Embed: Embed each chunk (use fastembed if Python 3.14 blocks PyTorch)
# Store: In a list (in-memory)
# Retrieve: Embed the query, find top 3 chunks
# Generate: Stuff chunks into a prompt, call the LLM, get the answer
# Constraints:
# No frameworks
# Same embedding model for docs and queries
# Show retrieved chunks before generating
# Include "no answer" fallback
# Success criteria:
# "How do I reset my password?" → correct answer
# You can see the 3 retrieved chunks
# Off-topic question → "I don't have enough information"
# Stretch goal:
# Log the full prompt token count
# Calculate cost per query
# Compare 3 chunks vs 5 chunks

import json
import os
import ssl
import urllib.request
import certifi
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())

DOCS_DIR = Path(__file__).parent / "documents"
ENV_PATH = Path(__file__).parent / ".env"
GROQ_MODEL = "openai/gpt-oss-20b"
NO_ANSWER_THRESHOLD = 0.05  # below this, don't bother calling the LLM


def load_env():
    for line in ENV_PATH.read_text().splitlines():
        if "=" in line and not line.startswith("#"):
            key, _, value = line.partition("=")
            os.environ.setdefault(key.strip(), value.strip())


def load_documents():
    paths = sorted(DOCS_DIR.glob("*.txt"))
    print(f"[load] found {len(paths)} files in {DOCS_DIR}")
    documents = []
    for path in paths:
        text = path.read_text()
        print(f"[load] {path.name}: {len(text.split())} words")
        documents.append({"source": path.name, "text": text})
    print(f"[load] loaded {len(documents)} documents")
    return documents


CHUNK_SIZE = 200  # tokens, approximated as whitespace-split words


def chunk_documents(documents, chunk_size=CHUNK_SIZE):
    chunks = []
    for doc in documents:
        words = doc["text"].split()
        num_chunks = 0
        for start in range(0, len(words), chunk_size):
            chunk_words = words[start:start + chunk_size]
            chunks.append({
                "source": doc["source"],
                "chunk_index": num_chunks,
                "text": " ".join(chunk_words),
            })
            num_chunks += 1
        print(f"[chunk] {doc['source']}: {len(words)} words -> {num_chunks} chunk(s)")
    print(f"[chunk] created {len(chunks)} chunks total")
    return chunks


vectorizer = TfidfVectorizer(stop_words="english")


def embed_chunks(chunks):
    texts = [chunk["text"] for chunk in chunks]
    vectors = vectorizer.fit_transform(texts)
    chunk_embeddings = [row.toarray()[0] for row in vectors]
    print(f"[embed] fit vectorizer on {len(texts)} chunks, vocab size={len(vectorizer.vocabulary_)}")
    print(f"[embed] stored {len(chunk_embeddings)} embeddings, dim={len(chunk_embeddings[0])}")
    return chunk_embeddings


def retrieve(query, chunks, chunk_embeddings, top_k=3):
    query_embedding = vectorizer.transform([query]).toarray()[0]
    scores = cosine_similarity([query_embedding], chunk_embeddings)[0]
    top_indices = scores.argsort()[::-1][:top_k]
    retrieved = [(chunks[i], scores[i]) for i in top_indices]
    print(f"[retrieve] top {top_k} chunks for query {query!r}:")
    for chunk, score in retrieved:
        print(f"  - {chunk['source']} (score={score:.3f}): {chunk['text'][:80]}...")
    return retrieved


def build_prompt(query, retrieved):
    context = "\n\n".join(f"[{chunk['source']}]\n{chunk['text']}" for chunk, _ in retrieved)
    return (
        "Answer the question using only the context below. "
        "If the context does not contain the answer, say "
        '"I don\'t have enough information."\n\n'
        f"Context:\n{context}\n\nQuestion: {query}\nAnswer:"
    )


def call_llm(prompt):
    body = json.dumps({
        "model": GROQ_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0,
    }).encode()
    req = urllib.request.Request(
        "https://api.groq.com/openai/v1/chat/completions",
        data=body,
        headers={
            "Authorization": f"Bearer {os.environ['GROQ_API_KEY']}",
            "Content-Type": "application/json",
            "User-Agent": "rag-demo/1.0",
        },
    )
    with urllib.request.urlopen(req, context=SSL_CONTEXT) as resp:
        result = json.load(resp)
    usage = result.get("usage", {})
    print(f"[llm] prompt_tokens={usage.get('prompt_tokens')} completion_tokens={usage.get('completion_tokens')}")
    return result["choices"][0]["message"]["content"].strip()


def answer_query(query, chunks, chunk_embeddings, top_k=3):
    retrieved = retrieve(query, chunks, chunk_embeddings, top_k)
    best_score = retrieved[0][1]
    if best_score < NO_ANSWER_THRESHOLD:
        print(f"[generate] best score {best_score:.3f} < threshold {NO_ANSWER_THRESHOLD}, skipping LLM call")
        return "I don't have enough information."
    prompt = build_prompt(query, retrieved)
    print(f"[generate] calling {GROQ_MODEL} with {len(prompt)} char prompt")
    return call_llm(prompt)


if __name__ == "__main__":
    load_env()
    documents = load_documents()
    chunks = chunk_documents(documents)
    chunk_embeddings = embed_chunks(chunks)

    query = input("Query: ")
    answer = answer_query(query, chunks, chunk_embeddings)
    print(f"\nAnswer: {answer}")
