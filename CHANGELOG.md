# GCU Firmware Changelog

Release notes for the Rush SR Gear Control Unit firmware. This file is the source of truth for version history; the [owner's manual GCU pages](https://manual.rush.sr/maintenance/electronics-and-wiring/gcu/README) mirror it.

## 5.1.2 — November 2026

5.1.2 fixes 2-1 downshifts that timed out while the compressor ran, on cars whose compressor still grounds through the stock harness. It also adds per-gear shift timing trims, three shift-health alarms for the dash, and a session fuel total that survives a brownout, plus a round of GCU Utility fixes. It is the first release since 5.0.0 on the public download page, so it also carries everything in [5.1.1](https://github.com/Rush-Auto-Works/GCU-releases/releases/tag/v5.1.1) and [5.1.0](https://github.com/Rush-Auto-Works/GCU-releases/releases/tag/v5.1.0), which were internal development builds (the GCU Utility, shift lockout, the compressor watchdog and the rest). Install it on any GCU Mk3.

### Shifting and the gear sensor

- 2-1 downshifts with the compressor running close on the gear sensor again instead of timing out. On a car whose compressor still grounds through the stock harness, the compressor drags the 1st-gear reading under the sensor-fault line for a few milliseconds at a time, and each dip used to drop the gear mid-shift: one car at COTA on 5.1.0-rc6 timed out 13 of 15 such downshifts. A dip with the compressor on is now ignored until it lasts long enough to be a real fault (100 ms), and it is never read as a gear. The compressor-droop learner also learns in 1st now. Cars whose compressor is grounded straight to the battery and set `relay_flyback_installed` to 1 are unaffected.
- New per-gear shift timing trims, one for each up and down pairing (`shift_trim_1u2` to `shift_trim_5u6`, `shift_trim_6d5` to `shift_trim_2d1`), -200 to +200 ms, default 0. Use one to lengthen or shorten a single stubborn gear change without touching the rest. The valve pulse never drops below 50 ms.
- Auto-downshift: a down paddle shorted to ground no longer escapes the stuck-paddle lockout when the wire also picks up electrical noise.
- The compressor start hold-off no longer carries one shift's wait into the next when a tank-pressure sample is unreadable, so the next shift gets its own full wait.
- The legacy neutral shift refuses a direction that is neither up nor down instead of firing the downshift valve.

### Dash and CAN

- Three shift-health alarms for the dash, on CAN and in `DUMP_STATUS` (`SHIFT_HEALTH`): a live gear-sensor fault (`0x701` byte 5 bit 5), closed-loop shifting lost at any point this session, and a count of back-to-back failed shifts. A gear-sensor dropout mid-shift is now logged as `GP_SENSOR_FAULT` instead of the shared `CAN_ERROR`.
- The session fuel total on Suzuki CAN cars survives a brownout or watchdog reset. It still clears on a normal power-on and on `FUEL_RESET`.

### GCU Utility

- Flashing no longer freezes the window when bossac hangs instead of answering; it gives up after 1.5 seconds and says why.
- Pressing Connect a second time no longer shows a live connection as Disconnected.
- Two dialogs open at once no longer hand each other their answers.
- Logs: a session's length runs from its first record to its last, so a parked session no longer reads as a few seconds long.
- Logs: an import, rename, delete or notes save that worked but could not be written to the library's audit log now shows the library's warning beside it, and a delete is no longer reported as refused.
- Logs: an answer the sessions pages cannot read is refused with a reason instead of being shown as imported or crashing.
- Logs and Live Data open faster, and long session names are no longer cut short before they have to be.
- Advanced: starting a bench test can no longer be queued twice, and the "Stop the car, then press Begin Bench Test" hint clears once the car is stopped.

### For developers

- Every release archive now carries `gcu-identifiers.json`, the list of names this firmware publishes (tunables per build, serial commands, `DUMP_STATUS` rows, heartbeat fields, shift sources, flash events). Documentation outside this repo pins to it.
- On a release tag, the Skill Release workflow opens a pull request that refreshes the manual's copy of the log-reading skill.
- The build stops when a firmware image it means to ship is missing, and the macOS build preflight refuses at once when no Command Line Tools are selected.
- `scripts/feather-flash.sh` no longer fails after a good write when macOS brings the board back under a different port name.
- The bench CAN partner sends the real Suzuki 0x1A1 frame and AiM dash frames from a scripted lap.
- The Developer Simulator shows tank pressure and shift counts in Live Data, keeps its scroll position, and the Utility no longer dials a stale simulator port.
- Release and test tooling: the shipped-text copy-site gate, the release-artifact guard (one pass per archive), the tunable-docs check (real C preprocessor), the error-code docs parser, the capture and VM screenshot tools, the duplicate-proc and fixture-version checks, and the journey matrix's scratch cleanup all got fixes and tighter self-tests. Details are in the merged pull requests.
- The release-artifact guard no longer fails a clean archive because its compressed bytes spell a word it looks for by chance.

## 5.1.1 — November 2026, internal development build

Internal development build, never posted for download. Everything in it ships in [5.1.2](https://github.com/Rush-Auto-Works/GCU-releases/releases/tag/v5.1.2), the build to install.

5.1.1 adds shift lockout, a setting that refuses the paddles while the car sits still at idle so a bumped paddle cannot put a gear in. It also makes the compressor droop correction safer, makes logging and settings saves more robust, and rebuilds large parts of the GCU Utility: a new Logs page with plain-language event cards, a Live Data dash, a status bar, and a Settings page where each setting is edited in place. Install it on any GCU Mk3.

### Shift lockout

- New shift lockout, on by default as `shift_lockout` (CAN cars only). While the car sits still at idle with the throttle closed, the paddles are refused, so a bumped paddle cannot put a gear in while the car warms up or is pushed. Finding neutral from 1st or 2nd is not affected, and any missing or stale input turns the lockout off.
- On a car with the dash's ClutchSW channel (`0x712` byte 6) and a proven clutch switch (pressed once since power-on, or `clutch_switch_fitted` set to 1), the lockout arms whenever the clutch is out, and pulling the clutch lets the paddles shift. On a car with no proven clutch switch, it arms in a trusted Neutral and stays off once the car is in gear.
- Ways out: hold the N button and pull a paddle to shift out of Neutral on any car, or pull either paddle three times within 5 seconds (any mix of up and down) to turn the lockout off until the next power cycle. A car with an auto clutch that idles in gear with the clutch out turns it off by itself after 2 seconds when the gear is measured. An auto-clutch car with no valid gear source should set `shift_lockout` to 0.
- If the dash stops sending its frames, the clutch reading now goes stale after 300 ms instead of 5 seconds, so a stale "clutch released" reading cannot keep the paddles refused. `DUMP_STATUS` reports the lockout as `SHIFT_LOCKOUT`, the flash log records `SHIFT_BLOCK_LOCKOUT` and `SHIFT_LOCKOUT_ESCAPED`, and the GCU Utility shows both settings.

### Shifting and the gear sensor

- The compressor droop correction can no longer be set by one bad compressor reading, and it will not report a gear the reading does not settle. When the fixed correction and the learned correction disagree about which gear a reading means, the GCU refuses paddle shifts and neutral commands, stops an active neutral search, and logs `SHIFT_BLOCK_UNSETTLED` until the gear sensor confirms a reading. The car does not drop into passive mode.
- A 1-2 or 2-1 that read its target but ran out of time before the settle dwell ended now gets the same `post_shift_validate_ms` bounce watch as a clean shift. A bounce that the retry rescues replaces the timeout it booked, so one shift records one verdict.
- When a shift ends with no reading from the gear sensor, the reported gear now falls back to the CAN gear at once instead of staying at the previous shift's landing. Before, a second shift finishing within 200 ms of the first could be read as the first shift's gear for up to about 45 ms.
- Auto-downshift: letting go of the paddle in 1st or neutral during a walk now ends the walk cleanly (the next hold could fail to start a walk), and switching the feature off during a downshift and back on no longer counts that old downshift as a fresh one.
- A shift the GCU refuses (over-rev, bad CAN data, an inferred gear, no gear to go to) no longer throws away the previous shift's trace, and a neutral shift started while another shift is running is refused like every other start.

### Settings and logging

- Each closed-loop shift now writes one outcome record, the final verdict. A shift that reached its gear, bounced out and failed the retry logs one failure whose reason starts with "bounce:", where before it logged both a success and a failure. Time-based shifts (no GP sensor, or passive mode) now log their own target and timeout on the start line.
- A session that spans more than 8 log files now lists and sends every file. Before, the session list and download stopped at the first 8 yet reported the transfer as complete, so later files could be pruned without ever being imported. This affects cars that ran 5.0.x boots between 5.1 boots.
- Logging holds up better when flash misbehaves. A failed delete of old sessions is retried on every later write until it works, so logs cannot grow past their flash budget. A failing prune or session index write is retried at most once every 30 seconds, and `DUMP_STATUS` shows a stuck prune as `LOG_PRUNE`. Logging reports ready only after the boot header is written, and a boot whose flash log cannot start still loads your saved settings and car identity.
- `RESET_CONSTS` now answers `ERR RESET_CONSTS_FAILED` when the saved settings file could not be removed or rewritten, or flash is not mounted. It used to answer OK regardless, so the next boot reloaded the file it claimed to have deleted. A reset that cannot persist now keeps the file, which can be the only copy of the hardware facts.
- If the GCU cannot read its hardware record (GP sensor fitted, relay flyback) at boot, Save no longer overwrites it. The other settings are saved, the GCU answers `OK SAVE_CONSTS held=hardware`, and the Utility tells you to restart the GCU first. If it cannot read the saved chassis identity, assigning a new one is refused instead of writing over it. Restore Factory Settings lifts either hold, and a board with no identity saved yet is not affected.
- Serial: a command typed while a log dump is still closing no longer prints inside the dump. One-line replies wait until the dump ends, and a command that answers with its own block (help, constants, status and the like) is refused with `ERR DUMP_FRAME_OPEN` until the dump is done. The end of a command line longer than 64 characters is now always discarded instead of possibly running as a command of its own. With the engine off, the framed replies (`SESSION_LIST`, `HIST_GET`, `GET_CONSTS` and others) wait longer for a slow reader, so a Utility that stops reading for a moment no longer gets a truncated session list. `FLUSH_LOGS` writes a pending session-index change as soon as it is sent. A heartbeat legend lost while a log dump held the serial output open is written again right after the dump instead of waiting out another 10 seconds.

### Updating and downloads

- The standard download now includes the public KLine firmware image beside the CAN one, so a KLine car can update from the released package. The build fails if either is missing.
- GCU Flasher for Mac now needs macOS 26 or newer, and says so to macOS, so an older system refuses it up front instead of failing inside the app. The GCU Utility app declares the same floor.
- The post-flash check now compares the build the GCU reports with the image that was written. A mismatch ends in "Wrote the image but the GCU reports something else: Build" with Retry, instead of a success on version alone. An update whose connection drops during the final version check ends in "could not confirm the version" after 30 seconds, with Retry, and the Utility reopens the board's new port if the first open is refused.

### GCU Utility: Logs

- Logs can import a saved GCU log file from disk (Import a Log File...), with no GCU needed. Its report, flags and cleanup work like any session's, and a refused file says "Could not import" with the file name, the reason and a way to choose another.
- Important events now lists one card per thing that happened instead of one row per log record. A missed downshift reads "Requested 2nd. Reported Neutral." with the firmware's explanation, "Cause: Not established by this log.", "Next step: Save the report for your mechanic.", an Export report... button that saves an HTML report, and the measurements behind a Technical details button. View this shift in timeline opens the report on the event's rows. Summary counts now count events, so three retries on one miss read as one missed shift.
- Reports are honest about partial logs. A log that stops early says "No problems found in the available portion", a log that lost shift records while logging says "in the records that were kept", and a saved log whose top-tier records were evicted no longer reads "No problems recorded".
- The page is quieter and easier to scan. The Sources column is gone, replaced by one top row with a button that hides or shows the session list, a drop-down (On This GCU, All Sessions, Recent, Flagged) and the Sessions and Safety & Fault History tabs. Picking a session no longer hides the list, which can fold to a narrow rail. Rows show the title, then date, length and shift count, then where the session lives and what it recorded. Getting sessions off the car now says Download, and a laptop with no logs gets one block of steps for getting them off the car. Delete empty saved sessions is its own task behind Clean up saved sessions..., showing how many saved copies match, with flagged and unfinished copies kept. A session with a warning or critical event is never offered.
- Safety & Fault History says what it covers, names the connected GCU, uses the same wording as the events list ("Missed downshift"), has a Back to history list control, and no longer sticks on "loading" when the GCU never answers or the link dies. A watchdog or brownout reset reads as "GCU reset", and a gear sensor dropout mid-shift reads as a sensor fault, not a CAN bus error.
- Sessions from each GCU are now kept apart: a second GCU whose `S0-1` is a different log no longer reads as already saved on this laptop. A session download that ends without an outcome is rejected as truncated and can be retried, and retrying a stalled download from 5.1.0-rc1 to rc3 firmware no longer saves heartbeat or status lines in place of session data.
- A GCU reset during an import no longer leaves Logs stuck: the transfer fails with a reason, the rest of the batch stops with a note, and Import comes back once the GCU restarts. Logs also lists the GCU's sessions again after a reset. Layout fixes keep the NOT COMPLETE banner, buttons and tiles inside the window at the smallest size, and Logs and the session report open faster.

### GCU Utility: Live Data, Settings and connection

- Live Data opens on a dash showing gear, RPM, GPS speed, tank pressure, front and rear brake, throttle and the car's clock, with CAN health and warnings on one line. Only a caution or critical value is coloured, and it always carries a word too. Detailed panels are behind Show details. The status bar now shows the connected car's gear, RPM and tank pressure on every page, with a symbol as well as a colour for a compressor fault or RPM at the redline.
- Settings is rebuilt so each setting is edited where it is listed, with its plain name and description, factory and saved values, a control that fits it (checkbox, dropdown, or number box with its range), a Saved, Temporary or Applying status, and its own Apply Temporarily button. Values are checked before they are sent, and each setting reports its own result in plain words. When the GCU restarts and loses temporary changes, Settings says so. With no GCU connected, it lists settings in the GCU's own order so related ones sit together.
- Settings warns when the car's timezone (`tz_offset`) and the laptop's zone disagree, and Set from Laptop applies the laptop's zone, so a car left on UTC no longer writes every session with the wrong local time unnoticed. `tz_offset` refuses 15 through 98, which the GCU treats as "not set", and says "-12 to 14, or 99 for not set".
- Connection handling is sturdier. When the link to the GCU wedges, the Utility shows Disconnected with the reason and reconnects on its own. A late answer to a timed-out command can no longer be taken as the answer to the next one. A stalled session list is asked for once more before the Update page refuses to flash. On Windows, a leftover or busy port listed beside a GCU no longer stops one-click connect.
- Advanced bench test: shift and brake labels now wait for the GCU's own reading ("unconfirmed" if none arrives), and a refused shift names the GCU's reason instead of "refused (shifting=1)". The Hold to Run button no longer leaves the compressor on when you hold Space on Windows, and releases if focus leaves it mid-hold.

## 5.1.0 — October 2026, internal development build

Internal development build, never posted for download. Everything in it ships in [5.1.2](https://github.com/Rush-Auto-Works/GCU-releases/releases/tag/v5.1.2), the build to install.

**5.1.0 introduces the GCU Utility desktop app, closed-loop shifting and gear-range safety on KLine cars, a compressor refill watchdog, and per-car gear sensor and compressor correction.** It also makes the GCU's logs much harder to lose or corrupt, and it adds an owner-readable shift record that says whether each shift worked. 5.1.0 never had a final public build: it went out as test builds 5.1.0-rc1 through rc7, and everything in them reached owners in 5.1.1. These notes describe the combined changes since 5.0.0. Run this release's GCU Utility with this firmware: a 5.0.0 Utility connects to 5.1 firmware but never fills its Config tab, and an older Utility cannot import logs from it.

Two changes need you to act. A car that has ever saved its settings keeps the old 70/90 psi tank band until you run `SET tank_min_psi 85`, `SET tank_max_psi 105` and `SAVE_CONSTS`. A dash or AiM channel that decodes `0x704` bytes 6-7 as counts has to be re-pointed to millivolts.

### Shifting and the gear sensor

- Shift records now say whether the shift worked. `SHIFT_OK_*` means the drum confirmed the gear, and `SHIFT_FAIL_*` means the valve fired and the drum never arrived. A refusal at either end of the drum is `SHIFT_BLOCK_TERMINAL_GEAR` and no longer counts as a failure. Every accepted shift also writes a `SHIFT_BEGIN` and `SHIFT_END` pair, so a shift is still on record when its optional trace is lost. Neutral shifts get a start line too, and serial bench shifts log as `src=serial` instead of reading as ghost or double shifts.
- New tunable `gear_settle_ms` (0 to 40 ms, default 15) holds the shift valve open a little longer after the gear confirms, so a drum that drifts out of the target gear is not booked as a success. It also holds the ECU cut or blip for the same time, so a confirmed shift now sends the cut 15 ms longer than on 5.0. A shift whose gear confirms too late to finish this wait is reported as a timeout. `gear_settle_ms 0` restores the 5.0 timing.
- KLine cars get closed-loop shifting and the gear-range safety gates. A KLine build used to have neither: an upshift from 6th or a downshift from 1st fired the valve. With a healthy gear sensor the car now closes the valve when the drum confirms, blocks shifts past either end, and drops to passive mode if the sensor dies. A KLine neutral shift now checks that it actually found N and logs a failure if it did not.
- Gear detection no longer trusts a false N. With the compressor running, the sensor can read 2nd low enough to land in the N band. The GCU now refuses an N the drum cannot have reached and uses the CAN gear or the last gear it saw (logged as `GEAR_MISMATCH`). In moto mode the NT button is refused in that state, and a downshift is refused when the compressor drops the sensor into N after a downshift from 3rd or above, until the ECU catches up or the sensor reads a gear again. A 2nd to 3rd upshift that times out with no 3rd confirmed no longer fires the countershift pulse, which could knock a drum still in 2nd into neutral. A shift pulled right after another one now judges the live drum instead of a frozen reading, and a CAN gear the ECU stopped reporting goes invalid after 500 ms (`CAN_TIMEOUT_GEAR`), so it can no longer be used for a money-shift check.
- Misshift and bounce retries work without an RPM reading, so a KLine car, a CAN car with no RPM frame and a bench shift with the engine off can all retry. Post-shift bounce checking (`post_shift_validate_ms`, still off by default) now uses the gear the GCU trusts, so it works on KLine cars too. Every full shift sends the gear-shift signal to the ECU, including N to 1st, N to 2nd and a shift from an unknown gear. A car-mode N to 1st now blips and a moto-mode N to 2nd now cuts.
- Paddle noise is handled. A relay or solenoid transient no longer counts as a press or a release, release bounce no longer starts a shift, a stray HIGH reading on a held down paddle no longer drops an auto-downshift walk, and noise on a held paddle can no longer turn one pull into several shifts. Rejected presses reported on `0x702` now count each re-pull in a shift.
- Auto-downshift is faster and lands lower. It no longer waits out the background trace after a confirmed shift, which paces the walk at about 300 ms per gear in the shift timeline (it measured 536 ms per gear on a car before; the new pace has not been measured on a car yet). New setting `auto_downshift_max_rpm` (CAN builds, default 10000, range 7000 to 11800) caps where an auto step may land, so a walk no longer lands just under the money-shift block. A step held back by it counts as `ceiling=` on the `AUTO_DS_VETO` line in `DUMP_STATUS`. The 4 second hold limit and the stuck-paddle lockout restart each time a downshift lands and is confirmed, so a long walk through a braking zone is no longer cut off partway.
- The neutral mode labels now match what the paddle does. Car mode (`n12`): the down paddle from 1st finds neutral. Moto mode (`1n2`): that paddle is blocked and N comes only from the NT button. The mode you set by holding both paddles now survives a power cycle on every car. If the save fails, the serial line `WARN neutral mode not saved` says the mode will revert.
- The GCU no longer does flash work in the middle of a shift. The first GPS time fix is kept in RAM and written after the shift ends, and every serial command that writes flash (`SAVE_CONSTS`, `CLEAR_ROLLING`, `FLUSH_LOGS` and the rest) answers `ERR SHIFT_IN_PROGRESS` during a shift. Log reads (`SESSION_LIST`, `SESSION_GET`, `DUMP_ROLLING`, `DUMP_EXCEPTIONS`) are refused during a shift or with the engine running.

### Compressor and air

- The compressor shuts itself off when a refill stalls. Below `tank_min_psi`, the relay latches off when a run gains less than 2 psi in the stall window, hits the maximum on-time backstop, or the tank sensor reads garbage. That logs `COMPRESSOR_TIMEOUT`, and `COMPRESSOR 1` answers `ERR COMPRESSOR inhibited` until `COMPRESSOR 0` or a reset. A stall inside the band logs `COMPRESSOR_RELIEF_SUSPECT`. These limits are not calibrated on a car yet.
- Tank pressure reads the sender that is actually fitted. The conversion is now a table measured on two cars for the Ashcroft sender, the compressor band is 85 to 105 psi, and the critical cutoff moves from 110 to 125 psi. `tank_min_psi` and `tank_max_psi` can no longer be set inverted: the value you just set wins and the other threshold moves to meet it, logged as `CONSTS_MIGRATED`. `DUMP_STATUS` returns a `TANK_PRESSURE adc=... psi=...` line so you can check it against a mechanical gauge without running the compressor.
- The compressor no longer starts in the middle of a shift. Its relay adds a voltage step to the gear reading, and starts used to land while the GCU was waiting to confirm the new gear. An automatic start now waits for the shift to end, for at most 500 ms, and starts at once if the tank is more than 5 psi under `tank_min_psi`. `COMPRESSOR 1` and a compressor that is already running are not affected.
- Gear detection corrects for compressor droop. The running compressor pulls the gear reading low, which could make a 3 to 4 upshift miss or run to its timeout. The GCU now measures this on each car: every time the compressor switches on or off away from a shift, it compares how far the reading moved with the old fixed correction and scales the correction in every gear to match. Right after power-up it uses the old fixed correction until the first clean measurement, nothing is stored, and each measurement is logged as `DROOP_LEARNED`. Set `relay_flyback_installed` to 1 on a car whose compressor wiring is fixed to turn the correction off.
- CAN cars also learn where each gear sits on the gear sensor and move the gear bands to fit. When the compressor is off, no shift ran in the last second and the ECU's gear is steady, the GCU keeps a running average of the sensor reading for that gear. Once a gear has a few samples, the edges beside it move to halfway between neighbours. Until then, and after every power-up, the standard table is used. Neutral is never learned, KLine cars keep the standard table, and each change logs `BAND_LEARNED`.
- Two settings describe how the car is wired, so they are now kept: `relay_flyback_installed` and `gp_sensor_fitted` (set it to 0 on a car whose gear sensor is absent, unplugged or dead, so a floating input is not read as a real gear). Restore Factory Settings, firmware updates, an unreadable settings file and a trip back to 5.0 all leave them alone. Only setting them again and saving changes them.

### Dash and CAN

- `0x704` bytes 6-7 (`FBKA`) now carry the front brake sensor in millivolts, 0 to 4477 mV, not raw counts, and a shorted or unplugged sensor reads 0 mV. A dash or AiM channel that decodes these bytes as counts has to be re-pointed.
- New CAN channels for dash and AiM diagnostics. `0x705` bytes 4-5 carry the gear sensor output in millivolts, what a meter on the sensor wire shows. `0x702` bytes 6 and 7 count up and down paddle presses the GCU dropped without shifting. `0x703` Shift Result now goes out every 1 s instead of every 5 s. Corner minimum and straight maximum speed publish on `0x705` in mph, from AiM GPS speed, with confirm windows set by `corner_min_accel_confirm_ms` and `straight_max_brake_confirm_ms` on CAN builds.
- The dash status byte (`0x701` byte 6) shows every active warning and clears again. Before, each warning overwrote the whole byte and a money-shift block from the out lap could still be lit at the chequered flag. A shift block now holds for 3 s from the first frame that reaches the wire, and a CAN bus-off lights the CAN-error bit (byte 6 bit 7), which it never did before. The money-shift and invalid-CAN block counts in `0x703` stop at 15 instead of wrapping to 0.
- On a Suzuki car, throttle and grip now reach the GCU from the real `0x1A1` frame. The firmware used to read them only from `0x102` and `0x101`, which no Suzuki car sends, so every logged shift trace showed `tps_pre:0`. Nothing that decides a shift reads either value.
- On a Suzuki car the GCU keeps a session fuel used total. It adds up the ECU's instant fuel channel (`0x221`) over time and sends the total once a second on a new frame, `0x706`, in tenths of a mL. `DUMP_STATUS` shows it on a `SESSION_FUEL` line, Live Data shows it, and the new `FUEL_RESET` command zeroes it. The total starts at 0 on every power-up. The scale is an estimate that no measured fill-up has checked yet, so treat the number as relative.

### Logging

- The GCU keeps its vehicle identity across a reboot. Before, every power cycle and every firmware flash came up unassigned and Update Firmware failed with `Identity: unassigned after update`.
- The heartbeat is a legend plus a values row, so it can no longer outgrow the wire. The old keyed `HB` line could reach 275 bytes against a 254-byte cap and a split line lost its last number. The firmware now sends `HBK` (the key list, about every 10 s) and `HBV` (the values, once per second). An older Utility shows Live Data as Waiting on a car with this firmware.
- A long stint no longer loses the oldest shift records first. When the log queue fills on track, the GCU drops routine records (compressor, wheel-speed) first, then shift traces, and keeps shift ends and every failure record longest. In one real session mix, shift outcomes and failures now last about 58 minutes of continuous track time instead of about 19. Dropped records are counted, the count reaches flash as `LOG_DROPPED`, and `DUMP_STATUS` shows it on a `LOG_DROPS` line.
- Logs are saved to flash in batches of about 3.5 KB instead of one record at a time. Replaying one session's 570 records took 46 block erases instead of 623, so the flash wears less and a full queue drains faster in the pit. When flash fills, the GCU now deletes sessions that logged nothing before older sessions that did, so a bench boot can no longer push a real outing out of flash.
- Log timestamps are honest about the timezone. A car that was never told its timezone stamps UTC with a trailing `Z` instead of a confident local time, `tz_offset` is now a public tunable on CAN builds, and a record keeps the timezone it was written under when you change `tz_offset` later. The boot record includes the firmware's Git hash and build time, every boot logs the settings in effect, and `DUMP_STATUS` now names the reset cause correctly: a real core brownout used to read as `power-on`.
- A dump or log transfer that was cut short no longer closes like a complete one. `DUMP_ROLLING` and `DUMP_EXCEPTIONS` now end with `status=complete`, `status=truncated reason=stall` or `status=truncated reason=read_error`, and other framed replies that lose a line stop without an `END`. The Utility warns that the log is incomplete and refuses to analyze it. Every complete log the GCU sends also ends with a checksum, and the Utility discards and re-reads a copy that does not match. The GCU's own status lines no longer land inside a session transfer and break its checksum, they wait until it closes. Clearing logs can no longer reset the GCU when the computer on the USB cable stops reading, and flash errors no longer print raw serial under the watchdog.
- The log system survives bad reads. A flash read error at boot no longer erases anything: the GCU retries, formats only a chip that reads fully erased, and otherwise runs with logging off for that boot. If the saved settings file cannot be read, `SAVE_CONSTS` and the paddle neutral toggle are refused instead of writing defaults over your tuning. A session index that cannot be read is not replaced by an empty one, so session titles survive. A saved vehicle identity that fails to write now says `ERR ID_WRITE save failed` instead of blaming the fields you typed.
- New diagnostic lines in `DUMP_STATUS`: `SETTINGS rejected=<n>` (the boot could not apply some saved settings rows, which stay at default), `STACK_FREE_MIN`, `ADC_A6` (a raw read of the `VDiv` input for bench checks), `DASH_STATUS`, and on CAN builds `WSS` with a `WSS_STATE` record on every change, so the logs can say whether the wheel-speed output was running. Session lists report each session's top speed as `vmax_mph` when an AiM dash is connected.
- If you save settings on 5.0, it deletes the settings 5.0 does not have, and they read their defaults once the car is back on 5.1 with nothing saying which ones. Check your per-car settings first and set any you changed again before saving on 5.1. On a public CAN build `tz_offset` goes back to unknown.

### Settings and bench tests

- The GCU reports which settings are unsaved. `DIRTY` answers `flash=<0|1> rows=<n>` and `GET_CONSTS` adds a `SAVED` row for each setting whose live value differs from flash, so a lost reply, a reconnect or an unsaved `RESET_CONSTS` still reads right. A car whose settings file was migrated or clamped at boot no longer shows phantom unsaved changes. `GET_MANIFEST` also describes each setting in words.
- Bench tests run on a lease. A bench command (`GSS`, `BRAKE_TEST`, `WSS`, `COMPRESSOR`) used to stay on if the laptop crashed mid-test. Now it runs under a 5 second lease that the Utility keeps renewing. When the lease ends for any reason, the firmware resets every output and reports what it read back. A manual `COMPRESSOR 1` stops after 60 s.
- Settings writes from the Utility reach the GCU: Apply Temporarily, Review & Save All Changes and Restore Factory Settings unlock write access for the write and lock it again. After Apply Temporarily the row stays selected and shows the value the GCU is running or its reason for refusing. Restore Factory Settings resets every setting except the two wiring settings, and its confirm message names them. Fixes in Settings and the Update page: Restore Factory Settings opens its confirmation, clicking a setting opens its value field, Discard puts each unsaved setting back to its saved value instead of resetting everything to factory defaults, and the Settings table scrolls and fits its window.

### GCU Utility: install, connect and update firmware

- The GCU Utility is one desktop app with six pages: Overview, Update Firmware, Live Data, Logs, Settings and Advanced. It ships for macOS and Windows, opens on Overview, connects by itself when exactly one GCU is attached, and offers a device menu when there are several. Help opens the GCU owner's manual, and nothing in the package needs Python. The old classic GCU Firmware Flasher window and its serial console are gone. A Raw Log window (Window, Raw Log on macOS; View, Raw Log on Windows) lists every command sent, every line received and every connection event, so a failed connect shows why.
- Update Firmware flashes a connected GCU, or a port with no GCU answer. It is refused while the engine runs or a shift is in progress, and your sessions, settings and identity are kept. The page shows the version written next to the version the GCU reports, and a board with no vehicle identity gets a warning instead of a failure. A refusal always says what happened and what to do next. Return to Production Firmware puts a car back on its matching public or developer build after a diagnostic build. A CAN GCU on public 5.0.0 updates to 5.1 in one step. Assign identity writes in one click: it opens write access, writes the identity, closes access again and tells you what the board was left with.
- Update Firmware reads a 5.0.x GCU's board type and starts on the matching target, CAN (Gen 2+) or KLine (Gen 1). A target from the other family is refused before anything is written. On a KLine car it warns that the GCU cannot tell whether the engine is running, so switch the engine off before you flash. A GCU on 5.0.0 or 5.0.1 connects, and a page that needs newer firmware says so with an Update Firmware button. A failed connect says what it found, offers Update Firmware, and lets go of the port so Retry works.
- Flashing is sturdier. The Utility waits 3 s after the bootloader appears before it starts, because starting within 500 ms made the write die mid-way on a test Feather. A write that hangs for 30 s is stopped, retried once, then reported with Retry and a window that can still be closed. On macOS the Utility bundles a native arm64 upstream bossac, which verifies again on macOS 27 and shows no Rosetta warning, and it refuses the Arduino fork of bossac that fails verify. On Windows it handles folder names outside the system code page, and the first connect no longer fails with `handshake failed: GET_MODE: timeout`, because the Utility waits 1.5 s after opening a COM port. Refreshing the port list is instant instead of taking about 10 s. The session list on a GCU with many sessions is no longer cut short by serial buffering, and a large log download keeps going while lines keep arriving.

### GCU Utility: pages

- Overview has a Device card (chassis, firmware, build, uptime, reset cause, session count, when this app last flashed the board, chip ID) and four task cards. Live Data is a board of headline tiles (Gear, Engine RPM, Tank pressure, CAN), grouped panels and a recent-activity strip, and shows a single "No GCU connected" state when nothing is attached. Old values never pass as current: a reboot clears the previous boot's numbers and a disconnect clears the ended session's.
- Advanced groups connection identity, access, the bench lease, System Readiness, bench controls and a read-only console. Opening Advanced starts the bench test when the engine is off and no shift is running. Bench controls show only while a lease is open. Export Console Capture saves every line received since the app started, with a marker for each connection.
- Pages repaint in place while the GCU is polled, so a scrolled page stays where you left it and Settings keeps the value you are typing. Cards, tables, status pills and dialog text reflow instead of being cut off at 144 dpi (150% scaling) in the 1200x720 window, which is now the minimum size. Windows draws text in Segoe UI. One failing part of the update loop no longer stops serial reads, reconnect and flashing for the whole app.

### GCU Utility: logs and sessions

- The GCU indexes its logs as sessions. A mid-run log rollover no longer looks like a second session. `SESSION_LIST`, `SESSION_GET` (resumable), `SESSION_TITLE` and `HIST_GET` give each boot a stable session id, a title and its fault history. Session ids stay unique after a 5.0 to 5.1 upgrade, and a GCU with more sessions than one list carries lists the newest and says the list is partial.
- The Logs page is a Device Sessions page with Sources, the sessions on this GCU, and a preview. Import runs only when you start it, one session at a time. A 5.0.x GCU has only its rolling dump, so Import Whole Log splits it into one session per boot, and a second dump imports only the new sessions. An import is byte for byte what the GCU stored, a retry resumes correctly, and a session the GCU kept recording into is updated in the library with its title, notes and tags kept. Importing, renaming, notes and deleting all run inside the Utility without Python.
- Sessions can be named, with the new title saved in the library at once and sent to the GCU when you apply it. Titles with accented letters or emoji are saved correctly, and a title too long for the GCU's command line is refused with the number of bytes that fit. Session rows show date, time, size, shift count and whether the copy is in the library or only on the GCU. Prune Empty, under Maintenance in Sources, removes library sessions with no shifts and no warnings after asking, and never touches anything on the GCU.
- The Session Report has Summary, Timeline and Raw Log tabs, editable notes, and a self-contained HTML export. A truncated or unreadable capture carries a `NOT COMPLETE` banner, and a raw log that fails its hash check says so. Safety & Fault History groups the GCU's fault records by session, and Open in Session jumps to that session's report. Log Analysis reads the rolling log or a saved capture and reports clean, flagged or unavailable, and it never shows a failure as clean.

## 5.0.0 — August 2026

**The first release on the GCU Mk3** — a development cycle's worth of shift-smarts, logged and tagged so the box tells you what it did. The GCU Mk3 now drives the brake light, every auto-downshift refusal is explained in the logs, and shift traces record exactly where the shift drum went.

- **The GCU drives the brake light.** Brake pressure from the dash's brake channels switches the brake light on and off — no more chasing a relay. Failsafe is fail-bright: if the dash goes quiet or a sensor reads out of range, the light comes on rather than staying dark. A bench mode (`BRAKE_TEST`) lets you force the light on for wiring checks without the engine running.
- **Auto-downshift refusals are visible.** Hold the down paddle and the GCU walks the box down toward redline. Every time it declines a shift — revs still climbing, wrong conditions, no fresh data — it now says why, in the logs and on the dash. No more silent "hold did nothing."
- **Shift logs tell the truth.** Every upshift now records where the drum actually went (not just "it shifted"), shift success/fail counters are readable without a dash, and twice as many shift traces survive an outing so a problem shift is more likely to be in the log you pull.
- **Settings saves no longer lie.** A failed write to flash now reports failure instead of saying OK.
- **Gentler neutral finder.** The progressive neutral pulse is configurable (5/10/20/30/40 ms) instead of one fixed value.
- **Flasher improvements.** It enters the bootloader on its own before flashing, and the Sessions viewer got a proper dialog and scroll-pause.

**Flasher note:** this release contains `.bin` files for the Feather M4 based GCU Mk3, not the legacy `.hex` files. The GCU Mk3 flasher is built into the same app.

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
