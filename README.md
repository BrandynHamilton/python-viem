# python-viem

`python-viem` is a lightweight utility for retrieving EVM chain metadata from a local snapshot (`viem-chains.json`). It supports fast O(1) lookups by either numeric chain ID or human-readable name.

---

## Installation

```bash
pip install python-viem

uv add python-viem # for uv users
```

---

## Features

- Instant chain metadata lookup by:
  - `chain_id` (e.g., `8453 → "Base"`)
  - `name` (e.g., `"Polygon" → 137`)
  - `network` (e.g., `"base-sepolia" → 84532`)

---

## Usage

```python
from python_viem import get_chain_by_id, get_chain_by_name, get_chain_by_network
from python_viem.viem import CHAINS_BY_NETWORK, CHAINS_BY_NAME, CHAINS_BY_ID

print(get_chain_by_id(8453)["name"])        # Base
print(get_chain_by_name("polygon")["id"])   # 137
print(get_chain_by_network("base-sepolia")["id"])  # 43113

print(list(CHAINS_BY_NETWORK.keys())) # List of all network keys
print(list(CHAINS_BY_NAME.keys()))    # List of all chain names
print(list(CHAINS_BY_ID.keys()))      # List of all chain IDs

```

---

## Functions

```python
get_chain_by_id(chain_id: int) -> Optional[Dict[str, Any]]
```

```python
get_chain_by_name(name: str) -> Optional[Dict[str, Any]]
```

```python
get_chain_by_network(network: str) -> Optional[Dict[str, Any]]
```

All functions return the full chain metadata dictionary or `None` if not found.

---

## Project Structure

```
python_viem/
├── __init__.py
├── viem.py
├── viem-chains.json
```

---

## License

MIT
