# DJI Ronin 4D ProRes-on-CFexpress — Cryptographic Commitment

I have a working method to record ProRes 422HQ, 4444XQ, and RAW on standard CFexpress Type B cards on the DJI Ronin 4D X9-6K, without DJI PROSSD.

## v2 — Second method discovered (2026-11-19)

A second, simpler method was found that requires no binary patching.

The v2 commitment extends the original tree from 14 to 20 leaves, adding 6 sealed leaves covering this new approach. The original 14 leaves (and their nonces) are preserved unchanged, so v1 proofs remain valid.

```bash
# Verify v2 (3 public leaves, 17 sealed)
python3 verify_commitment.py commitment_v2.json

# Verify v1 (original, unchanged)
python3 verify_commitment.py commitment.json
```

- v1 root: `061fa578e8e2bfac92a9d0df697ef57f109da4fdbf1d2ee4f6ef43bd19d563a1`
- v2 root: `edffe141ca38e6aa7576f86f11e1e34f0d8b941f0c3fc0a4c2fac84225b92573`
- v2 references v1 root in `v1_merkle_root` field for chain continuity

## What the public leaves prove

- **Firmware 01.05.1802** — the exact build this targets
- **Camera component 10.02.02.37** — the specific camera module version
- **Original library SHA-256** — proves I held the actual binary from this firmware. Anyone with the same firmware can independently compute this hash and confirm it matches.

## Commitment details

- Scheme: `merkle-sha256-ds-v1` (domain-separated SHA-256 Merkle tree)
- v1: 14 leaves (3 public, 11 sealed)
- v2: 20 leaves (3 public, 17 sealed) — extends v1 with a second method
- Leaf encoding: canonical JSON, SHA-256 with 0x00 domain prefix
- Node encoding: SHA-256 with 0x01 domain prefix
- Each sealed leaf has a 128-bit random nonce
- v1 is timestamped with OpenTimestamps (Bitcoin block attestation)

No dependencies beyond Python 3 stdlib.

## Later

When the full procedure is published, `commitment-sealed.json` and `commitment_v2-sealed.json` will be released. Run the verifier against them to confirm all leaves — proving both methods existed at the time these commitments were posted.
