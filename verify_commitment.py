#!/usr/bin/env python3
"""Standalone verifier for the Merkle commitment. No dependencies beyond stdlib."""
import hashlib, json, sys

def sha256(data):
    return hashlib.sha256(data).hexdigest()

def leaf_hash(i, l, s, n):
    canon = json.dumps({"i":i,"l":l,"s":s,"n":n}, separators=(",",":"), sort_keys=True, ensure_ascii=True).encode()
    return sha256(b"\x00" + canon)

def node_hash(left, right):
    return sha256(b"\x01" + bytes.fromhex(left) + bytes.fromhex(right))

def verify_proof(lh, proof, root):
    cur = lh
    for s in proof:
        cur = node_hash(cur, s["hash"]) if s["side"]=="right" else node_hash(s["hash"], cur)
    return cur == root

data = json.load(open(sys.argv[1] if len(sys.argv)>1 else "commitment.json"))
root = data["merkle_root"]
leaves = data.get("public_leaves",[])+data.get("sealed_leaves",[])+data.get("all_leaves",[])+data.get("revealed_leaves",[])
seen, ok = set(), True
for lf in sorted({l["index"]:l for l in leaves}.values(), key=lambda x:x["index"]):
    h = leaf_hash(lf["index"], lf["label"], lf["secret"], lf["nonce"])
    hok, pok = h==lf["leaf_hash"], verify_proof(lf["leaf_hash"], lf["merkle_proof"], root)
    print(f"  Leaf {lf['index']:2d} [{lf['label']:30s}] hash={'OK' if hok else 'FAIL'}  proof={'OK' if pok else 'FAIL'}")
    if not (hok and pok): ok = False
print(f"\nRoot: {root}\n{'ALL VERIFIED' if ok else 'VERIFICATION FAILED'}")
sys.exit(0 if ok else 1)
