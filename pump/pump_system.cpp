// Notes: Entire system runs at 1.3A. The flow rate of the system is about 165mL/min.
// To have 2.25L of water processed, about 13.6 min is required. To have all the filters
// used, a total of 40.9 min is needed. The system requires about 0.886 Ah of total charge.
// At least 1Ah is recommended.
#include <iostream>
// for delay function.
#include <chrono>
#include <string>
#include <thread>
#include <cstdio>

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

static int user_input_filter = 0;
static bool end_this_program = false;
static volatile int pulse_count = 0;
static volatile bool pump = 0;

// USEFULL FUNCTIONS

inline void delayMs(int ms) { this_thread::sleep_for(chrono::milliseconds(ms)); }

void signalHandler(int s) { end_this_program = true; }

// INTERRUPT FUNCTIONS

// Toggles the pump. Outputs the measured amount of water when between on/off toggles.
// Count is reset when
void pumpToggle(const std::string& channel)
{
    
    pump = !pump; // toggle state
    if (pump) {
        puts("PUMP ON");
        pulse_count = 0;
        GPIO::output(user_input_filter, GPIO::HIGH);
        GPIO::output(pump_pin, GPIO::HIGH);
    } else {
        puts("PUMP OFF!");
        GPIO::output(user_input_filter, GPIO::LOW);
        GPIO::output(pump_pin, GPIO::LOW);
        cout << pulse_count*0.223 << " mL" << endl;
    }
        
}

// ~4.467 pulses/mL -> 0.223 mL/pulse
void flowHandler(const std::string& channel)
{
    pulse_count++;
}

// get an input for activating the filter to collect from
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

    } while (!end_this_program);

}

int main()
{
    // When CTRL+C pressed, signalHandler will be called
    signal(SIGINT, signalHandler);

    // Pin Setup.
    GPIO::setmode(GPIO::BOARD);

    // set pin as an output pin with optional initial state of HIGH
    GPIO::setup(pump_pin, GPIO::OUT, GPIO::LOW);
    GPIO::setup(but_pin, GPIO::IN);
    GPIO::setup(flow_pin, GPIO::IN);
    GPIO::setup(filter_1_pin, GPIO::OUT, GPIO::LOW);
    GPIO::setup(filter_2_pin, GPIO::OUT, GPIO::LOW);
    GPIO::setup(filter_3_pin, GPIO::OUT, GPIO::LOW);

    cout << "Starting demo now! Press CTRL+C to exit" << endl;

    // detect events and trigger function
    // GPIO::add_event_detect(but_pin, GPIO::Edge::RISING, pumpToggle, 20);
    GPIO::add_event_detect(flow_pin, GPIO::Edge::RISING, flowHandler, 0);
    try {
        while (!end_this_program)
        {

            user_input_filter = getInputFilter(); // get input from user until it's valid or program ends
            GPIO::add_event_detect(but_pin, GPIO::Edge::RISING, pumpToggle, 200);
            puts("Push button to start!");
            while (pump == 0) {};
            puts("Push button to end!");
            while (pump == 1) {};
            GPIO::remove_event_detect(but_pin);
        }
    } catch (exception& exc) {
        cout << exc.what() << endl;
    }
    GPIO::cleanup();

    return 0;
}
