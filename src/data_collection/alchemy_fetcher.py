import os
import requests
import json
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()

API_KEY = os.getenv("ALCHEMY_API_KEY")
NETWORK = os.getenv("ALCHEMY_NETWORK", "eth-mainnet")

if not API_KEY:
    raise RuntimeError("ALCHEMY_API_KEY not found in .env")

BASE_URL = f"https://{NETWORK}.g.alchemy.com/nft/v3/{API_KEY}"

IMAGE_DIR = "data/raw/opensea/images"
META_DIR = "data/raw/opensea/metadata"

os.makedirs(IMAGE_DIR, exist_ok=True)
os.makedirs(META_DIR, exist_ok=True)


def fetch_nfts_by_collection(contract_address, limit=20):
    url = f"{BASE_URL}/getNFTsForCollection"
    params = {
        "contractAddress": contract_address,
        "withMetadata": "true",
        "pageSize": limit
    }

    response = requests.get(url, params=params, timeout=20)

    if response.status_code != 200:
        raise Exception(f"{response.status_code}: {response.text}")

    return response.json().get("nfts", [])


def resolve_image_url(url):
    if not url:
        return None

    if url.startswith("ipfs://"):
        return url.replace("ipfs://", "https://ipfs.io/ipfs/")

    if url.startswith("ar://"):
        return url.replace("ar://", "https://arweave.net/")

    return url


def download_image(url, path):
    resolved_url = resolve_image_url(url)
    if not resolved_url:
        return

    try:
        # STEP 1: Download metadata JSON
        r = requests.get(resolved_url, timeout=20)
        if r.status_code != 200:
            print(f"Failed to fetch metadata: {resolved_url}")
            return

        # If response is JSON, extract image field
        content_type = r.headers.get("Content-Type", "")
        if "application/json" in content_type:
            metadata = r.json()
            image_url = metadata.get("image")
            if not image_url:
                print("No image field in metadata")
                return

            image_url = resolve_image_url(image_url)
            r = requests.get(image_url, timeout=20)

        # STEP 2: Save image bytes
        if r.status_code == 200:
            with open(path, "wb") as f:
                f.write(r.content)
        else:
            print(f"Failed to fetch image bytes")

    except Exception as e:
        print(f"Download error: {e}")


def extract_image_url(nft):
    # 1️⃣ Media gateway (best case)
    media = nft.get("media", [])
    if isinstance(media, list) and len(media) > 0:
        gateway = media[0].get("gateway")
        if gateway:
            return gateway

        raw = media[0].get("raw")
        if raw:
            return raw

    # 2️⃣ tokenUri (can be dict OR string)
    token_uri = nft.get("tokenUri")

    if isinstance(token_uri, dict):
        gateway = token_uri.get("gateway")
        if gateway:
            return gateway

        raw = token_uri.get("raw")
        if raw:
            return raw

    elif isinstance(token_uri, str):
        return token_uri

    # 3️⃣ Metadata image fallback
    metadata = nft.get("metadata", {})
    if isinstance(metadata, dict):
        image = metadata.get("image")
        if image:
            return image

    return None

def main():
    contract_address = "0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d"

    nfts = fetch_nfts_by_collection(contract_address, limit=20)
    print(f"Fetched {len(nfts)} NFTs")

    for nft in tqdm(nfts):
        token_id = nft["tokenId"]

        image_url = extract_image_url(nft)

        filename = f"nft_{token_id[-4:]}"
        img_path = f"{IMAGE_DIR}/{filename}.png"
        meta_path = f"{META_DIR}/{filename}.json"

        if image_url:
            download_image(image_url, img_path)
        else:
            print(f"No image URL for token {token_id}")

        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(nft, f, indent=2)


if __name__ == "__main__":
    main()
