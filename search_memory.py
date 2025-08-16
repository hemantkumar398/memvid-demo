
# search_memory.py
from memvid import MemvidRetriever
retriever = MemvidRetriever("my_memory.mp4", "my_memory_index.json")

q = "what is fastapi?"
results = retriever.search(q, top_k=3)

print("sss1",results)

# Print results (structure may include text/score/metadata).
import json
print(json.dumps(results, indent=2, ensure_ascii=False))
