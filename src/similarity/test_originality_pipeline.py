from src.similarity.originality_pipeline import check_originality

# Test with an existing processed image
image_path = "data/processed/images/nft_0.png"

result = check_originality(
    query_image_path=image_path,
    query_image_name="nft_0.png"
)

print("Decision:", result["decision"])
print("Reason:", result["reason"])
print("\nTop Matches:")
for match in result["matches"]:
    print(match)
