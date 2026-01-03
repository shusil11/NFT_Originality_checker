"""
originality_pipeline.py

This module connects:
- CLIP embedding extraction
- FAISS similarity search
- Self-match exclusion
- Originality decision logic

This is the core AI pipeline used by the backend.
"""

import os
import numpy as np
import faiss
import torch
import clip
from PIL import Image

from src.similarity.decision_engine import decide_originality
from src.vector_db.faiss_manager import FaissManager


# Paths
FAISS_INDEX_PATH = "embeddings/faiss/nft.index"
IMAGE_NAMES_PATH = "embeddings/faiss/image_names.npy"

# Load FAISS index and image names once
faiss_index = faiss.read_index(FAISS_INDEX_PATH)
image_names = np.load(IMAGE_NAMES_PATH, allow_pickle=True)

# Load CLIP model once
device = "cuda" if torch.cuda.is_available() else "cpu"
clip_model, clip_preprocess = clip.load("ViT-B/32", device=device)
clip_model.eval()


def extract_clip_embedding(image_path):
    """
    Convert an image into a normalized CLIP embedding.
    """
    image = Image.open(image_path).convert("RGB")
    image_tensor = clip_preprocess(image).unsqueeze(0).to(device)

    with torch.no_grad():
        embedding = clip_model.encode_image(image_tensor)
        embedding = embedding / embedding.norm(dim=-1, keepdim=True)

    return embedding.cpu().numpy()


def find_similar_nfts(query_image_path, query_image_name=None, top_k=5):
    """
    Search FAISS for visually similar NFTs.

    Self-match is automatically excluded if query_image_name is provided.
    """
    query_embedding = extract_clip_embedding(query_image_path)
    scores, indices = faiss_index.search(query_embedding, top_k + 1)

    results = []

    for score, idx in zip(scores[0], indices[0]):
        matched_image = str(image_names[idx])

        # Skip self-match
        if query_image_name and matched_image == query_image_name:
            continue

        results.append({
            "image": matched_image,
            "score": float(score)
        })

        if len(results) == top_k:
            break

    return results


def check_originality(query_image_path, query_image_name=None):
    """
    Full originality check:
    - Find similar NFTs
    - Decide originality label
    """
    similarity_results = find_similar_nfts(
        query_image_path,
        query_image_name=query_image_name
    )

    decision = decide_originality(similarity_results)

    return {
        "decision": decision["label"],
        "reason": decision["reason"],
        "matches": similarity_results
    }

def learn_new_nft(image_path, image_name):
    """
    Add a new NFT to the FAISS index after originality check.
    """
    manager = FaissManager()

    embedding = extract_clip_embedding(image_path)

    manager.add_embedding(embedding, image_name)
    manager.save()

    return {
        "status": "LEARNED",
        "total_nfts": manager.get_size()
    }
