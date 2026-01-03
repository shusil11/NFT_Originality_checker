"""
perceptual_hash.py

This module computes perceptual hashes (pHash) for images
and compares them to detect near-duplicates even after
transformations like resize, crop, or rotation.
"""

from PIL import Image
import imagehash


def compute_phash(image_path):
    """
    Compute perceptual hash (pHash) for an image.

    Args:
        image_path (str): Path to image file

    Returns:
        imagehash.ImageHash object
    """
    image = Image.open(image_path).convert("RGB")
    return imagehash.phash(image)


def phash_distance(hash1, hash2):
    """
    Compute Hamming distance between two perceptual hashes.

    Smaller distance => more similar images.

    Args:
        hash1, hash2: imagehash.ImageHash

    Returns:
        int: Hamming distance
    """
    return hash1 - hash2


def interpret_phash_distance(distance):
    """
    Convert hash distance into a human-meaningful label.

    These thresholds are conservative and can be tuned later.
    """
    if distance <= 5:
        return "NEAR_DUPLICATE"
    elif distance <= 12:
        return "TRANSFORMED_COPY"
    else:
        return "VISUALLY_DIFFERENT"
