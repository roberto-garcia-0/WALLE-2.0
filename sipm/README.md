## SiPM - ADC Hat Config and Info

SiPM driver code adopted from Waveshare:

- Website: https://www.waveshare.com/wiki/High-Precision_AD_HAT
- Github: https://github.com/waveshare/High-Pricision_AD_HAT
- ADC Chip Datasheet: https://www.ti.com/product/ADS1263#tech-docs
- Interface Config Info (under **Configure Interface**): https://www.waveshare.com/wiki/High-Precision_AD_HAT
- Full Jetson Instructions: https://github.com/waveshare/High-Pricision_AD_HAT/blob/master/python/readme_jetson_EN.txt

**This README will be a SHORT version for configuration of the Jetson Nano.**

## Basic Information

This routine is based on the raspberrypi development with kernel version:

**Linux raspberrypi 5.4.51-v7l+ #1333 SMP Mon Aug 10 16:51:40 BST 2020 armv7l GNU/Linux**

You can view the detailed test routine in the project's main.py

## Pin Connections

Pin connections can be viewed in config.py, which is repeated here:
- EPD    =>    Jetson Nano/RPI(BCM)
- VCC    ->    Without direct connection, other devices can be directly connected to 3.3V
- GND    ->    GND
- DIN    ->    10(MOSI)
- DOUT   ->    9(MISO)
- SCLK   ->    11(SCLK)
- CS     ->    22
- DRDY   ->    17
- REST   ->    18
- AVDD   ->    5V or 2.5V
- AVSS   ->    GND or -2.5V

## Installation

### 1. Install Required Packages

Copy-Paste either of the following to install required dependencies.

**Python 2**

```
sudo apt-get update
sudo apt-get install python-pip
sudo apt-get install python-pil
sudo apt-get install python-numpy
sudo pip2 install Jetson.GPIO
sudo pip2 install spidev
```

or

**Python 3**

```
sudo apt-get update
sudo apt-get install python3-dev
sudo apt-get install python3-pip
sudo apt-get install python3-pil
sudo apt-get install python3-numpy
sudo pip3 install Jetson.GPIO
sudo pip3 install spidev
``` 

### 2. Configure SPI on GPIO

1. Run this command to begin setup of SPI cabilities for the GPIO pins. 

```
sudo /opt/nvidia/jetson-io/jetson-io.py
```

2. On the GPIO Tools menu, select **Configure 40-Pin Expansion Header** and press Enter.

3. Tick SPI1 and return to the higher menu 

4. Finally select **Save and Reboot to Reconfigure Pins** to make the device reboot configuration take effect.

**Setup is complete!**

### 3. modprobe 

You might need to run `sudo modprobe spidev` in the terminal every time you restart the Jetson due to the spidev module having issues locating on the Jetson. This solution was found online and appears to be a very common issue on Jetson if you need more infomation about it.

## Basic Usage

The factory hardware default COM has been connected to GND

The program has configured IN0 and IN1 two analog output

At this time you can draw IN0 or IN1 and GND to measure the target voltage

Input:

```
sudo python sipm.py
```

or

```
sudo python3 sipm.py
```
