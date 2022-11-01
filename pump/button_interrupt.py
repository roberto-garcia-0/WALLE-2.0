#!/usr/bin/env python

# Copyright (c) 2019, NVIDIA CORPORATION. All rights reserved.
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import RPi.GPIO as GPIO
import time

# Board Pin Definitions:

pump_pin = 12
but_pin = 18
pump_on = False
time_count = 0

# toggle pump
def pumpToggle(channel):
    global pump_on
    pump_on = ~pump_on
    if (pump_on):
        print("PUMP ON!")
        GPIO.output(pump_pin, GPIO.HIGH)
    else:
        print("PUMP OFF!")
        GPIO.output(pump_pin, GPIO.LOW)



def main():
    global time_count
    # Pin Setup:
    GPIO.setmode(GPIO.BOARD)  # BOARD pin-numbering scheme
    GPIO.setup(pump_pin, GPIO.OUT)  # Pump pin set as output
    GPIO.setup(but_pin, GPIO.IN)  # button pin and flow sensor pin set as input

    # Initial state for pump:
    GPIO.output(pump_pin, GPIO.LOW)

    GPIO.add_event_detect(but_pin, GPIO.FALLING, callback=pumpToggle, bouncetime=130)
    print("Starting demo now! Press CTRL+C to exit")
    try:
        while True:
            time.sleep(1)
            time_count += 1;
            print(time_count)

    finally:
        GPIO.cleanup()  # cleanup all GPIOs

if __name__ == '__main__':
    main()
