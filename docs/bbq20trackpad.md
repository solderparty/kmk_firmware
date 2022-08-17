# BlackBerry Q20 keyboard track pad

This module handles the usage of a track pad that's on the BlackBerry Q20 keyboard.


### Usage

Declare the I2C bus and add this module in your main class, with pin info.

```python
from kmk.modules.bbq20trackpad import BBQ20TrackPad
import busio as io

i2c = io.I2C(scl=board.D3, sda=board.D2)
motion_pin = board.D4
reset_pin = board.D5
shutdown_pin = board.D6
trackpad = BBQ20TrackPad(motion_pin, reset_pin, shutdown_pin, i2c)
keyboard.modules.append(trackpad)
```

Module will also work when you cannot use `busio` and do `import bitbangio as io` instead.
