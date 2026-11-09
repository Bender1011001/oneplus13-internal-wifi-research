# Router evidence for the directed management tests

**The owner's router independently recorded the test bulb disconnecting and completing a new authentication, association, and four-way handshake twice.** These sequences support the directed-deauthentication interpretation. Their timing correlates with the two recorded managed-interface tests, but the historical router-to-phone clock offset was not measured. The submitted frame itself still lacks an independent RF capture.

The exports were retrieved on November 9, 2026, after the November 8 experiments. This review sent no new test frames and changed no router settings. It concerns `NL80211_CMD_FRAME` on managed `wlan0`, not monitor-mode transmission or the separate [negative aireplay test](AIREPLAY_TEST.md).

## What the router recorded

The complete System Log export contains 869 lines and the Advanced Log contains 9,312. The relevant records are in the **Advanced Log**, under `hostapd`; the System Log has no entry for this client within two minutes of either selected sequence. The visible web table showed only a recent subset, so the saved export was needed to review the older events.

For each sequence, the AP recorded:

1. The exact owned test client disconnected from the exact owned AP.
2. The client authenticated successfully and sent an association request.
3. The AP associated the client, then exchanged all four EAPOL handshake messages.
4. The client was connected and the pairwise key handshake completed.

Each sequence has 12 `hostapd` entries and one router connection-monitor entry. All entries within a sequence share one router timestamp, with one-second resolution. The [redacted excerpt](../evidence/router-reconnections-redacted.txt) contains all 26 entries and their original source line numbers. Role labels replace the AP/client addresses; unrelated clients are excluded.

## Timing and its limits

The two phone records each contain one directed userspace submission and a driver-reported ACK. The original test also has the previously recorded response interruption and recovery. The later app test did not collect a new host-side response timeline.

| Record | First directed test | Later app test |
|---|---:|---:|
| Phone TX time, relative to first phone TX | 0 s | 3532.552612 s |
| Router sequence time, relative to first router sequence | 0 s | 3530 s |
| Selected router entries | 13 | 13 |
| Matching client/AP addresses verified privately | Yes | Yes |

**The phone and router columns use separate time origins. Their zeroes do not mean the events were simultaneous.** The event-pair intervals differ by 2.552612 seconds over about 59 minutes. This is supporting temporal correlation, not a measured clock correction or proof of causality.

If the raw router wall times are interpreted in the host's Pacific timezone, the sequences appear 10.170360 and 12.722972 seconds before the corresponding phone TX timestamps. The original phone-to-host correction reduces the first nominal difference to about 9.112 seconds; it does not calibrate the router. Do not present these apparent negative delays as actual reaction times or silently shift the log to make it fit.

The raw exports carry no timezone label. A next-day read-only inspection of the router Date & Time page displayed `Mountain_Time` with automatic NITZ time updates. That page cannot establish the timezone or offset used by the historical log. Historical clock alignment therefore remains unresolved, and neither exact reaction latency nor outage duration is established by this review.

## What can be claimed

- The phone recorded accepted directed management requests and matching ACK status on its internal radio.
- The original host observation recorded a target-specific response interruption and recovery.
- Independent AP records now establish two disconnect/reconnect sequences for the same client/AP pair, with timing that supports correlation with the two directed tests.

The excerpts do **not** identify a received deauthentication frame, its reason code, or its actual transmitter. They are stronger evidence than an ACK or application timeout alone, but do not close the RF-capture and historical-clock gaps. This remains one handset/build and one owned AP/client pair; no PMF bypass, arbitrary monitor injection, or independent researcher reproduction is established.

A stronger future reproduction would measure clock offsets, retain AP events and independent over-the-air capture, and correlate a bounded authorized test with the target's recovery. This review did not perform another transmission.

## Provenance and privacy

[Machine-readable review](../evidence/router-log-review.json) records the counts, intervals, caveats, and SHA-256 hashes of the private source artifacts. The raw router exports, original phone records, and later clock observations are retained privately. Public excerpts replace addresses and absolute router timestamps with role labels and relative times. Hashes identify retained files; they do not independently prove their contents.

See the [technical report](REPORT.md#3-evidence-and-interpretation) for the original experiment, [directed TX evidence](../evidence/directed-tx.redacted.json), and [host observations](../evidence/probe-observations.json).
