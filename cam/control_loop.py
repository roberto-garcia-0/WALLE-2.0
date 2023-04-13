import subprocess
import signal
import time
import RPi.GPIO as GPIO

from pump/pump_system import pump_system

# 1st Button Switch Crude Power On/Power Off
# 2nd Button Toggle Camera Preview and Start Recording
# This should require double rising edge detects
# 3rd Graceful emergency shutoff
# Should interrupt recording process while preserving current recording

class smalle():
    def __init__(self):
    
        # CONFIGURATION VARIABLES
        self.video_duration = 12
        self.pump_timestamps = [3,6,9]
        self.use_pump_sys = True
        self.use_sipm_sys = True

        # SYSTEM VARIABLES
        self.filters_sampled = 0


        # PIN DEFINITION
        self.cam_preview_toggle = 32
        self.graceful_shutoff_toggle = 33

        self.setUp()

    # Sets up all of the GPIO pins required for the cam system
    def setUp(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.cam_preview_toggle, GPIO.IN)
        GPIO.setup(self.graceful_shutoff_toggle, GPIO.IN)
        GPIO.add_event_detect(self.graceful_shutoff_toggle, GPIO.RISING, callback=self.gracefulShutoff, bouncetime=0)

    def lightbeacon(self):
        ## TODO

    def gracefulShutoff(self):
        ## TODO
        exit(0)

    def run(self):

        # Preview - Use switch to exit and proceed to next state
        preview_proc = subprocess.Popen(["./cams_preview.sh"])
        GPIO.wait_for_edge(self.cam_preview_toggle, GPIO.RISING)
        GPIO.wait_for_edge(self.cam_preview_toggle, GPIO.RISING)
        preview_proc.send_signal(signal.SIGINT)

        subprocess.run(["xset", "-display", ":0.0", "dpms", "force", "off"])
        ## TODO: Subprocess to disable desktop environment

        camera_proc = subprocess.Popen(["./cams_recording.sh"])
        sipm_proc = subprocess.Popen([]) ## TODO: create callable SiPM python script
        
        sleep(60*60*pump_timestamps[1])
        ## TODO: Pump system calls and sleeps

        camera_proc.wait()
        if sipm_proc.poll() is None:
            sipm_proc.terminate()

        self.lightbeacon()
        GPIO.cleanup()


# driver code
if __name__ == '__main__':
    s = smalle()
    s.run()