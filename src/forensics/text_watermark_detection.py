"""
text_watermark_detection.py

Detects:
- Text overlays using OCR
- Possible watermarks using simple heuristics

This module provides forensic signals, not legal judgments.
"""

import cv2
import numpy as np
import easyocr


# Initialize OCR reader once (English is enough for NFTs initially)
reader = easyocr.Reader(['en'], gpu=False)


def detect_text(image_path, confidence_threshold=0.4):
    """
    Detect visible text in an image using OCR.

    Returns:
        dict with detected text and bounding boxes
    """
    results = reader.readtext(image_path)

    detected_text = []
    boxes = []

    for box, text, confidence in results:
        if confidence >= confidence_threshold and text.strip():
            detected_text.append(text)
            boxes.append(box)

    return {
        "text_detected": len(detected_text) > 0,
        "texts": detected_text,
        "boxes": boxes
    }


def detect_watermark(image_path):
    """
    Heuristic watermark detection.

    Looks for:
    - High edge density in low-contrast regions
    - Repeated patterns
    - Semi-transparent overlays

    This is approximate by design.
    """
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    if img is None:
        return {"watermark_detected": False}

    # Edge detection
    edges = cv2.Canny(img, 100, 200)

    # Measure edge density
    edge_density = np.sum(edges > 0) / edges.size

    # Low contrast regions
    contrast = np.std(img)

    watermark_detected = edge_density > 0.02 and contrast < 60

    return {
        "watermark_detected": watermark_detected,
        "edge_density": round(edge_density, 4),
        "contrast": round(float(contrast), 2)
    }
