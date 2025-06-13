import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Any
from importlib import resources

# ---------------------------------------------------------------------
# Internal utils
# ---------------------------------------------------------------------

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
_CHAINS_BY_ID: Dict[int, Dict[str, Any]] = {c["id"]: c for c in _CHAINS}
_CHAINS_BY_NAME: Dict[str, Dict[str, Any]] = {c["name"].lower(): c for c in _CHAINS}

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
    return _CHAINS_BY_ID.get(chain_id)


def get_chain_by_name(name: str) -> Optional[Dict[str, Any]]:
    """
    Return chain metadata by (case-insensitive) chain name.

    Example
    -------
    >>> get_chain_by_name("base sepolia")["id"]
    84532
    """
    return _CHAINS_BY_NAME.get(name.lower())
