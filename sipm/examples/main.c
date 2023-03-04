#include <stdlib.h>     //exit()
#include <signal.h>     //signal()
#include <time.h>
#include "ADS1263.h"
#include "stdio.h"
#include <string.h>

// ADC1 test part
#define TEST_ADC1		0		
// ADC1 rate test par
#define TEST_ADC1_RATE	1		
	

#define REF			5.08		//Modify according to actual voltage
								//external AVDD and AVSS(Default), or internal 2.5V

void  Handler(int signo)
{
    //System Exit
    printf("\r\n END \r\n");
    DEV_Module_Exit();
    exit(0);
}

int main(void)
{
    UDOUBLE ADC[10];
	UWORD i;
	double RES, TEMP;
	
    // Exception handling:ctrl + c
    signal(SIGINT, Handler);
	
    printf("ADS1263 Demo \r\n");
    DEV_Module_Init();

	ADS1263_SetMode(0);
	if(ADS1263_init_ADC1(ADS1263_38400SPS) == 1) {
		printf("\r\n END \r\n");
		DEV_Module_Exit();
		exit(0);
	}
	
	if(TEST_ADC1) {
		printf("TEST_ADC1\r\n");
		while(1) {
			ADS1263_GetAll(ADC);	// Get ADC1 value
			for(i=0; i<10; i++) {
				if((ADC[i]>>31) == 1)
					printf("IN%d is -%lf \r\n", i, REF*2 - ADC[i]/2147483648.0 * REF);		//7fffffff + 1
				else
					printf("IN%d is %lf \r\n", i, ADC[i]/2147483647.0 * REF);		//7fffffff
			}
			printf("\33[10A");//Move the cursor up
		}
	}
	else if(TEST_ADC1_RATE) {
		printf("TEST_ADC1_RATE\r\n");
		struct timespec start={0, 0}, finish={0, 0}; 
		clock_gettime(CLOCK_REALTIME, &start);
		double time;
		UBYTE isSingleChannel = 1;
		if(isSingleChannel) {
			for(i=0; i<10000; i++) {
				ADS1263_GetChannalValue(0);
			}
			clock_gettime(CLOCK_REALTIME, &finish);
			time =  (double)(finish.tv_sec-start.tv_sec)*1000.0 + (double)(finish.tv_nsec-start.tv_nsec)/1000000.0;
			printf("%lf ms\r\n", time);
			printf("single channel %lf kHz\r\n", 10000 / time);

		}
		else {
			for(i=0; i<1000; i++) {
				ADS1263_GetAll(ADC);
			}
			clock_gettime(CLOCK_REALTIME, &finish);
			time =  (double)(finish.tv_sec-start.tv_sec)*1000.0 + (double)(finish.tv_nsec-start.tv_nsec)/1000000.0;
			printf("%lf ms\r\n", time);
			printf("multi channel %lf kHz\r\n", 10000 / time);
		}

	}

	return 0;
}
