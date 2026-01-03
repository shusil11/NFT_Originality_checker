from src.forensics.explanation_aggregator import aggregate_explanation

# Example simulated inputs (based on your pipeline results)
clip_similarity = 0.86
phash_label = "TRANSFORMED_COPY"

geometry_result = {
    "geometry_detected": True,
    "rotation": {"detected": True},
    "cropping": {"detected": True, "likely_sides": ["left", "top"]},
    "recentered": True
}

text_result = {"text_detected": False}
watermark_result = {"watermark_detected": True}

result = aggregate_explanation(
    clip_similarity,
    phash_label,
    geometry_result,
    text_result,
    watermark_result
)

print("FINAL AGGREGATED RESULT:\n")
for k, v in result.items():
    print(f"{k}: {v}")
