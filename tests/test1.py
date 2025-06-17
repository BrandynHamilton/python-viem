from python_viem import get_chain_by_id, get_chain_by_name, get_chain_by_network
from python_viem.viem import _CHAINS_BY_NETWORK

print(get_chain_by_id(8453)["name"])        # Base
print(get_chain_by_name("polygon")["id"])   # 137
print(get_chain_by_network("base-sepolia")["id"])  # 43113

print(list(_CHAINS_BY_NETWORK.keys()))
