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
- Caches parsed data for fast access.
- Robust fallback: supports both object and array-style JSON formats.

---

## Usage

```python
from python_viem import get_chain_by_id, get_chain_by_name

print(get_chain_by_id(8453)["name"])        # "Base"
print(get_chain_by_name("polygon")["id"])   # 137
```

---

## JSON Format

Your `viem-chains.json` can use either format:

### Object-style (preferred):

```json
{
  "mainnet": { "id": 1, "name": "Ethereum Mainnet", ... },
  "polygon": { "id": 137, "name": "Polygon", ... }
}
```

### Array-style (also supported):

```json
[
  { "id": 1, "name": "Ethereum Mainnet", ... },
  { "id": 137, "name": "Polygon", ... }
]
```

---

## Functions

```python
get_chain_by_id(chain_id: int) -> Optional[Dict[str, Any]]
```

```python
get_chain_by_name(name: str) -> Optional[Dict[str, Any]]
```

Both return the full chain metadata dictionary or `None` if not found.

---

## Project Structure

```
python_viem/
├── __init__.py
├── viem.py
├── viem-chains.json   ← bundled chain metadata
```

---

## License

MIT
