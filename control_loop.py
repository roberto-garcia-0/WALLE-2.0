import subprocess
import signal
import os
import time
import RPi.GPIO as GPIO

from pump.pump_system import pump_system

# 1st Button Switch Crude Power On/Power Off
# 2nd Button Toggle Camera Preview and Start Recording
# This should require double rising edge detects
# 3rd Graceful emergency shutoff
# Should interrupt recording process while preserving current recording

class smalle():
    def __init__(self):

        # CONFIGURATION VARIABLES
        self.deployment_duration = 12
        self.pump_time_cooldowns = [3,3,3] # The time in between collections ie: for [3,3,3], pump will trigger at hours 3, 6, and 9 
        self.use_pump_sys = False
        self.use_sipm_sys = False

        # SYSTEM VARIABLES
        self.filters_sampled = 0
        self.pump = pump_system()
        self.graceful_shutoff_toggle_count = 0

        # PIN DEFINITION
        self.cam_preview_toggle = 32
        self.graceful_shutoff_toggle = 33

        self.setUp()

    # Sets up all of the GPIO pins required for the cam system
    def setUp(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.cam_preview_toggle, GPIO.IN)
        GPIO.setup(self.graceful_shutoff_toggle, GPIO.IN)
        GPIO.add_event_detect(self.graceful_shutoff_toggle, GPIO.RISING, callback=self.gracefulShutoff, bouncetime=50)

    # Trigger light beacon
    def lightbeacon(self):
        ## TODO
        return "stub"

    # signals the camera process to end while preserving the video footage
    def gracefulShutoff(self, channel):
        self.graceful_shutoff_toggle_count += 1
        if (self.graceful_shutoff_toggle_count > 1):
            self.camera_proc.send_signal(signal.SIGINT)
            exit(0)

    def run(self):

        # Preview State 
        # Intializes a camera preview
        # Use switch to exit and proceed to recording state
        preview_proc = subprocess.Popen(["./cam/cams_preview.sh"])
        GPIO.wait_for_edge(self.cam_preview_toggle, GPIO.FALLING)
        print("Waiting")
        subprocess.Popen(["./cam/kill_gstreamer.sh"])
        time.sleep(5)
        print("Done!")
        # Run commands to shutoff display and disable desktop environment to preserve battery and system resources
        # subprocess.run(["xset", "-display", ":0.0", "dpms", "force", "off"])

        # Recording State
        # Camera and SiPM recording is initialized
        self.camera_proc = subprocess.Popen(["./cam/cams_recording.sh"])
        if self.use_sipm_sys:
            sipm_proc = subprocess.Popen(["./command/to/sipm"]) ## TODO: create callable SiPM python script
        
        # Sleeps until it is time to collect DNA samples (3 in total)
        if self.use_pump_sys:
            self.pump.collectSample(1)
            # for i in range(3):
            #     sleep(60*60*self.pump_time_cooldowns[i])
            #     self.pump.collectSample(i+1)
        
        # Waits until camera process ends (after a set time in the command)
        self.camera_proc.wait()
        if self.use_sipm_sys & sipm_proc.poll() is None:
            sipm_proc.terminate()

        self.lightbeacon()
        GPIO.cleanup()


# driver code
if __name__ == '__main__':
    s = smalle()
    s.run()
