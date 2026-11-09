# NetHunter and Wi-Fi app compatibility

Status: November 9, 2026. Hardware observations refer only to the device/build in the [report](REPORT.md). A store listing, root access, or successful interface detection does not validate an app's capture and transmit paths.

## Current evidence

| Tool or feature | Status | What integration requires |
|---|---|---|
| tcpdump radiotap capture | **Tested** on channel 6 | Driver-specific monitor preparation and reliable restoration |
| airodump-ng AP/station reception | **Tested** through the private Bender Lab backend | NetHunter ARM64 tool, fixed channel, working headless invocation, shared output paths |
| Hijacker AP/station UI and capture | **Port candidate; app untested** | Replace Nexmon setup, integrate QCA lifecycle/tool runner, deliver CSV/PCAP to the UI, verify cancellation |
| A directed deauthentication action in a modified app | **Backend mechanism tested; Hijacker integration unimplemented** | Dedicated privileged managed-interface TX operation, fresh interface discovery, TX-status handling, and explicit lab target confirmation |
| `aireplay-ng --test` on monitor `wlan0` | **Completed, negative: 0/30 responses** | Repeated with NetHunter mounts verified; the missing monitor TX handler cannot be supplied by an interface-name or prefix setting |
| Other aireplay-ng monitor injection actions | **Unsupported by the inspected monitor operations; individual modes untested** | A selected managed-interface operation needs a separate implementation |
| Reaver/WPS and mdk3 transmit workflows | **Not established** | Audit each operation's required frames, timing, and RX/TX concurrency; the single management-frame result is insufficient |
| hcxdumptool's normal active workflow | **Not established** | Its documented requirements include full monitor and injection support; this work has not met those requirements |
| Offline PCAP analysis | **Does not require radio TX** | Validate the exported format and permissions for the chosen consumer; individual app integrations remain untested |
| Channel hopping, 5/6 GHz capture, simultaneous monitor RX/TX | **Untested** | Independent capability and recovery tests before exposing these features |

Kali's [wireless-card documentation](https://www.kali.org/docs/nethunter/wireless-cards/) currently lists QCACLD-3.0 as monitor-mode-only. The separate managed-interface management TX finding here does not turn this driver into a fully supported monitor injector. The [hcxdumptool upstream requirements](https://github.com/ZerBea/hcxdumptool#requirements) likewise should not be replaced with a blanket compatibility claim.

## What the airodump test proves

The successful channel-6 run created a CSV containing the selected lab AP (28 beacons) and the owned test station (2 packets). Normal Wi-Fi was restored. The earlier attempt produced no CSV; enabling `--background 1` and setting `LANG`/`LC_ALL` to `C.UTF-8` made the subsequent invocation succeed. Because both settings changed together, the experiment does not isolate which change was necessary.

The installed aircrack-ng package was `1:1.7+git20230807.4bf83f1a-3`. These were the ARM64 tools in the NetHunter chroot, not proof that Hijacker's bundled executables work on this phone. The capture log retained a nonfatal `/proc/meminfo` warning. These observations and original artifact hashes are preserved in [app-compatibility.json](../evidence/app-compatibility.json).

This test establishes usable receive output. It does not establish Hijacker UI parsing, a complete WPA handshake capture, injection, channel hopping, or end-to-end WPS operation.

## The integration boundary

The subsequent [aireplay injection test](AIREPLAY_TEST.md) completed twice with 0/30 responses; the second run explicitly verified the initialized NetHunter environment. Both runs independently verified channel 6 from captured AP beacons. Neither printed the injection-success message, and monitor TX packet counters remained zero. The initial environment had not been inventoried, so the initialized repeat is the primary result. These observations support keeping monitor injection disabled on this build; they do not test the separate `NL80211_CMD_FRAME` path.

There are two distinct backend operations:

1. **Capture session:** save recoverable state, acquire exclusive radio ownership, stage the existing firmware/configuration, switch to `con_mode=4`, verify radiotap `wlan0`, run a receive tool, retain output, and restore saved state on success/failure/cancellation.
2. **Managed management operation:** stop capture, restore `con_mode=0`, rediscover the interface index and live capabilities, validate the authorized target, submit only the supported bounded operation, and distinguish request acceptance from a matching TX-status ACK and independently observed client behavior.

Switching modes can destroy and recreate `wlan0`. A cached interface index or a still-running capture process cannot be carried across the transition. The current design must serialize capture and managed TX; concurrent operation is unproven.

A shared backend can make additional app ports cheaper, but its API should advertise separate capabilities such as passive capture, selected management TX, and monitor packet TX. It must report the last capability as unavailable for the inspected build. An `injection=true` flag would misrepresent the finding.

## Fork and PR strategy

The original [chrisk44/Hijacker](https://github.com/chrisk44/Hijacker) repository was archived when checked on November 9, 2026. Its reported last push was August 26, 2020. That supports starting a maintained fork; it does not establish that every existing fork is inactive.

The first implementation milestone should be fixed-channel scanning/capture with restoration. A second milestone can add a clearly separate supported management operation after its own verification. Keep changes reviewable so an active downstream maintainer can later accept them as PRs. Preserve upstream authorship and GPL-3.0 licensing.

The [source-level port plan](HIJACKER_PORT.md) identifies the actual call sites and acceptance criteria. No upstream PR has been submitted and no fork is represented here as tested.
