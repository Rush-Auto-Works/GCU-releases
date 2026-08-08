# Rush SR — GCU Firmware Releases

Public distribution home for the **Gear Control Unit (GCU)** firmware that runs the Rush SR's pneumatic sequential paddle shifter. This repo carries the downloadable firmware bundles, the release notes, and the flashing instructions.

It is a **distribution repo**: it holds the ready-to-flash firmware bundles, the release notes, and the flashing guide. The firmware source code lives in a separate, private repository.

## Which GCU is in my car?

Rush has shipped two GCU generations. Pick the right one before you flash.

| | **Active GCU** | **Legacy GCU** |
|---|---|---|
| **Fitted to** | Newer builds (Gen2, drive-by-wire) | Earlier builds (Gen1, throttle cable) |
| **Hardware** | Small flat black box, one multicolor LED | Large grey box, two metal connectors, red/yellow/green LEDs |
| **Firmware** | **5.x** (`.bin` files) | **3.x** (`.hex` files) |
| **Flashing** | USB-C on the piggyback harness (dealer-installed if absent) | USB-B on the unit |

Not sure which you have? Gen1 cars have a throttle cable at the pedal box; Gen2 cars have an accelerator pedal sensor (no cable). The Active GCU also reports firmware 5.x on connect — the flasher prints the version automatically.

## Get the firmware

Grab the latest bundle from [**Releases**](../../releases). Each release zip contains the firmware for the relevant unit(s) plus the GCU Flasher app:

- **Active GCU (5.x)** — `release_CAN_feather-X.X.X.bin` / `release_KLine_feather-X.X.X.bin`
- **Legacy GCU (3.x)** — `release_CAN-X.X.X.hex` / `release_KLine-X.X.X.hex`

## Flash it

See [`docs/flashing.md`](docs/flashing.md) for the full step-by-step — the USB cable, the GCU Flasher app (macOS + Windows), picking the right firmware file, and the built-in serial console for diagnostics.

## Version history

[`CHANGELOG.md`](CHANGELOG.md) is the source of truth for what changed in each release. Older versions (3.0.3 and earlier) are not published here — contact Rush Auto Works.

---

*Maintained by Rush Auto Works. The [owner's manual GCU pages](https://manual.rush.sr/maintenance/electronics-and-wiring/gcu/README) mirror this repo's releases.*
