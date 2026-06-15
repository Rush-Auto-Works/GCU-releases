# GCU Firmware Changelog

Release notes for the Rush SR Gear Control Unit firmware. This file is the source of truth for version history; the [owner's manual firmware page](https://manual.rush.sr/maintenance/electronics-and-wiring/gcu-firmware) mirrors it.

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
