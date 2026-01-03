"""
geometry_analysis.py

Detects geometric transformations between two images:
- rotation
- scaling
- translation
- cropping (approximate)
- re-centering

Uses ORB keypoints + affine transformation estimation.
"""

import cv2
import numpy as np


def analyze_geometry(reference_image_path, query_image_path):
    """
    Analyze geometric differences between two images.

    Args:
        reference_image_path (str)
        query_image_path (str)

    Returns:
        dict with detected transformations
    """

    # Load images in grayscale
    ref_img = cv2.imread(reference_image_path, cv2.IMREAD_GRAYSCALE)
    qry_img = cv2.imread(query_image_path, cv2.IMREAD_GRAYSCALE)

    if ref_img is None or qry_img is None:
        raise ValueError("One or both images could not be loaded")

    # ORB feature detector
    orb = cv2.ORB_create(nfeatures=5000)

    # Detect keypoints and descriptors
    kp1, des1 = orb.detectAndCompute(ref_img, None)
    kp2, des2 = orb.detectAndCompute(qry_img, None)

    if des1 is None or des2 is None:
        return {"geometry_detected": False}

    # Match descriptors using Hamming distance
    matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = matcher.match(des1, des2)

    if len(matches) < 10:
        return {"geometry_detected": False}

    # Extract matched keypoints
    src_pts = np.float32([kp1[m.queryIdx].pt for m in matches]).reshape(-1, 2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in matches]).reshape(-1, 2)

    # Estimate affine transformation
    matrix, inliers = cv2.estimateAffinePartial2D(
        src_pts,
        dst_pts,
        method=cv2.RANSAC
    )

    if matrix is None:
        return {"geometry_detected": False}

    # Decompose affine matrix
    a, b = matrix[0, 0], matrix[0, 1]
    c, d = matrix[1, 0], matrix[1, 1]

    # Rotation (degrees)
    rotation_rad = np.arctan2(b, a)
    rotation_deg = np.degrees(rotation_rad)

    # Normalize near-180 degree rotations (common in symmetric NFTs)
    if abs(rotation_deg) > 170:
        rotation_deg = 180.0

    # Scale (average of x and y)
    scale_x = np.sqrt(a * a + b * b)
    scale_y = np.sqrt(c * c + d * d)
    scale = (scale_x + scale_y) / 2

    # Translation
    tx, ty = matrix[0, 2], matrix[1, 2]

    # Crop inference (approximate)
    crop_detected = abs(tx)>15 or abs(ty) > 15 
    likely_sides = []

    if tx > 10:
        likely_sides.append("left")
    if tx < -10:
        likely_sides.append("right")
    if ty > 10:
        likely_sides.append("top")
    if ty < -10:
        likely_sides.append("bottom")

    return {
        "geometry_detected": True,
        "rotation": {
            "detected": abs(rotation_deg) > 2,
            "angle_degrees": round(rotation_deg, 2)
        },
        "scaling": {
            "detected": abs(scale - 1.0) > 0.05,
            "scale_factor": round(scale, 3)
        },
        "translation": {
            "x": round(tx, 2),
            "y": round(ty, 2)
        },
        "cropping": {
            "detected": crop_detected,
            "likely_sides": likely_sides
        },
        "recentered": abs(tx) > 10 or abs(ty) > 10
    }
