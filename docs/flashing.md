# Flashing GCU Firmware

How to update the GCU (Gear Control Unit) firmware — flashing over USB and using
the serial console for diagnostics.

## What you need

A USB-B cable (printer-style) to connect the GCU to a laptop. We like
[these right-angle cables](https://www.amazon.com/StarTech-com-USBAB2MR-Right-Angle-Cable/dp/B00G6SOG5K/).

> **Important:** some GCUs were manufactured with slim clearance to the USB
> port. Use a right-angle USB-B plug that is as slim as you can buy, for maximum
> compatibility. The linked cable is one of the best we've found.

## Steps

1. Download the release zip for your version from [Releases](../../releases).
2. Unzip it to a folder on your computer.
3. Connect the GCU to your computer via USB-B.
4. Open the GCU Flasher app:
   - **macOS**: double-click `GCU Flasher.app`
   - **Windows**: double-click `GCU Flasher.bat`
5. Select the correct firmware for your car:
   - **Gen2 (CAN / drive-by-wire)**: `release_CAN-X.X.X.hex`
   - **Gen1 (KLine / throttle cable)**: `release_KLine-X.X.X.hex`
6. Select your serial port from the dropdown (click **Refresh** if it doesn't appear).
7. Click **Flash Firmware** and wait for the "Flash complete!" message.

> Not sure which version you have? Gen1 cars have a throttle cable at the pedal
> box; Gen2 cars have an accelerator pedal sensor (no cable).

## Viewing the serial console

The GCU Flasher includes a built-in serial console for diagnostics. Click
**View Console** to connect to the GCU's serial output at 115200 baud, and
**Disconnect** to close it. The console is useful for verifying the GCU is
running correctly after a flash or for troubleshooting shift issues — see the
[GCU debugging guide](https://manual.rush.sr/maintenance/electronics-and-wiring/gcu-debugging)
for the output strings to look for and what they mean.
