import os
from PIL import Image
from tqdm import tqdm

RAW_IMAGE_DIR = "data/raw/opensea/images"
PROCESSED_IMAGE_DIR = "data/processed/images"

os.makedirs(PROCESSED_IMAGE_DIR, exist_ok=True)


def preprocess_image(img_path, save_path, size=224):
    with Image.open(img_path) as img:
        img = img.convert("RGB")

        # Resize while keeping aspect ratio
        img.thumbnail((size, size), Image.Resampling.LANCZOS)

        # Center crop
        width, height = img.size
        left = (width - size) // 2
        top = (height - size) // 2
        right = left + size
        bottom = top + size

        img = img.crop((left, top, right, bottom))
        img.save(save_path, format="PNG")


def main():
    images = os.listdir(RAW_IMAGE_DIR)

    for img_name in tqdm(images):
        src_path = os.path.join(RAW_IMAGE_DIR, img_name)
        dst_path = os.path.join(PROCESSED_IMAGE_DIR, img_name)

        preprocess_image(src_path, dst_path)


if __name__ == "__main__":
    main()
