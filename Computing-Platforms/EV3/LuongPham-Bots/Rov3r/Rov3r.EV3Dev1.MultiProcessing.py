#!/usr/bin/env python3


from ev3dev.ev3 import (
    Motor, LargeMotor, MediumMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C,
    TouchSensor, ColorSensor, InfraredSensor, RemoteControl, INPUT_1, INPUT_3, INPUT_4,
    Sound, Screen
)

from PIL import Image
from multiprocessing import Process

import os
import sys
sys.path.append(os.path.expanduser('~'))
from util.drive_util_ev3dev1 import IRBeaconRemoteControlledTank


class Rov3r(IRBeaconRemoteControlledTank):
    def __init__(
            self,
            left_motor_port: str = OUTPUT_B, right_motor_port: str = OUTPUT_C,
            gear_motor_port: str = OUTPUT_A,
            touch_sensor_port: str = INPUT_1, color_sensor_port: str = INPUT_3,
            ir_sensor_port: str = INPUT_4, ir_beacon_channel: int = 1):
        super().__init__(
            left_motor_port=left_motor_port, right_motor_port=right_motor_port,
            ir_sensor_port=ir_sensor_port, ir_beacon_channel=ir_beacon_channel)

        self.gear_motor = MediumMotor(address=gear_motor_port)

        self.touch_sensor = TouchSensor(address=touch_sensor_port)
        self.color_sensor = ColorSensor(address=color_sensor_port)

        self.ir_sensor = InfraredSensor(address=ir_sensor_port)
        self.beacon = RemoteControl(sensor=self.ir_sensor,
                                    channel=ir_beacon_channel)

        self.speaker = Sound()
        self.dis = Screen()


    def spin_gears(self, speed: float = 1000):
        while True:
            if self.beacon.beacon:
                self.gear_motor.run_forever(speed_sp=speed)

            else:
                self.gear_motor.stop(stop_action=Motor.STOP_ACTION_HOLD)


    def change_screen_when_touched(self):
        while True:
            if self.touch_sensor.is_pressed:
                self.dis.image.paste(im=Image.open('/home/robot/image/Angry.bmp'))
                self.dis.update()

            else:
                self.dis.image.paste(im=Image.open('/home/robot/image/Fire.bmp'))
                self.dis.update()


    def make_noise_when_seeing_black(self):
        while True:
            if self.color_sensor.color == ColorSensor.COLOR_BLACK:
                self.speaker.play(wav_file='/home/robot/sound/Ouch.wav').wait()


    def main(self):
        self.speaker.play(wav_file='/home/robot/sound/Yes.wav').wait()

        Process(target=self.make_noise_when_seeing_black,
                daemon=True).start()

        Process(target=self.spin_gears,
                daemon=True).start()

        Process(target=self.change_screen_when_touched,
                daemon=True).start()

        self.keep_driving_by_ir_beacon()



if __name__ == '__main__':
    ROV3R = Rov3r()

    ROV3R.main()
