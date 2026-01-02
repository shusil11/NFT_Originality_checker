import numpy as np

data = np.load("embeddings/clip/embeddings.npy", allow_pickle=True)

print("Total embeddings:", len(data))
print("Embedding vector shape:", data[0]["embedding"].shape)
print("First 5 values:", data[0]["embedding"][:5])
