import requests
import re
import json
import os

# ------------------------------
# Internal: Try fetching viem chains from GitHub
# ------------------------------

def _fetch_viem_chains_from_github() -> list:
    try:
        url = "https://raw.githubusercontent.com/wevm/viem/main/src/chains.ts"
        res = requests.get(url, timeout=3)

        if res.status_code != 200:
            raise RuntimeError("Failed to fetch viem chains.ts")

        ts_code = res.text
        match = re.search(r'export const chains = (\[.*?\n(?:.*?\n)*?\]);', ts_code)
        if not match:
            raise ValueError("Could not extract chains array")

        chains_array_ts = match.group(1)

        # TypeScript → JSON conversion
        chains_array_json = re.sub(r"(\w+):", r'"\1":', chains_array_ts)   # keys
        chains_array_json = chains_array_json.replace("'", '"')            # quotes
        chains_array_json = re.sub(r",(\s*[}\]])", r"\1", chains_array_json)  # trailing commas

        return json.loads(chains_array_json)

    except Exception as e:
        print(f"[python-viem] Fallback to local chains: {e}")
        return None

# ------------------------------
# Internal: Load chains (live or fallback)
# ------------------------------

def _load_chains() -> list:
    chains = _fetch_viem_chains_from_github()
    if chains:
        return chains

    # Load fallback
    fallback_path = os.path.join(os.path.dirname(__file__), "viem_chains.json")
    with open(fallback_path) as f:
        return json.load(f)

# ------------------------------
# Public Access: Lazy-loaded maps
# ------------------------------

_CHAINS = _load_chains()
_CHAINS_BY_ID = {c["id"]: c for c in _CHAINS}
_CHAINS_BY_NAME = {c["name"].lower(): c for c in _CHAINS}

def get_chain_by_id(chain_id: int) -> dict:
    """Return chain metadata for a given chain ID."""
    return _CHAINS_BY_ID.get(chain_id)

def get_chain_by_name(name: str) -> dict:
    """Return chain metadata by case-insensitive name."""
    return _CHAINS_BY_NAME.get(name.lower())
