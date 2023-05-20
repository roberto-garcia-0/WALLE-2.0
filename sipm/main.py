#this file controls the light system of smalle
#it should be sutable for Jetson and RaspiPi with a few edit in the config.py file for different pin out configerations
import config
import amb_light
import SiPM


#sudo COde
##

"""Sudo Code
    while(1):
        save amb_light data to file
            save time stamp every second(configerable)
        
        if interupt:
            start/stop the SiPM
                if SiPM is started record data
                    save time stamp every second(configerable)
            


"""