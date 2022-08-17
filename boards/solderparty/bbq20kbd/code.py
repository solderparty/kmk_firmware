import board

from kb import BBQ20KBD

from kmk.keys import KC
from kmk.modules.layers import Layers
from kmk.modules.modtap import ModTap
from kmk.scanners import DiodeOrientation
from kmk.modules.bbq20trackpad import BBQ20TrackPad
from kmk.modules.mouse_keys import MouseKeys

import pwmio

backlight = pwmio.PWMOut(board.BACKLIGHT, frequency=1000, duty_cycle=0)
backlight.duty_cycle = int(0.5 * 65535)

keyboard = BBQ20KBD()
#keyboard.debug_enabled = True

trackpad = BBQ20TrackPad(board.TP_MOTION, board.TP_RESET, board.TP_SHUTDOWN, keyboard.i2c)
keyboard.modules.append(trackpad)

keyboard.modules.append(MouseKeys())

keyboard.keymap = [
    [
         KC.MB_LMB, #0
         KC.W, #1
         KC.G, #2
         KC.S, #3
         KC.L, #4
         KC.H, #5
         KC.NO, #6
         KC.Q, #7
         KC.R, #8
         KC.E, #9
         KC.O, #10
         KC.U, #11
         KC.NO, #12
         KC.NO, #13
         KC.F, #14
         KC.LSHIFT, #15
         KC.K, #16
         KC.J, #17
         KC.NO, #18
         KC.SPACE, #19
         KC.C, #20
         KC.Z, #21
         KC.M, #22
         KC.N, #23
         KC.NO, #24
         KC.NO, #25
         KC.T, #26
         KC.D, #27
         KC.I, #28
         KC.Y, #29
         KC.NO, #30
         KC.NO, #31
         KC.V, #32
         KC.X, #33
         KC.DLR, #34
         KC.B, #35
         KC.NO, #36
         KC.A, #37
         KC.RSHIFT, #38
         KC.P, #39
         KC.BSPC, #40
         KC.ENTER, #41
     ],
]

if __name__ == '__main__':
    keyboard.go()
