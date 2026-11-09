# Aireplay injection test: completed, negative

On November 9, 2026, `aireplay-ng --test` completed on the OnePlus 13's internal monitor interface with **0/30 directed-probe responses**. It did not print `Injection is working!`. A repeat after the owner started NetHunter, with the chroot environment explicitly checked, produced the same result. The initialized repeat is the primary result in this report.

This establishes a negative result for the tested aireplay configuration. It does not demonstrate successful monitor injection, and it does not retest the separate managed-interface `NL80211_CMD_FRAME` operation.

## Environment and controls

- Same handset, build, and module hash as the [main report](REPORT.md): Magisk-rooted CPH2655, Android 16, kernel `6.6.89-android15-8-g97a9aaefab9a-ab14519050-4k`, `qca_cld3_peach_v2`.
- Internal `wlan0` only, `con_mode=4`, radiotap interface type 803; no external Wi-Fi adapter.
- NetHunter ARM64 chroot; aircrack-ng package `1:1.7+git20230807.4bf83f1a-3`, tcpdump `4.99.6-2`. The exact aireplay binary hash is recorded in [the evidence summary](../evidence/aireplay-test.json).
- The initialized run verified `/proc`, `/sys`, and `/dev` mounts, readable `/proc/meminfo` and `/proc/net/dev`, a character-device `/dev/null`, root execution, and interface inspection from inside Kali.
- The chroot process received `PATH=/usr/sbin:/usr/bin:/sbin:/bin`, `LANG=C.UTF-8`, and `LC_ALL=C.UTF-8`.
- The owned test AP was on channel 6. Before each completed test, tcpdump captured five beacons from that AP; all five radiotap headers reported 2437 MHz. No channel hopping ran.

## Invocation and observations

The relevant invocation, with private identifiers replaced by variables, was:

```sh
aireplay-ng --test --ignore-negative-one -a "$OWNED_AP_BSSID" -e "$OWNED_SSID" wlan0
```

The private runner imposed a 45-second limit with a further 3-second kill grace period. The initialized test completed normally, before that limit. `--ignore-negative-one` was needed because the monitor driver did not expose a usable current channel to aireplay. It bypassed the tool's channel-detection guard; channel selection and captured radiotap metadata were checked separately.

| Observation | Initialized-run result |
|---|---|
| AP receive precheck | Five captured beacons, all at 2437 MHz |
| Broadcast probe phase | `No Answer...` |
| APs listed by the test | 1 |
| Directed probe response count | 0/30, 0% |
| Injection-success message | Absent |
| Aireplay process exit code | 0 |
| Timeout | No |
| Monitor TX packet / byte counters | 0 / 0 before and after |
| Post-test phone state | Managed mode 0, saved empty firmware path restored, normal Wi-Fi associated |
| Leftover capture/test processes or radio lock | None observed |

**Exit code 0 records process completion, not successful injection.** The [Aircrack-ng injection-test documentation](https://www.aircrack-ng.org/doku.php?id=injection_test) describes probe-response-based testing. Seeing the AP's beacons or its name in the output does not establish that it answered transmitted probes. The test includes a broadcast probe phase even when an AP is selected; it was not a deauthentication test.

See the [redacted initialized-run output](../evidence/aireplay-output-redacted.txt) and [structured evidence](../evidence/aireplay-test.json). The transcript preserves the tool's output, with the lab BSSID and SSID replaced, terminal carriage returns normalized to newlines, and trailing whitespace stripped.

## Earlier attempts and environment correction

1. The initial invocation stopped before the probe test: the inherited Android PATH could not find `grep`, and aireplay rejected channel `-1`.
2. A revised wrapper stopped before launching aireplay because its channel check expected a field that `iw dev wlan0 info` does not report in this monitor mode.
3. After setting the Linux PATH and verifying the channel from captured beacons, aireplay completed with 0/30 responses. The chroot mounts were not inventoried for this run. The owner then noted that NetHunter had not been started.
4. The owner started NetHunter. The runner verified its mounts and execution environment and repeated the same target, channel, and command. The result remained 0/30.

Both preflight stops and both completed runs were preserved. The two early stops are not counted as negative injection tests. The final repeat addresses the unverified chroot setup in the preceding run.

## Interpretation and remaining limits

The result is consistent with the installed module's monitor operations table lacking `ndo_start_xmit`, as documented in the main report. A 0/30 result and zero TX counters alone are not an independent RF measurement and do not prove that no frame ever reached the air. They also do not establish behavior on another build, band, or modified driver.

For Hijacker, usable airodump reception remains a demonstrated foundation. Existing aireplay monitor-transmit actions are not established as working. A supported directed management operation would need a separate backend that returns to managed mode and uses the previously tested netlink path.

The earlier directed-deauthentication evidence remains a matching driver-reported ACK plus correlated loss and recovery of responses from the owned WiZ client. An independently captured transmitted frame and AP association/disconnection logs are still missing; this report does not upgrade that result to independent on-air proof.

## Provenance

Original captures, scripts, and logs remain private because they contain local identifiers. The structured summary includes their SHA-256 hashes. Hashes bind retained artifacts but do not let a reader independently verify unpublished contents. The public transcript and summaries omit the lab's addresses and SSID. Follow the main report's [authorized-hardware and recovery protocol](REPORT.md#4-reproduction-and-safety-protocol) for any reproduction.
