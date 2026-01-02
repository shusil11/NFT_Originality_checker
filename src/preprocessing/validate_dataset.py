import os
from PIL import Image

IMAGE_DIR = "data/raw/opensea/images"
META_DIR = "data/raw/opensea/metadata"

def validate():
    images = set(os.listdir(IMAGE_DIR))
    metas = set(os.listdir(META_DIR))

    valid_count = 0
    errors = []

    for img in images:
        name, ext = os.path.splitext(img)
        meta_file = name + ".json"

        if meta_file not in metas:
            errors.append(f"Missing metadata for {img}")
            continue

        img_path = os.path.join(IMAGE_DIR, img)

        try:
            with Image.open(img_path) as im:
                im.verify()
            valid_count += 1
        except Exception as e:
            errors.append(f"Corrupt image {img}: {e}")

    print(f"Valid images: {valid_count}")
    print(f"Errors found: {len(errors)}")

    for err in errors:
        print("ERROR:", err)

if __name__ == "__main__":
    validate()
