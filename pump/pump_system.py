import RPi.GPIO as GPIO
import time

class pump_system:
    def __init__(self):
        # VARIABLES (DO NOT CHANGE UNLESS NECESSARY)
        self.input_filter = 1                    # Tracks which filter to activate
        self.pulse_count = 0                     # Used to calculate how much water was collected
        self.water_sampled = 0                   # Stores how much water was sampled in the last toggle
        self.pump = False                        # Stores state of the pump
        self.mLPerPulse = 0.223                  # Stores mL per pulse, can be changed here
        
        # PIN DEFINITIONS (Can be redefined here)
        self.pump_pin = 12
        self.flow_pin = 16
        self.filter_1_pin = 11
        self.filter_2_pin = 13
        self.filter_3_pin = 15
        
        self.setUp() # Call function to setup pins

    # INTERRUPT HANDLERS

    # toggles pump and specific valve solenoid to select filter
    def toggleCollection(self, channel=None):
        
        self.pump = ~self.pump
        if (self.pump):
            # PUMP ON
            self.pulse_count = 0
            GPIO.output(self.pump_pin, GPIO.HIGH)
            GPIO.output(self.input_filter, GPIO.HIGH)
        else:
            # PUMP OFF
            GPIO.output(self.pump_pin, GPIO.LOW)
            time.sleep(2)
            GPIO.output(self.input_filter, GPIO.LOW)
            self.water_sampled = self.pulse_count*self.mLPerPulse

    # Counts number of pulses
    def flowHandler(self, channel):
        self.pulse_count += 1

    # METHODS

    # Sets up all of the GPIO pins required for the pump system
    def setUp(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.flow_pin, GPIO.IN)
        GPIO.setup(self.pump_pin, GPIO.OUT)
        GPIO.setup(self.filter_1_pin, GPIO.OUT)
        GPIO.setup(self.filter_2_pin, GPIO.OUT)
        GPIO.setup(self.filter_3_pin, GPIO.OUT)
        GPIO.add_event_detect(self.flow_pin, GPIO.RISING, callback=self.flowHandler, bouncetime=0)

# Triggers collection of 2L sample
    def collectSample(self, filter):
        print("Starting Collection of 2L!")
        total_sampled = 0 # in mL
        duration = 0      # in seconds
        self.setInputFilter(filter)
        while (total_sampled < 2100):
            self.toggleCollection()
            time.sleep(8)
            self.toggleCollection()
            total_sampled += self.water_sampled
            print("Total Sampled: " + str(total_sampled) + "mL")
            duration += 1

    # Use to properly select filter, otherwise sets to one
    def setInputFilter(self, input_u):
        if (input_u == 1):
            self.input_filter = self.filter_1_pin
        elif (input_u == 2):
            self.input_filter = self.filter_2_pin
        elif(input_u == 3):
            self.input_filter = self.filter_3_pin
        else:
            self.input_filter = self.filter_1_pin

    # Call to cleanup, mainly for testing
    def clean(err=None):
        GPIO.output(self.pump_pin, GPIO.LOW)
        GPIO.output(self.input_filter, GPIO.LOW)
        GPIO.cleanup()

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








