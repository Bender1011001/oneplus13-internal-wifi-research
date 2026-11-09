# Hijacker: OnePlus 13 port plan

**Design status only:** source reviewed; no patched Hijacker APK has been validated on the phone. The underlying airodump-ng receive path passed a separate handset test.

Reviewed upstream: [`chrisk44/Hijacker` at `898af5b530dd000b8251f21da94626d9e41e53d2`](https://github.com/chrisk44/Hijacker/tree/898af5b530dd000b8251f21da94626d9e41e53d2). Upstream is archived as checked November 9, 2026. A maintained GPL-3.0 fork is the practical starting point; retain the upstream remote and attribution.

## Concrete changes

| Existing code | Observed assumption | Required change |
|---|---|---|
| [`strings.xml`, monitor/prefix defaults](https://github.com/chrisk44/Hijacker/blob/898af5b530dd000b8251f21da94626d9e41e53d2/app/src/main/res/values/strings.xml#L321) | `nexutil` monitor toggles and `libfakeioctl.so` preload | Add an explicit QCA internal-radio backend; preserve existing hardware profiles |
| [`MainActivity.java`, tool setup](https://github.com/chrisk44/Hijacker/blob/898af5b530dd000b8251f21da94626d9e41e53d2/app/src/main/java/com/hijacker/MainActivity.java#L530) | Both `armv7l` and `aarch64` enter the bundled-tool setup; architecture detection alone does not verify each executable | Use and validate the tested ARM64 NetHunter tools, including executable ABI, dependencies, permissions, chroot mounts, and output paths |
| [`Airodump.java`, start](https://github.com/chrisk44/Hijacker/blob/898af5b530dd000b8251f21da94626d9e41e53d2/app/src/main/java/com/hijacker/Airodump.java#L141) | Builds a shell command, requests monitor mode through `runOne`, then launches capture | Await a structured ready/error result; verify radiotap mode before starting; use controlled argument construction |
| [`Shell.java`, runOne](https://github.com/chrisk44/Hijacker/blob/898af5b530dd000b8251f21da94626d9e41e53d2/app/src/main/java/com/hijacker/Shell.java#L108) | No operation result is returned to the caller | Surface exit status and timeout; do not infer successful mode preparation from command submission |
| [`Airodump.java`, stop](https://github.com/chrisk44/Hijacker/blob/898af5b530dd000b8251f21da94626d9e41e53d2/app/src/main/java/com/hijacker/Airodump.java#L199) | Stops tools by process name and updates UI | Own the specific session/process, preserve partial output, restore driver/firmware-path state, and report restoration failures |
| [`MainActivity.java`, aireplay dispatch](https://github.com/chrisk44/Hijacker/blob/898af5b530dd000b8251f21da94626d9e41e53d2/app/src/main/java/com/hijacker/MainActivity.java#L986) | All those actions invoke `aireplay-ng` | Gate unsupported actions; implement any supported managed-interface operation separately rather than treating it as monitor injection |
| [`app/build.gradle`](https://github.com/chrisk44/Hijacker/blob/898af5b530dd000b8251f21da94626d9e41e53d2/app/build.gradle) | SDK 29 and NDK 21 era build | Reproduce a baseline build, then resolve current Android packaging/runtime issues as a separate, reviewable change |

The presence of custom monitor commands and a configurable prefix is useful, but changing those settings alone does not establish correct lifecycle handling, tool compatibility, file visibility, or TX support.

## First milestone: receive support

Implement an explicit backend selection, initially limited to the verified device/build or an explicitly marked unverified profile. Capture support should:

- Identify the actual driver/build and available tools without changing radio state.
- Save the current firmware loader path and Wi-Fi state before changing anything, with a persistent recovery record and an exclusive session lock.
- Prepare `con_mode=4`, wait for the newly created interface, and verify type 803/radiotap before capture.
- Start with a fixed channel; channel 6 is the only demonstrated receive channel in this investigation.
- Use the tested ARM64 airodump invocation options and provide a path visible to both the chroot process and Hijacker's CSV observer. Check CSV behavior against the application's parser rather than assuming compatibility from filename creation.
- Handle success, missing tools, permission errors, cancellation, activity destruction, and process failure. A foreground service and root-side recovery helper are design candidates, not implemented features.
- Restore the saved firmware loader path, writing a newline for an originally empty sysfs value; return to managed mode and report the actual final state.

Acceptance requires a fresh APK on the real phone: AP/station rows update, selected capture files export and parse, stopping/cancelling restores Wi-Fi, and unsupported TX controls are clearly unavailable. Include error/cancellation evidence as well as a successful capture. An emulator or a CLI airodump result cannot satisfy this milestone alone.

## Second milestone: a separate management operation

The existing directed lab result establishes a specific candidate backend, not support for every aireplay mode. Before exposing a corresponding UI action:

- Serialize it against capture and restore managed mode first.
- Rediscover interface identity and live features after the mode change.
- Require an explicit authorized lab AP/client selection and revalidate it at execution.
- Keep a bounded request and retain the response cookie and matching TX-status event.
- Show request acceptance, driver-reported ACK, and independently observed target behavior as different results.
- Preserve the existing limits: no PMF bypass, generic monitor injection, arbitrary frame support, or simultaneous RX/TX claim.

Fresh-boot active-only reproduction and independent RF capture or AP association logs are still needed to strengthen the mechanism and effect claims. They should be tracked as outstanding evidence, not silently assumed.

## Public release standard

Publish reproducible source/build instructions, exact supported-build information, and an APK only after the receive milestone passes. Use a distinct package/application name if parallel installation is needed. Preserve GPL-3.0 notices and make the corresponding source available. Keep private lab configuration, raw captures, signing keys, and user identifiers out of the release.

A short demonstration should show scanning, capture/export, and restoration on the internal radio, followed by a clear list of supported and unsupported features. That gives others a useful result they can check, without relying on a claim of first discovery.
