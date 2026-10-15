# Enclosure: Hammond/Tayda 1590B

Generated 2026-10-14 from the KiCad board (v1.0). The board is the Ugly Face 1 outline with the same pot and LED positions, so the face holes match UF1 v1.0 (four pots, no toggle).

- **`Penfold_1590B_drill.csv`:** face holes for the Tayda Box Tool.
- **`Penfold_1590B_drill_template.svg`:** a 1:1 printable template (outside view, labelled, with a 50 × 5 mm check box).
- **`Penfold_1590B_mill_marks.svg`:** for engraving hole marks on the Othermill.

## Face (side A), outside view

| Hole | X | Y | Ø mm | Part |
|---|---|---|---|---|
| VOLUME (top left) | −14.29 | 36.22 | 7.5 | RV5 Alpha 16 mm A100k |
| DRIVE (top right) | 14.29 | 36.22 | 7.5 | RV2 Alpha 16 mm A100k |
| LED | 0 | 20.34 | 3.2 | 3 mm LED, no bezel (~5–6 mm with a bezel) |
| DECAY (bottom left) | −14.29 | 10.82 | 7.5 | RV4 Alpha 16 mm B250k |
| FILTER (bottom right) | 14.29 | 10.82 | 7.5 | RV3 Alpha 16 mm B100k |
| Footswitch | 0 | −37.5 | 12.2 | 3PDT (same position as the Trem 1590B) |

- **Origin and units:** the origin is the face centre; mm, **+X right, +Y up**, viewed from outside. The top is the jack end.
- **Board-to-face mapping** (the same as UF1): the box centre is at board (148.35, 113.75). The pots and LED face the panel, so the outside view is mirrored: **X = 148.35 − x_board**.
  - Pot shafts are 16 mm above the pot pins: **Y = 113.75 − (y_pins − 16)**.
  - LED: **Y = 113.75 − y_LED**.
  - Checked against UF1 v1.2's CSV (VOL / FRQ / ENV / LED match exactly).
- **Not included:** the jacks and DC jack (side walls; mark them by hand after a test fit) and the SENS trimmer (RV1 3362P, internal).
- **Hole sizes** are for raw aluminium. For powder-coated boxes, add Tayda's allowance (users report +0.2 to +0.4 mm).

## Mill marking file (Bantam Tools Othermill)

**`Penfold_1590B_mill_marks.svg`:**
- **Page:** 60 × 112 mm = the 1590B face (portrait), outside view, **top edge = the jack end**.
- **Contents:** one circle per hole at its finished diameter, plus a 1 mm circle at each centre. Stroke only: no text, no outline.
- **Alignment:**
  - Page placement: the lower-left page corner = the lower-left face corner.
  - Geometry placement: the marks' bounding box starts **11.96 mm from the left edge and 12.40 mm from the bottom edge** (it spans x 11.96–48.04, y 12.40–95.97).
  - The layout is symmetric left/right (LED and footswitch on the centre line). **Zeroing on the face centre** (X 30, Y 56 from the lower-left) is the most reliable. The walls have draft, so measure your box.
- The 1590B is ~31 mm tall: check it fits under the spindle with the engraving bit.
