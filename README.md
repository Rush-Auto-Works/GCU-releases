# Rush SR — GCU Firmware Releases

Public distribution home for the **Gear Control Unit (GCU)** firmware that runs
the Rush SR's pneumatic sequential paddle shifter. This repo carries the
downloadable firmware bundles, the release notes, and the flashing instructions.

It is a **distribution repo**: it holds the ready-to-flash firmware bundles, the
release notes, and the flashing guide. The firmware source code lives in a
separate repository.

## Get the firmware

Grab the latest bundle from [**Releases**](../../releases). Each release zip
contains the firmware for both car generations plus the GCU Flasher app:

- **Gen2 (CAN / drive-by-wire)** — `release_CAN-X.X.X.hex`
- **Gen1 (KLine / throttle cable)** — `release_KLine-X.X.X.hex`

Not sure which you have? Gen1 cars have a throttle cable at the pedal box; Gen2
cars have an accelerator pedal sensor (no cable).

## Flash it

See [`docs/flashing.md`](docs/flashing.md) for the full step-by-step — USB-B
cable, the GCU Flasher app (macOS + Windows), picking the right hex, and the
built-in serial console for diagnostics.

## Version history

[`CHANGELOG.md`](CHANGELOG.md) is the source of truth for what changed in each
release. Older versions (3.0.3 and earlier) are not published here — contact
Rush Auto Works.

---

*Maintained by Rush Auto Works. The firmware page in the
[owner's manual](https://manual.rush.sr/maintenance/electronics-and-wiring/gcu-firmware)
mirrors this repo's releases.*
