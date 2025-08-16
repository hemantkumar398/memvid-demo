
# create_memory.py
from memvid import MemvidEncoder

# sample small docs
docs = [
    "AI bias mitigation involves fairness metrics and model explainability.",
    "Docker containers package apps and their dependencies for reproducible runs.",
    "FastAPI is a modern high-performance Python web framework."
]

encoder = MemvidEncoder()          # default options
encoder.add_chunks(docs)          # add a list of short chunks
encoder.build_video("my_memory.mp4", "my_memory_index.json")
print("Saved: my_memory.mp4 and my_memory_index.json")
