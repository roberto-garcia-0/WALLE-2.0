# tentative file to put sipm driver code here
# Adapted from https://github.com/waveshare/High-Pricision_AD_HAT/tree/master/python
#!/usr/bin/python
# -*- coding:utf-8 -*-

# import time
import datetime
import ADS1263
# import RPi.GPIO as GPIO

REF = 5.00          # Modify according to actual voltage
                    # external AVDD and AVSS(Default), or internal 2.5V
                    #VDD max = 7V
                    #VSS min = -3V
                    #max diff betwewen VDD and VSS = 7V, Min diff = -0.3V

# ADC1 test part
TEST_ADC1       = True
# ADC2 test part
# TEST_ADC2       = False
# ADC1 rate test part, For faster speeds use the C program
TEST_ADC1_RATE   = False
# RTD test part 
# TEST_RTD        = False     

#save time date
#read data from port 0 and 4 to text doc
#save time data
#record data to new time doc

# data format: 
#yr/m/D:time:   port 0 Data  port 4 Data

ADC = ADS1263.ADS1263()
# The faster the rate, the worse the stability
# and the need to choose a suitable digital filter(REG_MODE1)
# digital filter is set in ADS1263_ConfigADC, using sinc1 right now
if (ADC.ADS1263_init_ADC1('ADS1263_38400SPS') == -1): #should return 0 if everthinng is working
    exit()
ADC.ADS1263_SetMode(0) # 0 is singleChannel, 1 is diffChannel

#main loop
channelList = [0, 4]


#funtion [channel List, time limit of file, ]
try:
    # start_time = datetime.UTC
    print(datetime.UTC)
    while(1):
        ADC_Value = ADC.ADS1263_GetAll(channelList)    #get ADC1 value

        for i in channelList:

            if(ADC_Value[i]>>31 ==1):
                data = (REF*2 - ADC_Value[i] * REF / 0x80000000)
                # print("ADC1 IN%d = -%lf" %(i, (REF*2 - ADC_Value[i] * REF / 0x80000000)))  #over_flow
            else:
                data = (ADC_Value[i] * REF / 0x7fffffff)
                # print("ADC1 IN%d = %lf" %(i, (ADC_Value[i] * REF / 0x7fffffff)))   # 32bit
            
            print(data)

        # for i in channelList:
        #     print("\33[2A") #clear the screen



except IOError as e:
    print(e)

except KeyboardInterrupt:
    print("ctrl + c:")
    print("Program end")
    ADC.ADS1263_Exit()
    exit()












# try:
#     ADC = ADS1263.ADS1263()
    
#     # The faster the rate, the worse the stability
#     # and the need to choose a suitable digital filter(REG_MODE1)
#     if (ADC.ADS1263_init_ADC1('ADS1263_400SPS') == -1):
#         exit()
#     ADC.ADS1263_SetMode(0) # 0 is singleChannel, 1 is diffChannel

#     # ADC.ADS1263_DAC_Test(1, 1)      # Open IN6
#     # ADC.ADS1263_DAC_Test(0, 1)      # Open IN7
    
#     if(TEST_ADC1):       # ADC1 Test
#         channelList = [0, 1, 2, 3, 4]  # The channel must be less than 10
#         while(1):
#             ADC_Value = ADC.ADS1263_GetAll(channelList)    # get ADC1 value
#             for i in channelList:
#                 if(ADC_Value[i]>>31 ==1):
#                     print("ADC1 IN%d = -%lf" %(i, (REF*2 - ADC_Value[i] * REF / 0x80000000)))  
#                 else:
#                     print("ADC1 IN%d = %lf" %(i, (ADC_Value[i] * REF / 0x7fffffff)))   # 32bit
#             for i in channelList:
#                 print("\33[2A")
        
#     #elif(TEST_ADC2):
#     #    if (ADC.ADS1263_init_ADC2('ADS1263_ADC2_400SPS') == -1):
#     #        exit()
#     #    while(1):
#     #        ADC_Value = ADC.ADS1263_GetAll_ADC2()   # get ADC2 value
#     #        for i in range(0, 10):
#     #            if(ADC_Value[i]>>23 ==1):
#     #                print("ADC2 IN%d = -%lf"%(i, (REF*2 - ADC_Value[i] * REF / 0x800000)))
#     #            else:
#     #                print("ADC2 IN%d = %lf"%(i, (ADC_Value[i] * REF / 0x7fffff)))     # 24bit
#     #        print("\33[11A")

#     elif(TEST_ADC1_RATE):    # rate test
#         time_start = time.time()
#         ADC_Value = []
#         isSingleChannel = True
#         if isSingleChannel:
#             while(1):
#                 ADC_Value.append(ADC.ADS1263_GetChannalValue(0))
#                 if len(ADC_Value) == 5000:
#                     time_end = time.time()
#                     print(time_start, time_end)
#                     print(time_end - time_start)
#                     print('frequency = ', 5000 / (time_end - time_start))
#                     break
#         else:
#             while(1):
#                 ADC_Value.append(ADC.ADS1263_GetChannalValue(0))
#                 if len(ADC_Value) == 5000:
#                     time_end = time.time()
#                     print(time_start, time_end)
#                     print(time_end - time_start)
#                     print('frequency = ', 5000 / (time_end - time_start))
#                     break

#     elif(TEST_RTD):     # RTD Test
#         while(1):
#             ADC_Value = ADC.ADS1263_RTD_Test()
#             RES = ADC_Value / 2147483647.0 * 2.0 *2000.0       #2000.0 -- 2000R, 2.0 -- 2*i
#             print("RES is %lf"%RES)
#             TEMP = (RES/100.0 - 1.0) / 0.00385      #0.00385 -- pt100
#             print("TEMP is %lf"%TEMP)
#             print("\33[3A")
        
#     ADC.ADS1263_Exit()

# except IOError as e:
#     print(e)
   
# except KeyboardInterrupt:
#     print("ctrl + c:")
#     print("Program end")
#     ADC.ADS1263_Exit()
#     exit()
   
