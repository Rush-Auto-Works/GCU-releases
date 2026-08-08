# GCU Firmware Changelog

Release notes for the Rush SR Gear Control Unit firmware. This file is the source of truth for version history; the [owner's manual GCU pages](https://manual.rush.sr/maintenance/electronics-and-wiring/gcu/README) mirror it.

## 5.0.0 — August 2026

**The first release on the Active GCU** — a development cycle's worth of shift-smarts, logged and tagged so the box tells you what it did. The Active GCU now drives the brake light, every auto-downshift refusal is explained in the logs, and shift traces record exactly where the shift drum went.

- **The GCU drives the brake light.** Brake pressure from the dash's brake channels switches the brake light on and off — no more chasing a relay. Failsafe is fail-bright: if the dash goes quiet or a sensor reads out of range, the light comes on rather than staying dark. A bench mode (`BRAKE_TEST`) lets you force the light on for wiring checks without the engine running.
- **Auto-downshift refusals are visible.** Hold the down paddle and the GCU walks the box down toward redline. Every time it declines a shift — revs still climbing, wrong conditions, no fresh data — it now says why, in the logs and on the dash. No more silent "hold did nothing."
- **Shift logs tell the truth.** Every upshift now records where the drum actually went (not just "it shifted"), shift success/fail counters are readable without a dash, and twice as many shift traces survive an outing so a problem shift is more likely to be in the log you pull.
- **Settings saves no longer lie.** A failed write to flash now reports failure instead of saying OK.
- **Gentler neutral finder.** The progressive neutral pulse is configurable (5/10/20/30/40 ms) instead of one fixed value.
- **Flasher improvements.** It enters the bootloader on its own before flashing, and the Sessions viewer got a proper dialog and scroll-pause.

**Flasher note:** this release contains `.bin` files for the Feather-M4-based Active GCU, not the legacy `.hex` files. The Active GCU flasher is built into the same app.

## 3.1.1 — July 2026

**You can set the compressor cut-in and cut-out pressures yourself now.** They still ship at 70 and 90 PSI, so nothing changes unless you change it.

- **Set it from the flasher**: the Compressor row shows the band the GCU is running. Change the numbers, click Save, and it stores them. The setting survives a power cycle and a reflash.
- **Bad numbers get refused**: cut-in has to be 50 PSI or higher, cut-out 130 or lower, and cut-out at least 10 PSI above cut-in.
- **Only before you've shifted**: saving briefly stops the GCU watching the paddles, so it only allows the write before the first shift after power-on. Set the band in the paddock.
- **Shift timing doesn't follow the band**: shift length still tracks actual tank pressure. Moving the band changes when the compressor runs, nothing else.

## 3.1.0 — March 2026

**Much faster sequential shifting.** Each shift now completes in about 180ms (previously 325ms), allowing approximately 5.5 shifts per second instead of 3. You'll notice the difference on fast downshift sequences.

- **Faster shifts**: Reduced the wait time between shifts by over 70%. The air cylinder returns fast enough that the old delays were unnecessary.

## 3.0.6 — October 2025

**Shifts adapt to tank pressure.** The GCU now automatically adjusts shift timing based on how much air is in the tank.

- At low tank pressure, shifts take a bit longer to make sure they complete reliably.
- At normal pressure (70–90 PSI), shifts behave as before.
- At high pressure, shifts are quicker since there's more force available.

You don't need to do anything — this happens automatically. The result is more consistent shifts regardless of tank pressure.

## 3.0.5 — June 2025

**Diagnostic LED improvements.**

- **Startup self-test**: When the GCU powers on, the red, yellow, and green LEDs light up in sequence. This confirms all three LEDs are working.
- **Compressor indicator**: The yellow LED now flashes while the air compressor is running. Useful for confirming the compressor is cycling on and off correctly — if you suspect a compressor issue, watch the yellow LED.

## 3.0.4 — June 2025

**First stable release with countershift.** Countershift sends a brief reverse air pulse after each shift to help the gear fully seat, reducing the chance of a missed or incomplete shift.

- Separate shift timing for upshifts and downshifts
- Improved shift light behavior

## 3.0.3 and earlier

Contact Rush Auto Works for firmware files for older versions.
