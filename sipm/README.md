SiPM driver code adabpted from waveshare: 
Website:https://www.waveshare.com/wiki/High-Precision_AD_HAT
Github:https://github.com/waveshare/High-Pricision_AD_HAT
ADC chip datasheet:https://www.ti.com/product/ADS1263#tech-docs

For details on pinout layout, Hardware configuration, and Communication protocol reda this documennt: https://www.waveshare.com/wiki/High-Precision_AD_HAT

Read "Configure Interface" section in the website above for details, below will be annabrivated version to configure the Jetson nano.

https://github.com/waveshare/High-Pricision_AD_HAT/blob/master/python/readme_jetson_EN.txt
The above page is copied below for convenience.

1. Basic information:
This routine is based on the jetson nano development, the kernel version:
	Linux raspberrypi 5.4.51-v7l+ #1333 SMP Mon Aug 10 16:51:40 BST 2020 armv7l GNU/Linux
You can view the detailed test routine in the project's main.py

2. Pin connection:
Pin connections can be viewed in config.py, which is repeated here:
	EPD    =>    Jetson Nano/RPI(BCM)
	VCC    ->    Without direct connection, other devices can be directly connected to 3.3V
	GND    ->    GND
	DIN    ->    10(MOSI)
	DOUT   ->    9(MISO)
	SCLK   ->    11(SCLK)
	CS     ->    22
	DRDY   ->    17
	REST   ->    18
	AVDD   ->    5V or 2.5V
	AVSS   ->    GND or -2.5V

3.Installation library
    sudo apt-get update
    sudo apt-get install python-pip
    sudo apt-get install python-pil
    sudo apt-get install python-numpy
    sudo pip2 install Jetson.GPIO
	sudo pip2 install spidev

or

    sudo apt-get update
    sudo apt-get install python3-pip
    sudo apt-get install python3-pil
    sudo apt-get install python3-numpy
    sudo pip3 install Jetson.GPIO
	sudo pip3 install spidev

4.Open SPI：
In terminal input：
	sudo /opt/nvidia/jetson-io/jetson-io.py
The GPIO Tools menu will pop up, select "Configure 40-Pin Expansion Header" and press Enter to enter the secondary menu.
Then tick SPI1 and return to the higher menu, and finally select "Save and Reboot to Reconfigure Pins" to make the device reboot configuration take effect.

5. Basic use:
The factory hardware default COM has been connected to GND
The program has configured IN0 and IN1 two analog output
At this time you can draw IN0 or IN1 and GND to measure the target voltage
Input:
	sudo python sipm.py
or
	sudo python3 sipm.py
  
  
**Plese Note**: you might need to run `sudo modprobe spidev` in the terminal every time you restart the Jetson because spidev module has issues being located on the Jetson. This solution was found online and appears to be a very common issue on Jetson if you need more infomation about it.

Please run in python3, older versions of python might not work with the above sudo command.


