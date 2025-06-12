# from python_viem import get_chain_by_id, get_chain_by_name
# from python_viem.viem import _load_chains

# data = _load_chains()
# print(data)

# chain = get_chain_by_id(8453)
# print(chain["name"])  # Base

# eth = get_chain_by_name("ethereum")
# print(eth["id"])      # 1
import requests
url = "https://raw.githubusercontent.com/wevm/viem/main/src/chains.ts"
res = requests.get(url, timeout=3)

data = res.text
print(data[:1000])  # Print the first 1000 characters of the fetched data
