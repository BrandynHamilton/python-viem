from python_viem import get_chain_by_id, get_chain_by_name, get_chain_by_network
from python_viem.viem import CHAINS_BY_NETWORK, CHAINS_BY_NAME, CHAINS_BY_ID

print(get_chain_by_id(8453)["name"])        # Base
print(get_chain_by_name("polygon")["id"])   # 137
print(get_chain_by_network("base-sepolia")["id"])  # 43113

print(list(CHAINS_BY_NETWORK.keys())) # List of all network keys
print(list(CHAINS_BY_NAME.keys()))    # List of all chain names
print(list(CHAINS_BY_ID.keys()))      # List of all chain IDs
