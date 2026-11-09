# Contributing

Start with the [report](docs/REPORT.md) and [compatibility matrix](docs/COMPATIBILITY.md). Contributions should distinguish observation from inference and include failures as well as successes.

For a reproduction, provide the model, Android/build ID, kernel release, driver name/hash, root implementation, tool versions, interface mode, tested channel/band, operation, observation method, and final recovery state. Use the reproduction issue template. Do not upload MAC/BSSID/SSID values, private addresses, serial numbers, credentials, raw captures, or proprietary binaries.

Only test hardware you own and are explicitly authorized to test. Keep management transmission bounded and confined to the authorized lab. A driver ACK is not independent proof of the receiver's association state. Document missing evidence and do not label PMF or generic injection as supported without separate proof.

For compatibility changes, prefer one backend capability or lifecycle fix per PR. Include the exact app/tool revision, the intended before/after behavior, and validation on the affected device/build. Source review and offline tests are valuable but must not be reported as live handset validation.

Original material contributed here is under the repository's MIT license. Do not copy GPL code into this repository under MIT; link to it or work in an appropriately licensed fork. Hijacker-derived code retains GPL-3.0 requirements and upstream attribution.

After editing repository files, regenerate the checksum manifest deliberately, then verify it:

```sh
python tools/verify_repository.py --write-manifest
python tools/verify_repository.py
```

The verifier checks local file integrity and references only. It does not validate experimental truth, redact private data, or operate a radio. Review public contents before pushing.
