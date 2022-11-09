
import RPi.GPIO as GPIO
import time

class pump_system:
    def __init__(self):
        self.setUp()

    # INTERRUPT HANDLERS

    # toggles pump
    def pumpToggle(self, channel=None, input_filter=None):
        
        if (input_filter == None):
            input_filter = self.input_filter
        
        self.pump = ~self.pump
        if (self.pump):
            print("PUMP ON!")
            self.pulse_count = 0
            GPIO.output(self.pump_pin, GPIO.HIGH)
            GPIO.output(input_filter, GPIO.HIGH)
        else:
            GPIO.output(self.pump_pin, GPIO.LOW)
            GPIO.output(input_filter, GPIO.LOW)
            print("PUMP OFF!")
            self.water_sampled = self.pulse_count*0.223

    # Counts number of pulses
    def flowHandler(self, channel):
        self.pulse_count += 1

    # METHODS

    # Sets up all of the GPIO pins required for the pump system
    def setUp(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.but_pin, GPIO.IN)
        GPIO.setup(self.flow_pin, GPIO.IN)
        GPIO.setup(self.pump_pin, GPIO.OUT)
        GPIO.setup(self.filter_1_pin, GPIO.OUT)
        GPIO.setup(self.filter_2_pin, GPIO.OUT)
        GPIO.setup(self.filter_3_pin, GPIO.OUT)
        GPIO.add_event_detect(self.flow_pin, GPIO.RISING, callback=self.flowHandler, bouncetime=0)

    def getInputFilter(self):
        while(1):
            input_u = input("Enter filter number to activate! (1, 2, 3)")
            if (input_u == 1):
                self.input_filter = self.filter_1_pin
                return
            elif (input_u == 2):
                self.input_filter = self.filter_2_pin
                return
            elif(input_u == 3):
                self.input_filter = self.filter_3_pin
                return

    def demo(self):
        print("Starting demo now! Press CTRL+C to exit")
        try:
            while (1):
                self.getInputFilter(); # get input from user until it's valid
                print("Push button to start!")
                GPIO.wait_for_edge(self.but_pin, GPIO.RISING)
                self.pumpToggle()
                print("Push button to end!")
                time.sleep(0.1)
                GPIO.wait_for_edge(self.but_pin, GPIO.RISING)
                self.pumpToggle()
                print("Water Sampled: " + str(self.water_sampled) + " mL")
        finally:
            GPIO.cleanup()
    
    # VARIABLES

    input_filter = 0
    pulse_count = 0
    water_sampled = 0
    pump = False

    # PIN DEFINITIONS

    pump_pin = 12
    but_pin = 18
    flow_pin = 16
    filter_1_pin = 11
    filter_2_pin = 13
    filter_3_pin = 15
# END pump_system


def main():
    p = pump_system()
    p.demo()
   

if __name__ == '__main__':
    main()
