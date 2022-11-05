
#include <iostream>
// for delay function.
#include <chrono>
#include <string>
#include <thread>
#include <cstdio>

// for signal handling
#include <JetsonGPIO.h>
#include <signal.h>


using namespace std;

// BOARD Pin Definitions
const int pump_pin = 12; 
const int but_pin = 18;   
const int flow_pin = 16;
static bool end_this_program = false;

// GLOBAL VARS


// USEFULL FUNCTIONS

inline void delayMs(int ms) { this_thread::sleep_for(chrono::milliseconds(ms)); }

void signalHandler(int s) { end_this_program = true; }

// INTERRUPT FUNCTIONS

// Toggles the pump. Outputs the measured amount of water when between on/off toggles.
// Count is reset when
void pumpToggle(const std::string& channel)
{
    // initialize variables ONCE in this instance
    static int pulse_count = 0;
    static bool pump = 0;
    
    pump = !pump; // toggle state
    if (pump) {
        puts("PUMP ON");
        pulse_count = 0;
        GPIO::output(pump_pin, GPIO::HIGH);
    } else {
        puts("PUMP OFF!");
        GPIO::output(pump_pin, GPIO::LOW);
        cout << pulse_count*0.223 << " mL" << endl;

    }
        
}

// ~4.467 pulses/mL -> 0.223 mL/pulse
void flowHandler(const std::string& channel)
{
    pulse_count++;
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

    cout << "Starting demo now! Press CTRL+C to exit" << endl;

    // detect events and trigger function
    GPIO::add_event_detect(but_pin, GPIO::Edge::RISING, pumpToggle, 20);
    GPIO::add_event_detect(flow_pin, GPIO::Edge::RISING, flowHandler, 0);

    while (!end_this_program)
    {

    }

    GPIO::cleanup();

    return 0;
}
