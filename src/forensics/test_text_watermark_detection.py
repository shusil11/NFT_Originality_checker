from src.forensics.text_watermark_detection import detect_text, detect_watermark

image_path = "data/processed/images/new_user_nft.png"

text_result = detect_text(image_path)
watermark_result = detect_watermark(image_path)

print("TEXT DETECTION RESULT:")
print(text_result)

print("\nWATERMARK DETECTION RESULT:")
print(watermark_result)
