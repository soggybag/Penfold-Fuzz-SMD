# Penfold Fuzz SMD v1.0: archived revision

- **Git tag:** `v1.0` (commit `317331e`, 2026-10-06)
- **Tag note:** v1.0: ordered from JLCPCB (October 2026 batch)
- **Archived:** 2026-10-06 with `_tools/archive_version.py`

## Finding a part

1. Open `Penfold_Fuzz_ibom.html` in a browser. Type a reference (R14) or a value (100k) in the filter box; the part lights up on the board.
   - Hover over a pad to see its net.
   - F / B switch sides.
2. Find the same reference in `Penfold_Fuzz_schematic.pdf` with Cmd-F.
3. `Penfold_Fuzz_board_front.pdf` / `_back.pdf` are printable: page 1 has the outlines and references, page 2 the copper. The back is mirrored, as you see it holding the board.

## Files

- `Penfold_Fuzz_board_back.pdf`
- `Penfold_Fuzz_board_front.pdf`
- `Penfold_Fuzz_ibom.html`
- `Penfold_Fuzz_render_bottom.png`
- `Penfold_Fuzz_render_top.png`
- `Penfold_Fuzz_schematic.pdf`
- `docs`/
- `parts.csv`
- `production`/

`production/` holds the files sent to JLCPCB for this revision: Penfold_Fuzz.zip, bom.csv, designators.csv, netlist.ipc, positions.csv.
