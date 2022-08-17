import time
import digitalio

from kmk.kmktime import PeriodicTimer
from kmk.modules import Module
from kmk.modules.mouse_keys import PointingDevice


I2C_ADDRESS = 0x3B

REG_PID = 0x00
REG_REV = 0x01
REG_MOTION = 0x02
REG_DELTA_X = 0x03
REG_DELTA_Y = 0x04
REG_DELTA_XY_H = 0x05
REG_CONFIG = 0x11
REG_OBSERV = 0x2E
REG_MBURST = 0x42

BIT_MOTION_MOT = (1 << 7)
BIT_MOTION_OVF = (1 << 4)

BIT_CONFIG_HIRES = (1 << 7)

BIT_OBSERV_RUN = (0 << 6)
BIT_OBSERV_REST1 = (1 << 6)
BIT_OBSERV_REST2 = (2 << 6)
BIT_OBSERV_REST3 = (3 << 6)


class BBQ20TrackPad(Module):
    def __init__(self, motion, reset, shutdown, i2c, address=I2C_ADDRESS):
        self._motion = digitalio.DigitalInOut(motion)
        self._motion.switch_to_input()

        self._reset = digitalio.DigitalInOut(reset)
        self._reset.switch_to_output()

        self._shutdown = digitalio.DigitalInOut(shutdown)
        self._shutdown.switch_to_output()

        self._i2c = i2c
        self._addr = address

        self._pointing_device = PointingDevice()

        self.polling_interval = 20

    def during_bootup(self, keyboard):
        self._timer = PeriodicTimer(self.polling_interval)

        self._shutdown.value = False

        self._reset.value = False
        time.sleep(0.1)
        self._reset.value = True

    def before_matrix_scan(self, keyboard):
        if not self._timer.tick():
            return

        motion = self._read_register8(REG_MOTION)
        if motion & BIT_MOTION_MOT:
            x = self._read_register8(REG_DELTA_X)
            y = self._read_register8(REG_DELTA_Y)

            self._pointing_device.report_x[0] = 255 - x
            self._pointing_device.report_y[0] = y
            self._pointing_device.hid_pending = True

    def after_matrix_scan(self, keyboard):
        pass

    def before_hid_send(self, keyboard):
        pass

    def after_hid_send(self, keyboard):
        if self._pointing_device.hid_pending:
            keyboard._hid_helper.hid_send(self._pointing_device._evt)

            self._clear_pending_hid()

    def _clear_pending_hid(self):
        self._pointing_device.hid_pending = False
        self._pointing_device.report_x[0] = 0
        self._pointing_device.report_y[0] = 0
        self._pointing_device.report_w[0] = 0
        self._pointing_device.button_status[0] = 0

    def _read_register8(self, reg):
        while not self._i2c.try_lock():
            time.sleep(0)

        buff = bytearray(1)
        buff[0] = reg

        self._i2c.writeto(self._addr, buff)
        self._i2c.readfrom_into(self._addr, buff)

        self._i2c.unlock()

        return buff[0]
