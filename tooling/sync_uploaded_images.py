"""Add newly uploaded repository images to the public wallpaper catalog."""
import hashlib
import json
import re
from pathlib import Path

root = Path(__file__).resolve().parents[1]
catalog = root / "wallpapers.json"
data = json.loads(catalog.read_text(encoding="utf-8"))
items = data["wallpapers"]
hashes = {item["sha256"] for item in items if item.get("sha256")}
base = "https://sagealtair.github.io/zaburi-wallpapers/"
added = 0
for image in sorted((root / "images").iterdir()):
    if not image.is_file() or image.suffix.lower() not in {".jpg", ".jpeg", ".png", ".webp"}:
        continue
    raw = image.read_bytes()
    if not raw or len(raw) > 12 * 1024 * 1024:
        continue
    sha = hashlib.sha256(raw).hexdigest()
    if sha in hashes:
        continue
    if len(items) >= 200:
        raise SystemExit("Catalog full: maximum 200 wallpapers")
    title = re.sub(r"[_-]+", " ", image.stem).strip().title()[:80]
    url = base + "images/" + image.name
    items.append({"id": "wallpaper-" + sha[:20], "title": title,
                  "category": "Psalms", "imageUrl": url,
                  "thumbnailUrl": url, "sha256": sha})
    hashes.add(sha)
    added += 1
if added:
    catalog.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"Added {added} wallpapers")
