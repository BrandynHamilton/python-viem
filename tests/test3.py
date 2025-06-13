from pathlib import Path
import requests

import json
import re
import requests


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

def build_chain_map() -> dict:
    index_url = (
        "https://api.github.com/repos/wevm/viem/contents/"
        "src/chains/definitions"
    )
    files = [f["name"] for f in requests.get(index_url, timeout=5).json()
             if f["name"].endswith(".ts")]

    chain_map = {}
    for fname in files:
        try:
            chain = grab_chain(fname)
            chain_map[chain["id"]] = chain
            print("  •", fname, "✓")
        except Exception as err:
            print("  •", fname, "✗", err)

    return chain_map


if __name__ == "__main__":
    chains = build_chain_map()
    print(f"\nParsed {len(chains)} chains.")
    # show one entry
    sample_id, sample = next(iter(chains.items()))
    print(json.dumps(sample, indent=2))
