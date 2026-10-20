import json
import os
import urllib.request
from pathlib import Path
from urllib.parse import quote
root = Path(__file__).resolve().parents[1]
catalog = root / "wallpapers.json"
base = "https://tatyzxohhrhdtewlivdd.supabase.co"
key = os.environ["SUPABASE_PUBLISHABLE_KEY"]
req = urllib.request.Request(base + "/rest/v1/zaburi_wallpapers?select=id,title,category,object_path&is_published=eq.true", headers={"apikey":key})
with urllib.request.urlopen(req, timeout=25) as response:
    remote = json.load(response)
if not isinstance(remote, list):
    raise ValueError("Unexpected response; catalog unchanged")
existing = json.loads(catalog.read_text(encoding="utf-8"))["wallpapers"]
legacy = [x for x in existing if not str(x.get("id","")).startswith("supabase-")]
fresh = []
for row in remote:
    url = base + "/storage/v1/object/public/zaburi-wallpapers/" + "/".join(quote(segment, safe="") for segment in row["object_path"].split("/"))
    fresh.append({"id":"supabase-" + row["id"],"title":row["title"],"category":row["category"],"imageUrl":url,"thumbnailUrl":url})
output = json.dumps({"wallpapers":legacy+fresh},ensure_ascii=False,indent=2)+"\n"
if output != catalog.read_text(encoding="utf-8"):
    catalog.write_text(output,encoding="utf-8")
print("Catalog synced:",len(legacy),"legacy and",len(fresh),"Supabase")
