"""
decision_engine.py

This module converts similarity scores into
human-readable originality decisions.

Possible labels:
- ORIGINAL
- INFLUENCED
- COPIED
"""

# Thresholds (tunable later)
COPY_THRESHOLD = 0.95
INFLUENCE_THRESHOLD = 0.80


def decide_originality(similarity_results):
    """
    Decide originality based on similarity scores.

    Parameters:
        similarity_results (list of dict):
        Example:
        [
            {"image": "nft_0.png", "score": 1.00},
            {"image": "nft_8.png", "score": 0.86}
        ]

    Returns:
        dict with:
        - label
        - reason
    """

    if not similarity_results:
        return {
            "label": "ORIGINAL",
            "reason": "No similar NFTs found in the database"
        }

    top_match = similarity_results[0]
    score = top_match["score"]

    if score >= COPY_THRESHOLD:
        return {
            "label": "COPIED",
            "reason": f"Very high similarity ({score:.2f}) with existing NFT {top_match['image']}"
        }

    if score >= INFLUENCE_THRESHOLD:
        return {
            "label": "INFLUENCED",
            "reason": f"Moderate similarity ({score:.2f}) with existing NFT {top_match['image']}"
        }

    return {
        "label": "ORIGINAL",
        "reason": f"Low similarity score ({score:.2f}); no strong visual overlap"
    }
