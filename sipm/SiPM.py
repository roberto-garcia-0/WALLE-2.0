#This file is for configering the SiPM
import ADS1263

"""Sudo code
    class SiPM:
        def init():
            
            ADC = ADS1263.ADS1263()
    
            if (ADC.ADS1263_init_ADC1('ADS1263_400SPS') == -1): exit()
            ADC.ADS1263_SetMode(0) # 0 is singleChannel, 1 is diffChannel
        
        def trigger():
            if flag is on, turn off()->set flag
            if flag is off, turn on()->set flag
        
        def record_data(time_stamp):
        #append data file(start with time stamp)
        
        def on():
        #turn sensor on
        
        def off():
        #stop recording data/ save file
        #turn sensor off
        

"""