from src.similarity.originality_pipeline import check_originality, learn_new_nft

# Simulate a new upload
image_path = "data/processed/images/new_user_nft.png"
image_name = "new_user_nft.png"

# Step 1: Check originality
result = check_originality(image_path)

print("Decision:", result["decision"])
print("Reason:", result["reason"])

# Step 2: Learn if not copied
if result["decision"] != "COPIED":
    learning_result = learn_new_nft(image_path, image_name)
    print("Learning result:", learning_result)
else:
    print("NFT rejected (copied)")
