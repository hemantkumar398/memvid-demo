
# backend/app.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os, uuid

from memvid import MemvidEncoder, MemvidRetriever

app = FastAPI()

origins = [
    "https://memvid-demo.vercel.app",  # your Vercel frontend
    "http://localhost:3000",           # for local testing
]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_methods=["*"],allow_credentials=True, allow_headers=["*"])

MEM_DIR = "memories"
os.makedirs(MEM_DIR, exist_ok=True)

class CreateReq(BaseModel):
    documents: list[str]
    memory_name: str | None = None

class SearchReq(BaseModel):
    memory_name: str
    query: str
    top_k: int = 5

@app.post("/create_memory")
def create_memory(req: CreateReq):
    name = req.memory_name or str(uuid.uuid4())
    mp4 = os.path.join(MEM_DIR, f"{name}.mp4")
    idx = os.path.join(MEM_DIR, f"{name}_index.json")

    encoder = MemvidEncoder()
    encoder.add_chunks(req.documents)
    encoder.build_video(mp4, idx)
    return {"memory_name": name, "mp4": mp4, "index": idx}

@app.post("/search")
def search(req: SearchReq):
    mp4 = os.path.join(MEM_DIR, f"{req.memory_name}.mp4")
    idx = os.path.join(MEM_DIR, f"{req.memory_name}_index.json")
    if not os.path.exists(mp4):
        raise HTTPException(status_code=404, detail="memory not found")
    retriever = MemvidRetriever(mp4, idx)
    results = retriever.search(req.query, top_k=req.top_k)
    return {"results": results}
