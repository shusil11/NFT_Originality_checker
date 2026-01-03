"""
explanation_aggregator.py

Combines multiple forensic signals into:
- a final originality decision
- a confidence score
- a human-readable explanation

This module is intentionally rule-based and explainable.
"""

from typing import Dict


def aggregate_explanation(
    clip_similarity: float,
    phash_label: str,
    geometry_result: Dict,
    text_result: Dict,
    watermark_result: Dict
):
    """
    Aggregate all forensic signals into one decision.

    Returns:
        dict with decision, confidence, evidence, explanation
    """

    score = 0.0
    evidence = []

    # --- CLIP similarity (semantic)
    if clip_similarity >= 0.90:
        score += 0.5
        evidence.append("Very high semantic similarity")
    elif clip_similarity >= 0.75:
        score += 0.3
        evidence.append("Moderate semantic similarity")

    # --- Perceptual hash (structural)
    if phash_label == "NEAR_DUPLICATE":
        score += 0.4
        evidence.append("Near-duplicate image structure detected")
    elif phash_label == "TRANSFORMED_COPY":
        score += 0.25
        evidence.append("Structurally similar image after transformation")

    # --- Geometry analysis
    if geometry_result.get("geometry_detected"):
        score += 0.15
        transforms = []

        if geometry_result["rotation"]["detected"]:
            transforms.append("rotated")

        if geometry_result["cropping"]["detected"]:
            sides = geometry_result["cropping"]["likely_sides"]
            if sides:
                transforms.append(f"cropped from {', '.join(sides)}")
            else:
                transforms.append("cropped")

        if geometry_result.get("recentered"):
            transforms.append("re-centered")

        if transforms:
            evidence.append("Image was " + ", ".join(transforms))

    # --- OCR / watermark
    if text_result.get("text_detected"):
        score += 0.1
        evidence.append("Text overlay detected")

    if watermark_result.get("watermark_detected"):
        score += 0.1
        evidence.append("Possible watermark detected")

    # --- Clamp score
    score = min(score, 1.0)

    # --- Final decision rules
    if score >= 0.7:
        decision = "COPIED"
        confidence = "HIGH"
    elif score >= 0.4:
        decision = "INFLUENCED"
        confidence = "MEDIUM"
    else:
        decision = "ORIGINAL"
        confidence = "HIGH"

    # --- Explanation text
    explanation = (
        f"This NFT is classified as {decision.lower()}. "
        + "Key observations: "
        + "; ".join(evidence)
        if evidence
        else "No significant similarity or modifications were detected."
    )

    return {
        "decision": decision,
        "confidence_score": round(score, 3),
        "confidence_level": confidence,
        "evidence": evidence,
        "explanation": explanation
    }
