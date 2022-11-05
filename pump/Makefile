# to compile code utilizing the JetsonGPIO C++ libraries, use this command
# g++ -o your_program_name [your_source_codes...] -lJetsonGPIO -lpthread -Wl,-rpath=/usr/local/lib

all: pump_system

pump_system: pump_system.cpp
	g++ -o pump_system pump_system.cpp -lJetsonGPIO -lpthread -Wl,-rpath=/usr/local/lib

clean:
	rm -f pump_system *.o
