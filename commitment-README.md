# DJI Ronin 4D ProRes-on-CFexpress — Cryptographic Commitment

I have a working method to record ProRes 422HQ, 4444XQ, and RAW on standard CFexpress Type B cards on the DJI Ronin 4D X9-6K, without DJI PROSSD.

The complete attack chain (11 steps) is committed in a Merkle tree. The root and 3 public leaves are published here. The remaining 11 sealed leaves will be revealed later with full reproduction steps.

## Verify now

The 3 public leaves (firmware version, camera component version, original library SHA-256) are verifiable against the Merkle root:

```bash
python3 verify_commitment.py commitment.json
```

No dependencies beyond Python 3 stdlib.

## What the public leaves prove

- **Firmware 01.05.1802** — the exact build this targets
- **Camera component 10.02.02.37** — the specific camera module version
- **Original library SHA-256** — proves I held the actual binary from this firmware. Anyone with the same firmware can independently compute this hash and confirm it matches.

## Commitment details

- Scheme: `merkle-sha256-ds-v1` (domain-separated SHA-256 Merkle tree)
- Leaves: 14 total (3 public, 11 sealed)
- Leaf encoding: canonical JSON, SHA-256 with 0x00 domain prefix
- Node encoding: SHA-256 with 0x01 domain prefix
- Each sealed leaf has a 256-bit random nonce

## Later

When the full procedure is published, `commitment-sealed.json` will be released. Run the same verifier against it to confirm all 14 leaves — proving the complete method existed at the time this commitment was posted.
