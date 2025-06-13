import os
import re
import json
import requests
from pathlib import Path

GH_OWNER = "wevm"
GH_REPO  = "viem"
GH_PATH  = "src/chains/definitions"
RAW_URL  = f"https://raw.githubusercontent.com/{GH_OWNER}/{GH_REPO}/main/{GH_PATH}"

SESSION = requests.Session()
SESSION.headers["User-Agent"] = "viem-ts-scraper/0.1"

def list_ts_files() -> list[str]:
    """Return every .ts filename in the definitions directory (GitHub REST)."""
    api = f"https://api.github.com/repos/{GH_OWNER}/{GH_REPO}/contents/{GH_PATH}"
    resp = SESSION.get(api, timeout=10)
    resp.raise_for_status()
    return [item["name"] for item in resp.json() if item["name"].endswith(".ts")]

OBJ_RE = re.compile(
    r"defineChain\s*\(\s*({.+?})\s*\)\s*\)?",
    re.DOTALL
)
KEY_RE  = re.compile(r"(\b\w+)\s*:")

def ts_object_to_json(obj_ts: str) -> str:
    """Rudimentary TS-object → JSON conversion good enough for viem chain files."""
    # remove comments
    obj_ts = re.sub(r"//.*?$|/\*.*?\*/", "", obj_ts, flags=re.S)
    # quote keys            id: 420  -> "id":
    obj_ts = KEY_RE.sub(r'"\1":', obj_ts)
    # single → double quotes
    obj_ts = obj_ts.replace("'", '"')
    # remove trailing commas
    obj_ts = re.sub(r",(\s*[}\]])", r"\1", obj_ts)
    return obj_ts

def grab_chain(fname: str) -> dict:
    """Download a `viem` chain .ts file and return a Python dict."""
    raw_url = (
        "https://raw.githubusercontent.com/wevm/viem/main/"
        f"src/chains/definitions/{fname}"
    )
    ts = requests.get(raw_url, timeout=5)
    ts.raise_for_status()

    # 1️⃣ pull out the `defineChain({...})` object literal
    m = re.search(r"defineChain\(\s*({.*?})\s*\)", ts.text, re.S)
    if not m:
        raise ValueError(f"❌ could not find chain object in {fname}")
    obj = m.group(1)

    # 2️⃣ make it JSON-ish …
    # (a) quote *only* real keys:  { foo: 1 } -> { "foo": 1 }
    obj = re.sub(
        r'([{\[,]\s*)([A-Za-z_][A-Za-z0-9_]*)\s*:',
        lambda m: f'{m.group(1)}"{m.group(2)}":',
        obj,
    )
    # (b) single → double quotes
    obj = obj.replace("'", '"')
    # (c) strip trailing commas
    obj = re.sub(r",(\s*[}\]])", r"\1", obj)
    # (d) kill line comments // ...
    obj = re.sub(r"//.*", "", obj)

    try:
        return json.loads(obj)
    except json.JSONDecodeError as e:
        print(f"[ERROR] Failed to parse {fname}:\n{obj}\n")
        raise e

def build_chain_map() -> dict[str, dict]:
    print("📥  Fetching list of chain definition files…")
    result: dict[str, dict] = {}
    for fname in list_ts_files():
        print("  •", fname)
        chain_dict = grab_chain(fname)
        result[chain_dict["name"]] = chain_dict
    return result

if __name__ == "__main__":
    chain_map = build_chain_map()

    # --- demo: show a few entries ---
    for nm, data in list(chain_map.items())[:5]:
        print(f"\n{nm:=^40}")
        print(json.dumps(data, indent=2))

    # persist locally if you like
    Path("viem_chains.json").write_text(json.dumps(chain_map, indent=2))
    print("\n✅  Wrote viem_chains.json")
