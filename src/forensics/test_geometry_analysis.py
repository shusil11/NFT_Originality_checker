from src.forensics.geometry_analysis import analyze_geometry

ref_image = "data/processed/images/nft_0.png"
query_image = "data/processed/images/new_user_nft.png"

result = analyze_geometry(ref_image, query_image)

print("Geometry analysis result:")
for key, value in result.items():
    print(f"{key}: {value}")
