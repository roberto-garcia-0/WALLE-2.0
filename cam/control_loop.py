import subprocess
import RPi.GPIO as GPIO

from pump_system import pump_system

class GPIO_Pins():
    cam_state = 32

    video_duration = 31
    video_duration_value = 1

# Press the external button to manually cycle through the video durations
def increment_video_duration():
    GPIO_Pins.video_duration_value = (GPIO_Pins.video_duration_value % 12) + 1

# Sets up all of the GPIO pins required for the cam system
def GPIO_setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(GPIO_Pins.cam_state, GPIO.IN)
    GPIO.setup(GPIO_Pins.video_duration, GPIO.IN)
    GPIO.add_event_detect(GPIO_Pins.video_duration, GPIO.RISING, callback = increment_video_duration, bouncetime = 0)

# driver code
if __name__ == '__main__':
# small.e Setup
    GPIO_setup()

# Preview Mode
    preview_proc = subprocess.Popen(["./cams_preview.sh"])
    GPIO.wait_for_edge(GPIO_Pins.cam_state, GPIO.RISING)
    preview_proc.terminate()
    GPIO.remove_event_detect(GPIO_Pins.video_duration)
    
# Data Collection Mode

    # Turn off display
    subprocess.run(["xset", "-display", ":0.0", "dpms", "force", "off"])

    # 
    camera_proc = subprocess.Popen(["./cams_recording.sh"])
    sipm_proc = subprocess.Popen([])
    pump_proc = subprocess.Popen([])

    camera_proc.wait()
    if sipm_proc.poll() is None:
        sipm_proc.terminate()
    if pump_proc.poll() is None:
        pump_proc.terminate()

# small.e Cleanup
    GPIO.cleanup()

    # Activate beacon
    subprocess.run()