import os
import torch
import clip
import numpy as np
from PIL import Image
from tqdm import tqdm

# Paths
IMAGE_DIR = "data/processed/images"
EMBED_DIR = "embeddings/clip"

os.makedirs(EMBED_DIR, exist_ok=True)

# Device
device = "cuda" if torch.cuda.is_available() else "cpu"

# Load CLIP
model, preprocess = clip.load("ViT-B/32", device=device)
model.eval()


def extract_embedding(image_path):
    image = Image.open(image_path).convert("RGB")
    image = preprocess(image).unsqueeze(0).to(device)

    with torch.no_grad():
        embedding = model.encode_image(image)
        embedding = embedding / embedding.norm(dim=-1, keepdim=True)

    return embedding.cpu().numpy()[0]


def main():
    image_files = os.listdir(IMAGE_DIR)
    all_embeddings = []

    for img_name in tqdm(image_files):
        img_path = os.path.join(IMAGE_DIR, img_name)
        emb = extract_embedding(img_path)

        all_embeddings.append({
            "image": img_name,
            "embedding": emb
        })

    np.save(os.path.join(EMBED_DIR, "embeddings.npy"), all_embeddings)
    print(f"Saved {len(all_embeddings)} embeddings")


if __name__ == "__main__":
    main()
