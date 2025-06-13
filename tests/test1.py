from python_viem import get_chain_by_id, get_chain_by_name

print(get_chain_by_id(8453)["name"])        # Base
print(get_chain_by_name("polygon")["id"])   # 137
