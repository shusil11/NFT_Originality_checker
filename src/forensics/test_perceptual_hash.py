from src.forensics.perceptual_hash import (
    compute_phash,
    phash_distance,
    interpret_phash_distance
)

img1 = "data/processed/images/nft_0.png"
img2 = "data/processed/images/new_user_nft.png"

hash1 = compute_phash(img1)
hash2 = compute_phash(img2)

distance = phash_distance(hash1, hash2)
label = interpret_phash_distance(distance)

print("pHash distance:", distance)
print("Interpretation:", label)
