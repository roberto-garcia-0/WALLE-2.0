import RPi.GPIO as GPIO
import time

class pump_system:
    def __init__(self):
        # VARIABLES (DO NOT CHANGE UNLESS NECESSARY)
        self.input_filter = 0                    # Tracks which filter to activate
        self.pulse_count = 0                     # Used to calculate how much water was collected
        self.water_sampled = 0                   # Stores how much water was sampled in the last toggle
        self.pump = False                        # Stores state of the pump
        self.mLPerPulse = 0.223                  # Stores mL per pulse, can be changed here
        
        # PIN DEFINITIONS (Can be redefined here)
        self.pump_pin = 12
        self.but_pin = 18
        self.flow_pin = 16
        self.filter_1_pin = 11
        self.filter_2_pin = 13
        self.filter_3_pin = 15
        
        self.setUp()

    # INTERRUPT HANDLERS

    # toggles pump and specific filter (valve solenoid)
    def toggleCollection(self, channel=None):
        
        self.pump = ~self.pump
        if (self.pump):
            # print("PUMP ON!")
            self.pulse_count = 0
            GPIO.output(self.pump_pin, GPIO.HIGH)
            GPIO.output(self.input_filter, GPIO.HIGH)
        else:
            GPIO.output(self.pump_pin, GPIO.LOW)
            time.sleep(1)
            GPIO.output(self.input_filter, GPIO.LOW)
            # print("PUMP OFF!")
            self.water_sampled = self.pulse_count*self.mLPerPulse

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

    # Checks if 2.2 L or more has been sampled.
    def enoughCollected(self):
        return self.water_sampled >= 2200

    # Used to properly select which filter (1,2,3), otherwise sets to zero
    def setInputFilter(self, input_u):
        if (input_u == 1):
            self.input_filter = self.filter_1_pin
        elif (input_u == 2):
            self.input_filter = self.filter_2_pin
        elif(input_u == 3):
            self.input_filter = self.filter_3_pin
        else:
            self.input_filter = 0

    # DEMO METHODS

    # Used for demo
    def getInputFilter(self):
        while(1):
            input_u = input("Enter filter number to activate! (1, 2, 3)\n")
            if (input_u == 1):
                self.input_filter = self.filter_1_pin
                return
            elif (input_u == 2):
                self.input_filter = self.filter_2_pin
                return
            elif(input_u == 3):
                self.input_filter = self.filter_3_pin
                return

    # Used for demo, requires button, no way out except ctrl+c
    def demo(self):
        print("Starting demo now! Press CTRL+C to exit/stop")
        try:
            while (1):
                self.getInputFilter() # get input from user until it's valid
                self.toggleCollection()
                print("Starting collection! Press CTRL+C to stop")
                try:
                    time.sleep(10)
                except KeyboardInterrupt:
                    pass
                self.toggleCollection()
                print("Water Sampled: " + str(self.water_sampled) + " mL")
        except KeyboardInterrupt:
            self.clean()
            exit(0)

    def clean(err=None):
        GPIO.cleanup()





