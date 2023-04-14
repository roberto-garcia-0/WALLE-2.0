
<p float="left">
  <img src=https://user-images.githubusercontent.com/59896939/231983585-c8b760ad-28db-4382-8136-c9313adf8950.png width="300" />
  <img src="https://user-images.githubusercontent.com/59896939/231979197-8c97de6d-7fe1-4d55-a3d7-8840e243fdc7.png" width="400" /> 
</p>

### Stereovideographic & Macromolecular Acquisition of Low-Light Emitters

The UCSB Oakley Evolution Lab seeks to investigate the evolutionary history of bioluminescence courtship signaling of small crustaceans called ostracods. Such emissions occur after nightfall when there is no moonlight and are characterized as pulses that vary in temporal and spatial patterns between species. We are creating a camera and DNA collection system named Stereovideographic & Macromolecular Acquisition of Low-Light Emitters (small-e), for deployment at the bottom of the Caribbean Sea. Small-e will capture stereo-vision video that will be stereo-rectified to create 4D models of the courtship patterns. We are aiming to have small-e be compact and to support new features compared to previous camera systems, such as time-precise light intensity measurements, time correspondent eDNA collection, and a 12-hour runtime. 

# External Behavioral Specification
The videography system will record stereo video footage of the ostracod courtship signaling. This data will be reconstructed into 3D models of the signals. Light intensity measurements of the signals will be made with a SiPM. This data will be output into a processable text file. The footage and light intensity measurements cause the DNA collector system to pump water through DNA collecting filters. The pump system will measure the amount of water processed to ensure proper collection.

## Low-Light Electrostereo Videography System
Stereo synchronized cameras will provide stereo vision video for reconstructing 3D bioluminescence courtship signaling of ostracods over time. This footage will be used to recognize patterns from courtship.

## DNA Collector System
At set timer intervals, a pump will push water through a filter to collect the DNA present in the water. 3 filters will be used to sample a total of 6L over the course of 12 hourss. The lab will be able to extract the ostracod DNA from the various species present in the water at different times corresponding to the video footage.

## Light Intensity Measurement
Detects the blue light intensity from the ostracod courtship signaling and outputs it into a file. Will help characterize the temporal patterns of the pulses among ostracod species. 

# Block Diagram 

![small-e Block Diagram](https://user-images.githubusercontent.com/59896939/231986084-3c14e02d-4b69-470a-8d1c-ec4c69f3b8d4.png)

# Team Member Responsibility 
- Ebony (Leader) - Programming the SiPM sensor to detect BioLuminescent light under water. Designing waterproof case suitable for SiPM Sensor.
- Reiley - Implementation of low-light, stereo camera system and synchronization.
- Roberto -  Designing DNA collector. Configuring the software interface of the pump system. Designing modular waterproof case for this system. 
- Ryan - Implementing user interface for utilizing the entire system as well as other general responsibilities, including the data storage system.
- Sammy - Implementation of low-light, stereo camera system and synchronization and SiPM.

