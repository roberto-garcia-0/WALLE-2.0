// Notes: Entire system runs at 1.3A. The flow rate of the system is about 165mL/min.
// To have 2.25L of water processed, about 13.6 min is required. To have all the filters
// used, a total of 40.9 min is needed. The system requires about 0.886 Ah of total charge.
// At least 1Ah is recommended.


#include <iostream>         // for debugging and testing
#include <chrono>           // for delay function.
#include <string>
#include <thread>

// for signal handling
#include <JetsonGPIO.h>
#include <signal.h>

// namespace

using namespace std;

// BOARD Pin Definitions

const int pump_pin = 12;
const int but_pin = 18;   
const int flow_pin = 16;
const int filter_1_pin = 11;
const int filter_2_pin = 13;
const int filter_3_pin = 15;

// GLOBAL VARS

static int user_input_filter = 0;           // Used to activate appropriate filter to sample from. Need to specify!
static volatile int pulse_count = 0;        // Number of pulses to determine amount of water sampled.
static volatile double water_sampled = 0;   // Water measured in mL.
static volatile bool pump = 0;              // State of the pump.

// FUNCTIONS

inline void delayMs(int ms) { this_thread::sleep_for(chrono::milliseconds(ms)); }

// When CTRL+C pressed, signalHandler will be called. GPIO clean up
void signalHandler(int s)
{
    puts("Exiting");
    GPIO::cleanup();
    exit(0);
}

// get an input for activating the filter to collect from, can be used in demo
int getInputFilter()
{
    static string input;
    do
    {
        puts("Enter filter number to activate! (1, 2, 3)");
        cin >> input;
        if (input == "1")
                return filter_1_pin;
        else if (input == "2")
                return filter_2_pin;
        else if (input == "3")
                return filter_3_pin;

    } while (1);

}

// INTERRUPT FUNCTIONS

// Toggles the pump. Outputs the measured amount of water when between on/off toggles.
// Count is reset when pump is activated.
// Requires user_input_filter to be set to a filter
void pumpToggle(const std::string& channel)
{
    
    pump = !pump; // toggle state
    if (pump) {
        puts("PUMP ON");
        pulse_count = 0;
        GPIO::output(user_input_filter, GPIO::HIGH);
        GPIO::output(pump_pin, GPIO::HIGH);
    } else {
        GPIO::output(user_input_filter, GPIO::LOW);
        GPIO::output(pump_pin, GPIO::LOW);
        puts("PUMP OFF!");
        water_sampled = pulse_count*0.223;
    }
        
}

// ~4.467 pulses/mL -> 0.223 mL/pulse
void flowHandler(const std::string& channel)
{
    pulse_count++;
}

int main()
{
    signal(SIGINT, signalHandler);

    // Pin Setup.
    GPIO::setmode(GPIO::BOARD);

    // set pins as inputs or outputs
    GPIO::setup(pump_pin, GPIO::OUT, GPIO::LOW);
    GPIO::setup(but_pin, GPIO::IN);
    GPIO::setup(flow_pin, GPIO::IN);
    GPIO::setup(filter_1_pin, GPIO::OUT, GPIO::LOW);
    GPIO::setup(filter_2_pin, GPIO::OUT, GPIO::LOW);
    GPIO::setup(filter_3_pin, GPIO::OUT, GPIO::LOW);

    cout << "Starting demo now! Press CTRL+C to exit" << endl;

    // detect events and trigger function
    GPIO::add_event_detect(flow_pin, GPIO::Edge::RISING, flowHandler, 0);

    while (1)
    {
        user_input_filter = getInputFilter(); // get input from user until it's valid
        GPIO::add_event_detect(but_pin, GPIO::Edge::RISING, pumpToggle, 200);
        puts("Push button to start!");
        while (pump == 0) {};
        puts("Push button to end!");
        while (pump == 1) {};
        GPIO::remove_event_detect(but_pin);
        cout << water_sampled << " mL" << endl;
    }


    return 0;
}
