from sklearn.datasets import fetch_20newsgroups
from pathlib import Path

OUT_DIR = Path(__file__).parent / "documents"

data = fetch_20newsgroups(
    subset="train",
    categories=["comp.graphics", "sci.med", "talk.politics.misc"],
    remove=("headers", "footers", "quotes"),
)

documents = data.data[:30]

for i, doc in enumerate(documents):
    (OUT_DIR / f"doc_{i:02d}.txt").write_text(doc.strip() + "\n")

print(f"Wrote {len(documents)} documents to {OUT_DIR}")
