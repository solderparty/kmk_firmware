import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.scanners import DiodeOrientation


class BBQ20KBD(_KMKKeyboard):
    row_pins = (
        board.ROW1,
        board.ROW2,
        board.ROW3,
        board.ROW4,
        board.ROW5,
        board.ROW6,
        board.ROW7,
    )
    col_pins = (
        board.COL1,
        board.COL2,
        board.COL3,
        board.COL4,
        board.COL5,
        board.COL6,
    )
    diode_orientation = DiodeOrientation.ROWS
    i2c = board.I2C()
