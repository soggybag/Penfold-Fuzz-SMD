# Penfold Fuzz SMD v1.0: test procedure

Board: `Penfold_Fuzz` **v1.0** (git tag `v1.0`; `archive/v1.0/` has the schematic PDF and the interactive BOM). TL072 ×2 + LM13700, on the Ugly Face 1 frame (1590B, 16 mm pots).
General method: `../../_tools/BENCH_TESTING.md`. First build of this board.

## How it works

A Rat-style fuzz whose output goes through a VCA (LM13700). The VCA's gain follows an **envelope taken from the clean input**: the fuzz is loud when you play hard and fades as the note decays. **With no playing, the output is silent.** That's normal.

| Block | Parts | What it does |
|---|---|---|
| Bias | R1/R2 100k + C5 47µ → **VREF ≈ 4.4 V** (U3B is a parked follower) | |
| Input | C6 100n, R4 1M pull-down, R5 1M to VREF → **IN_B** (feeds both the fuzz and the envelope) | |
| **Rat stage** U1A | R6 1k + C7 1n; **RV2 DRIVE A100k** ∥ C8 100p; legs R7 47 + C9 2.2µ, R8 560 + C10 4.7µ | Very high gain (Rat) |
| Clip + filter | C11 4.7µ → R9 1k → D3/D4 to GND; R10 1k5 → **RV3 FILTER B100k** + C12 3.3n | Rat clipping and filter (~32 kHz → ~480 Hz) |
| Buffer U3A | C13 100n, R11 1M to VREF | SIG |
| **VCA** U2 (LM13700, OTA A) | SIG → R12 15k → + input (R18 470 to OTA_BIAS); − via R19 470; OTA_BIAS = R16/R17 3k9 + C17 22µ ≈ 4.4 V; R20 100k output load; Darlington buffer → R21 4k7 | Gain ∝ Iabc |
| **Envelope** U1B | + = IN_B; **RV1 SENS** (3362P 500k trimmer) feedback, leg R13 2k2 + C14 4.7µ (×1 → ×228) | Amplifies the clean guitar |
| Detector | C15 4.7µ → **D5 BAT54S** (doubler) → ENV: C16 4.7µ hold; **RV4 DECAY B250k** + R14 4k7 discharge; **R15 220k → Iabc (pin 1)** | Envelope → OTA current |
| Output | C18 10µ → **RV5 VOLUME A100k** → OUT | |
| LED | R3 2k → D2 → LED_K | ~3.4 mA |

## 0. Before power

| # | Check | Expected | Measured |
|---|---|---|---|
| 0.1 | Visual: U1/U3 pin 1, **U2 LM13700 pin 1** (SOIC-16), D1 band, D3/D4, **D5 BAT54S orientation**, C5 polarity | as silkscreen | ✅ |
| 0.2 | Ohms J1 → GND | tens of kΩ (lower than the other boards: the OTA bias divider is 7.8k) | 27.8K |

## 1. First power (100 Ω; knobs at noon; SENS trimmer mid; no input)

| # | Check | Expected | Measured |
|---|---|---|---|
| 1.1 | LED off | **~7.5 mA** (two TL072 ~5 + OTA bias divider 1.1 + LM13700 buffer ~0.7 + chip) | 0.84V -> 8.4mA |
| 1.2 | LED on | +~3.4 mA | 1.12V -> 10.2mA |

## 2. DC voltages (no input)

| # | Node | Where | Expected | Measured |
|---|---|---|---|---|
| 2.1 | VREF | C5 + | 4.4 V | 4.34V |
| 2.2 | U1 pin 1 (DIST) | | ≈ VREF (DC gain 1) | 4.37V |
| 2.3 | U1 pin 7 (envelope amp) | | ≈ VREF | 4.37V |
| 2.4 | U3 pin 1 (SIG) | | ≈ VREF | 4.37V |
| 2.5 | OTA_BIAS | U2 pins 13/14 | ≈ 4.4 V | 4.38V |
| 2.6 | **ENV** (C16 +) | | **0 V** at rest | 0V |
| 2.7 | U2 pin 1 (Iabc) | | **0 V at rest**; ~1.2 V only while Iabc flows (see notes) | 0V |
| 2.8 | U2 pin 5 (OTA out) | | ≈ OTA_BIAS | 4.33V |
| 2.9 | U2 pin 8 (buffer out) | | ≈ OTA_BIAS − ~1.3 V ≈ 3.1 V (Darlington) | 3.15V |

**Sections 0–2 notes (2026-10-14):**
- **0.2** 27.8 kΩ ✓ (lower, as expected, because of the 7.8k OTA bias divider).
- **Supply current:** 8.4 mA LED off (estimate 7.5 ✓). The LED adds **1.8 mA** (estimate 3.4). The difference is the LED's forward voltage: a white/blue or high-Vf LED drops ~3 V+ instead of ~2 V, so R3 2k passes less. Fine if the brightness suits you.
- **DC: all good.** VREF 4.34 V; DIST / envelope amp / SIG 4.37 V; OTA_BIAS 4.38 V; ENV 0 V; OTA out 4.33 V; buffer out 3.15 V ✓.
- **2.7 Iabc = 0 V is correct at rest; my "~1.2 V" expectation was wrong.** Pin 1 is the input of the LM13700's current mirror. It only sits two diode drops (~1.2 V) above GND when current flows. With ENV = 0 V, no current flows through R15, so the pin sits at ~0 V.
  - **For section 3:** while playing, pin 1 should rise to ~1.2 V and stay there, while ENV climbs higher.
  - **Consequence:** the VCA only starts to open once ENV passes ~1.2 V (the mirror's turn-on). Iabc = (ENV − 1.2 V) / 220k. So soft playing may not open it at all. SENS sets how hard you have to play. Watch for this "dead zone" in the guitar tests.

## 3. Signal (generator 200 Hz, 100 mVpp; scope)

| # | Point / setting | Expected | Seen |
|---|---|---|---|
| 3.1 | U1 pin 1 (DIST), DRIVE up | heavy clipping | Has good fuzz clipping |
| 3.2 | D3/D4 node | squared at about ±0.6 V around 0 V | |
| 3.3 | U3 pin 1 (SIG), FILTER ends | bright ↔ dark | Filter seems to have no or very little effect on the sound.  |
| 3.4 | U1 pin 7 (envelope amp), SENS trimmer | the clean sine, ×1 → ×228 (it clips at high settings: fine) | the trimmer is working. I will play with the settings and have more feedback in the future.  |
| 3.5 | **ENV** (C16 +), with the sine on | a DC level of a few V, set by SENS. Turn the sine off: it decays over ~20 ms (DECAY min) to ~1 s (max) | |
| 3.6 | OUT, sine on | the fuzz, level set by ENV | |
| 3.7 | OUT, sine off | fades to **silence** with the DECAY time | |

**Set SENS (RV1):** with a guitar played normally, turn SENS up until a picked note opens the VCA fully and the decay sounds natural. Too high: always open (just a fuzz). Too low: only hard picking gets through.

## 4. Guitar

| # | Check | Seen |
|---|---|---|
| 4.1 | Dynamics: soft playing quiet, hard playing loud, notes swell/decay | This is working. Low strings dominate and activate the envelope. High strings Don’t open the envelope when sensitivity is set just at the edge of envelope. |
| 4.2 | DECAY range (short chop ↔ long sustain) | Short chop is not very short, maybe 1 to 2 seconds. long decay is 3 to 4 seconds. Can we change the envelope to something closer to an ADSR? It would be more playable if we can adjust the attack decay, the sustain level would be lower but use the guitars natural decay. The idea would be to control the initial attack. Often heavily compressed distortion and fuzz effects get lost in the mix due to the lack of this initial attack and decay, this is what makes the notes of a clean guitar stand out. |
| 4.3 | Envelope ripple: a "buzz" on low notes at short DECAY? (ideas in `Penfold Roadmap.md`) | There is some “ripple” as notes decay. |
| 4.4 | Knob directions all increase clockwise | yes |

**Sections 3–4 notes (2026-10-14):**
- **3.3 FILTER has almost no effect: a design error (mine).**
  - The Rat filter is 1k5 + FILTER pot in **series**, with 3.3n to GND, and the output taken **at the capacitor** (≈475 Hz – 32 kHz).
  - On this board, C13 (to the U3A buffer) taps the **R10 / pot junction** (/FILT) instead of the **pot / C12 junction**. The pot ends up in the shunt arm, so the darkest setting is only ~19 kHz.
  - **Bench fix:** lift C13's /FILT end and wire it to C12 pin 1 (= RV3 pins 2/3). FILTER should then go from bright to dark, darker clockwise.
  - **v1.1:** move the C13 connection in the schematic.
- **4.1 Low strings open the envelope, high strings don't:** the low strings put out more level. The detector also has a ~1.2 V threshold (the Iabc mirror), so quieter strings fall below it. Fix: **pre-emphasis in the envelope amp**. Make C14 smaller (4.7µ → ~220n puts the gain leg's corner at ~330 Hz), so the low notes get less envelope gain than the high ones.
- **4.2 DECAY range 1–2 s / 3–4 s instead of 20 ms – 0.55 s:**
  - The envelope amp clips at the SENS setting needed to open the VCA. While the note rings, the detector sees a full-size square, so ENV stays pinned high.
  - The DECAY time only starts when the note falls below the clip point, so what you hear is mostly the guitar's own sustain, flattened.
  - Lower SENS, or the pre-emphasis above, lets ENV follow the note's level instead.
- **4.3 Ripple on decaying notes:** expected with the single-cap doubler (Roadmap Idea 2).
- **4.2 question: an ADSR-like "attack spike → lower sustain → natural fade":** see `Penfold Roadmap.md` → *Transient shaper*. A bench experiment is described there.
- Not yet filled: 3.2, 3.5–3.7.

## 5. After boxing

- Supply current (1.1).

## Record

| Item | Result |
|---|---|
| Unit number | |
| Date | |
| SENS trimmer setting | |
| Notes | |
