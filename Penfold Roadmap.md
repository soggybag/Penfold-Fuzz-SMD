# Penfold Fuzz SMD — roadmap, notes and to-do

Discussion 2026-09-29. Baseline: **Penfold Fuzz SMD** (Rat-style drive → LM13700 VCA driven by an envelope follower; DRIVE, FILTER, DECAY, VOLUME + SENS trimmer).

## How the dynamics work now (from the schematic)

- **Envelope:**
  1. U1B amplifies the clean input (R13 2k2 + C14 leg, SENS trimmer RV1 500k → gain up to about 230).
  2. C15 4.7µ → **BAT54S voltage doubler** (a half-wave peak detector) → **C16 4.7µ hold cap** = ENV.
  3. DECAY discharges it: R14 4k7 + RV4 B1M to ground.
  4. **R15 47k** turns ENV into the OTA control current (U2 pin 1). R15 also drains C16, which is why decay tops out around 200 ms.
- **VCA:** half A of the LM13700. Signal in through R12 15k / R18 470 (÷33), a 3k9/3k9 + 22µ bias node, and **buffer A** (pins 7/8) as the output buffer with R20/R21.
- **Unused:** **OTA half B** (pins 12–16; its inputs are only tied to the bias node), **Darlington buffer B** (pins 9/10), and both linearising-diode pins (2, 15).

## Idea 1 — what to do with the extra OTA (and spare buffer)

Brainstorm, roughly in order of how much I like each for this pedal:

1. **Envelope filter after the fuzz (dynamic tone):** OTA B as a voltage-controlled low-pass, one pole with its buffer, driven by the *same* envelope. Pick hard → brighter and more open; as the note decays, the fuzz darkens and closes. It's a "Mu-Tron-lite" on top of the volume dynamics, and pairs naturally with the FILTER knob. A 2-pole version needs both OTAs, so one pole it is; still very audible.
2. **Dynamic blend clean ↔ fuzz:** OTA B as a second VCA on the *clean* signal, fed the *inverted* envelope, so the two OTAs crossfade.
   - Soft playing = fuzz, hard playing = clean, or the reverse with a toggle.
   - "Fuzz that cleans up when you dig in" (or blooms as notes decay) is a really musical, unusual control.
3. **Noise gate / downward expander:** OTA B after the fuzz, closing below a threshold on the envelope. The Rat stage at full DRIVE hisses; this silences it between notes. Needs a THRESHOLD trimmer or knob.
4. **Auto-swell / slow attack:** OTA B with a slow *attack* on its own envelope branch, for violin swells. Could share the path with the ripple fix below (separate attack/release).
5. **Effects-loop VCA:** see Idea 3. Half B could control the loop return while half A keeps the internal fuzz, or vice versa.
6. **Oddities:** OTA "self-multiplication" (signal into both the input and I_ABC) for octave-up grit; a sidechain compressor ahead of the Rat; a stereo second output.

**The spare Darlington buffer B has a clear job:** buffer the envelope hold cap (ENV → buffer → R15 → I_ABC). The OTA no longer drains C16, so DECAY becomes independent of the control path and can go much longer, and ripple drops (see Idea 2). It adds one resistor and costs nothing extra.

**My pick:** buffer B on the envelope (a free win), plus **OTA B as either the envelope filter (1) or the dynamic clean/fuzz blend (2)**. Both reuse the existing envelope, fit the pedal's "dynamic fuzz" identity, and need about one knob.

## Idea 2 — smoothing envelope ripple

The doubler is effectively a **half-wave peak detector**: it recharges C16 once per cycle of the note, so ENV has ripple at the note's own frequency (82 Hz on a low E). With short DECAY settings the ripple is large and becomes **amplitude modulation on the fuzz**: grit or a buzzy "flutter" on low notes. The trade-off is always release time vs ripple. Fixes, cheapest first:

1. **A second RC after the hold cap:** ENV → 10k → 1µ → R15. This makes a 2-pole smoothing filter, roughly −20 dB more ripple at 82 Hz, and adds only a few ms of lag. Drop-in, a few parts.
2. **Separate attack and release:** a series attack resistor (e.g. 470 Ω–2k2) before C16, so the peaks don't slam the cap. Attack becomes ~2–10 ms (also a "feel" control), and release stays DECAY.
3. **Buffer the hold cap** (spare buffer B, above): C16 is only discharged by DECAY, so a *larger C16 with a smaller DECAY resistance* gives the same release with less ripple.
4. **Full-wave precision rectifier:** two op-amp halves (another TL072). Ripple is at *twice* the note frequency and much smaller, and the envelope responds equally to both halves of the wave, which suits the asymmetric Rat/fuzz signal. Best result, most parts.
5. **Optional log/exponential control:** a transistor exponential converter into I_ABC gives dB-linear dynamics that sound more natural than the current linear V→I. Future refinement.

**Recommendation:** 1 + 2 + 3 in the next revision (a few passives plus the spare buffer). Keep 4 for a "Dynamics" version if we add an op-amp anyway, e.g. for the effects loop.

## Idea 3 — effects loop through the VCA

**Yes, it works.** It turns the Penfold into a **dynamics controller for any pedal or chain**: the envelope comes from your clean guitar, and the VCA shapes whatever comes back from the loop.

- **Routing:**
  - IN → buffer → **SEND** (clean guitar out to the loop), and the same buffer feeds the envelope follower.
  - **RETURN** → return buffer → VCA → OUT.
- **"Fuzz is there until you plug in":** use a **switched RETURN jack**. With nothing plugged in, its normalling contact routes the internal Rat into the VCA; plugging in a return cable replaces the internal fuzz with the loop. This is standard insert-jack normalling. You could also put the internal fuzz *in* the loop path, but the switched return is simpler and more flexible.
- **Great synergy:** Ugly Face (always full volume) in the loop gets real dynamics, which solves the Ugly Face "always on" problem without redesigning it. The same goes for synth, octave and bit-crusher pedals, and it gives delay/reverb "ducking-in" effects.
- **Details to handle:**
  - **Return level:** pedals in the loop can return several volts. Add a RETURN level trimmer ahead of the OTA's ÷33 attenuator (or make the attenuator adjustable) so hot returns don't distort the OTA.
  - **Envelope source:** default is the clean input. A toggle to follow the *return* signal instead makes it a gate/compressor on the loop.
  - **Jacks and enclosure:** IN, OUT, SEND, RETURN + DC is five connectors; four audio jacks on top of a 125B is tight. Options: a single **TRS insert jack** (tip = send, ring = return, with a Y-cable, as on mixers), or send/return on the sides.
  - **Grounding:** the loop adds cable runs; keep all jack grounds star-connected on the board (our IG/OG pad scheme scales to SG/RG).
- Fits well with OTA B: half A on the loop return, half B on the internal fuzz, both on one envelope → blend loop and fuzz dynamically. That's the "big" version.

## Proposed direction — "Penfold Dynamics" (v2)

```
IN ─► input buffer ─┬─► SEND ─► (external loop) ─► RETURN ─┐ (switched: internal Rat when empty)
                    ├─► Rat drive + FILTER ───────────────────┤
                    └─► envelope: full-wave / attack / DECAY ─► buffer B ─┬─► OTA A I_ABC (VCA on return/fuzz)
                                                                          └─► OTA B (envelope filter or clean/fuzz blend)
                                                         VCA ─► OTA B ─► VOLUME ─► OUT
```

- Probably a 125B (drilling to match the Hyper Fuzz family if the controls fit), plus a SEND/RETURN solution.

## Road map

1. **Phase 0 (current board, bench):**
   - Tack a 10k + 1µ RC between ENV and R15 and listen to the low-E ripple at short DECAY.
   - Try an attack resistor ahead of C16.
2. **Phase 1 (Penfold SMD r2, same enclosure):**
   - Buffer B on the envelope, a 2-pole smoothing RC, attack resistor, larger C16 with a re-scaled DECAY.
   - Fix anything found in the first build.
3. **Phase 2 — "Penfold Dynamics":**
   - Effects loop with a switched return.
   - OTA B as envelope filter or clean/fuzz blend.
   - Full-wave rectifier (extra TL072).
   - 125B.

## To-do

- [ ] Build/test the current Penfold SMD; note ripple and decay behaviour (low E, short DECAY).
- [ ] Phase 0: bench-test the extra RC and the attack resistor.
- [ ] Decide OTA B's job: envelope filter vs clean/fuzz blend (breadboard both?).
- [ ] Decide the loop connection: two jacks (side-mounted?) vs one TRS insert jack.
- [ ] Pick a switched jack (normalling contact) that fits the enclosure and footprint library.
- [ ] Check RETURN headroom into the OTA; add a RETURN level trim.
- [ ] Decide the envelope source toggle (input vs return).
- [ ] Draw the Penfold Dynamics schematic after Phase 0/1 results.

## Open questions

- Should the internal fuzz be *replaced* by the loop (switched return) or *mixed* with it (needs OTA B)?
- Envelope filter or clean/fuzz blend for OTA B, or a toggle between them?
- Keep SENS as a trimmer, or bring it to the panel now that the pedal does more?
- Discrete VCA option (from the Trem SMD, bench-proven 2026-10-02): see `Trem SMD/docs/VCA Building Block.md`. Verdict: keep the LM13700 here (two OTAs + buffers, fast envelope control, wider range); discrete only if the LM13700 becomes hard to source.

## v1.0 pre-order changes (2026-10-03)

- **DECAY fix (value-only):** R15 47k → **220k**, R20 20k → **100k**.
  - At 47k, R15 (envelope → OTA Iabc) drained the hold cap C16 in parallel with DECAY, so the knob did everything in its first ~10% and topped out at ~0.2 s.
  - R20 100k restores the output level lost with the smaller Iabc.
- **Fit a B250k DECAY pot (RV4), not B1M.** Range ≈ 20 ms → 0.55 s across the whole rotation.
- **SENS trimmer RV1:** 3296W → **Bourns 3362P 500k** (single-turn, top adjust), same footprint as UF1 v1.2. C4 moved down 0.4 mm to make room; board re-routed with `_tools/autoroute.py`.
- Pots and LED now excluded from the BOM/CPL in both the schematic and the board.
- **Bench watch-outs:** pick-attack thumps from OTA offset (no trim), and envelope ripple on low notes at fast DECAY.

## Dynamic fuzz vs clean-up distortion (2026-10-07)

Two related ideas came out of the Flatline expander discussion. Both use the same block: a clean input buffer and an envelope follower that listens to the **clean** guitar, driving a gain element (OTA or vactrol). Where the gain element sits relative to the clipper decides the effect:

| | **Dynamic fuzz** (this pedal) | **Clean-up distortion** (separate design) |
|---|---|---|
| Gain element | **after** the fuzz | **before** the clipper |
| Envelope controls | output **volume** | **drive** |
| Hard pick / soft or decay | loud fuzz / quiet fuzz, same character | dirty / clean |

**Decision:** keep them as separate pedals that share the envelope block. Penfold already *is* the dynamic fuzz (envelope → LM13700 VCA after the Rat stage).

**Test Penfold first** (boards ordered October 2026):
- Listen for **envelope ripple**: grain or fizz on low notes, worse at short DECAY. It comes from the BAT54S half-wave detector and the C16 hold cap.
- **If the ripple is audible, try an LED/LDR (vactrol) gain element in place of the OTA.** The LDR's slow response (~2.5 ms on, ~35 ms off) filters ripple on its own, and it's the Flatline's proven path. A quick test: drive a vactrol LED from the envelope (with a series resistor), and put the LDR as a series/shunt attenuator after the fuzz.
- If the OTA sounds clean, keep it: it's faster, repeatable and needs no vactrol.

**Later:**
- A Muff-style core in place of the Rat stage.
- The optical "Dynamic Loop" (SEND/RETURN, so any fuzz gets the treatment): see `Flatline SMD/Flatline Roadmap.md`.
- Both directions in one pedal: an LM13700's two OTAs, one before the clipper and one after, with a single DYNAMICS knob sweeping between them. Only if both separate versions prove themselves.

The clean-up distortion breadboard (LED/LDR, Flatline/Punch Line style) is in `~/Documents/KiCad/projects/Clean-Up Drive/`.

## Transient shaper: attack spike → lower sustain → natural fade (2026-10-14)

**Goal (from the v1.0 guitar test):** keep a heavily compressed fuzz from getting lost in a mix by restoring the pick attack. Each note should:
- jump up at the pick;
- decay quickly (adjustable) to a **lower sustain level**;
- then fade with the guitar's **own** decay.

This is what makes clean notes stand out. It's what a "transient designer" does (the SPL idea: the difference between a fast and a slow envelope).

**Why v1.0 can't do it:**
- The envelope amp clips, so ENV is a flat "note on" level with a release (DECAY) at the end, not the note's shape.
- There's only one control path into Iabc.

**Control law:** VCA current = **SUSTAIN × ENV** + **PUNCH × spike**.
- **ENV** must follow the note's real level. The envelope amp must not clip: lower SENS and add pre-emphasis. Buffer ENV with U3B (it's spare, now a parked follower), so the Iabc resistors don't drain C16.
- **spike** = ENV high-passed: a series cap that turns each rise of ENV into a pulse that decays with its own time constant (**ATTACK DECAY**, ~20–300 ms).
- The LM13700's Iabc pin is a current input sitting at ~1.2 V, so the two paths are simply **two resistors (or pot + resistor) summed into pin 1**:
  - **SUSTAIN path:** ENV → SUSTAIN pot / R15 → pin 1 (as now, just weaker).
  - **PUNCH path:** ENV → C_p → node X → diode → R_p → pin 1, plus R_d from X to GND.
    - The diode passes only positive pulses (the fade can't pull Iabc down).
    - R_d discharges C_p between notes; τ ≈ C_p·R_d sets how long the spike lasts.
- Controls: **PUNCH** (R_p as a pot: spike height), **ATTACK DECAY** (R_d as a pot), **SUSTAIN** (sustain-path pot), plus today's DECAY (release after the note). An optional **ATTACK** (resistor before C16) gives slow swells.

**Bench experiment on the v1.0 board (no cuts):**
1. Lower SENS until ENV (C16 +) rises and falls with the note instead of sitting flat (scope with a guitar).
2. Raise R15 220k → 470k (or put 220k in series): a lower sustain.
3. Air-wire the punch path from C16 + to U2 pin 1 (or R15's pin-1 end):
   - **C_p 1µ** (film or electrolytic, + toward ENV) → node X → **1N4148** (anode at X) → **R_p 47k** → pin 1;
   - **R_d 100k** from X to GND.
   - That's a ~0.1 s spike decay.
4. Try R_p 22k–100k (punch amount) and R_d 47k–470k (spike length).
   - Without a U3B buffer, C_p's charging current loads C16 a little at each attack. Fine for the test.

**v2 parts:**
- U3B as the ENV buffer (or the spare LM13700 Darlington B);
- the punch network;
- two or three new pots (PUNCH, ATTACK DECAY, SUSTAIN), probably replacing SENS's role, with SENS staying as a trimmer.
- This fits the "Penfold Dynamics" v2 direction above.
