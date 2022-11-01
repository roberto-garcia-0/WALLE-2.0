# WALLE-2.0
### Waterborne Autonomous Low-Light Electrostereo Videography System and DNA Sampler Version 2

We will develop a second version of a Waterborne Autonomous Low-Light Electrostereo (WALLE) videography system that can generate  3-D models of the bioluminescent courtship signaling of ostracods. Additionally, WALLE will be capable of sampling the DNA of ostracods for the UCSB Oakley Evolution Lab.

## External Behavioral Specification
The videography system will record stereo video footage of the ostracod courtship signaling. This data will be reconstructed into 3D models of the signals. Light intensity measurements of the signals will be made with a SiPM. This data will be output into a processable text file. The footage and light intensity measurements cause the DNA collector system to pump water through DNA collecting filters. The pump system will measure the amount of water processed to ensure proper collection.

### Low-Light Electrostereo Videography System
Stereo synchronized cameras will provide stereo vision video for reconstructing 3D bioluminescence courtship signaling of ostracods. This footage will be used to recognize patterns from courtship.

### DNA Collector System
Upon a threshold of light level or when a new courtship pattern is detected, a pump will push water through a filter to collect the DNA present in the water. The lab will be able to extract the ostracod DNA from the various species present in the water.

### Light Intensity Measurement
Detects the blue light intensity from the ostracod courtship signaling and outputs it into a text file for processing. This processed data will also be used to trigger the DNA collector.

## Block Diagram 
![Diagram](https://user-images.githubusercontent.com/59896939/199332750-f5f42a2f-9a82-4969-a6a4-3770f6d8e20b.jpg)

## Team Member Responsibility 
Ebony (Leader) - Programming the SiPM sensor to detect BioLuminescent light under water. Designing waterproof case suitable for SiPM Senor.
Reiley - Implementation of low-light, stereo camera system and synchronization.
Roberto -  Designing DNA collector. Configuring the software interface of the pump system. Designing modular waterproof case for this system. 
Ryan - Implementing user interface for utilizing the entire system as well as other general responsibilities, including the data storage system.
Sammy - Implementation of low-light, stereo camera system and synchronization.
