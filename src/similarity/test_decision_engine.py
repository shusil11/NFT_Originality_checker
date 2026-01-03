from src.similarity.decision_engine import decide_originality

test_input = [
    {"image": "nft_0.png", "score": 1.00},
    {"image": "nft_8.png", "score": 0.86}
]

result = decide_originality(test_input)

print("Decision:", result["label"])
print("Reason:", result["reason"])
