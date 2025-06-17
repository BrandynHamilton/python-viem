import json
import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Any
from importlib import resources

# ---------------------------------------------------------------------
# Internal utils
# ---------------------------------------------------------------------

def slugify(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")

def _load_snapshot() -> List[Dict[str, Any]]:
    """Load the built-in viem_chains.json (dict *or* list)."""
    try:
        text = resources.files(__package__).joinpath("viem-chains.json").read_text(
            encoding="utf-8"
        )
        data = json.loads(text)

        # ── accept `{ name: {...}, … }` or `[ {...}, … ]` ──────────────────────
        if isinstance(data, dict):      # ← your current file
            return list(data.values())
        if isinstance(data, list):      # ← previous code path
            return data

        raise ValueError("Snapshot must be a JSON dict or array")
    except Exception as exc:
        raise RuntimeError(f"[python-viem] Could not read viem_chains.json: {exc}") from exc

# ---------------------------------------------------------------------
# Lazy-loaded global maps
# ---------------------------------------------------------------------

_CHAINS: List[Dict[str, Any]] = _load_snapshot()

# indexed for O(1) lookup
CHAINS_BY_ID: Dict[int, Dict[str, Any]] = {c["id"]: c for c in _CHAINS}
CHAINS_BY_NAME: Dict[str, Dict[str, Any]] = {c["name"].lower(): c for c in _CHAINS}
CHAINS_BY_NETWORK: Dict[str, Dict[str, Any]] = {}

for chain in _CHAINS:
    network = chain.get("network")
    key = network.lower() if network else slugify(chain["name"])
    CHAINS_BY_NETWORK[key] = chain
# ---------------------------------------------------------------------
# Public helpers
# ---------------------------------------------------------------------

def get_chain_by_id(chain_id: int) -> Optional[Dict[str, Any]]:
    """
    Return chain metadata given a numeric chain ID.

    Example
    -------
    >>> get_chain_by_id(8453)["name"]
    'Base'
    """
    return CHAINS_BY_ID.get(chain_id)

def get_chain_by_name(name: str) -> Optional[Dict[str, Any]]:
    """
    Return chain metadata by (case-insensitive) chain name.

    Example
    -------
    >>> get_chain_by_name("base sepolia")["id"]
    84532
    """
    return CHAINS_BY_NAME.get(name.lower())

def get_chain_by_network(network: str) -> Optional[Dict[str, Any]]:
    """
    Return chain metadata by (case-insensitive) network name.

    Example
    -------
    >>> get_chain_by_network("base-sepolia")["id"]
    43113
    """
    return CHAINS_BY_NETWORK.get(network.lower())
