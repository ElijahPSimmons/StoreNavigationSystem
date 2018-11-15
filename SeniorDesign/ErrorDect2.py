#!/usr/bin/env python

# Written by Limor "Ladyada" Fried for Adafruit Industries, (c) 2015
# This code is released into the public domain
import numpy as np
import time
import os
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
DEBUG = 1

pot_adjust = [[0,0,0,0,0,0],
                [0,0,0,0,0,0],
                [0,0,0,0,0,0],
                [0,0,0,0,0,0],
                [0,0,0,0,0,0]]

trim_pot = 	[[0,0,0,0,0,0],
                [0,0,0,0,0,0],
                [0,0,0,0,0,0],
                [0,0,0,0,0,0],
                [0,0,0,0,0,0]]

ogwait = [0,0,0,0,0,0]				
# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
        if ((adcnum > 7) or (adcnum < 0)):
                return -1
        GPIO.output(cspin, True)

        GPIO.output(clockpin, False)  # start clock low
        GPIO.output(cspin, False)     # bring CS low

        commandout = adcnum
        commandout |= 0x18  # start bit + single-ended bit
        commandout <<= 3    # we only need to send 5 bits here
        for i in range(5):
                if (commandout & 0x80):
                        GPIO.output(mosipin, True)
                else:
                        GPIO.output(mosipin, False)
                commandout <<= 1
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)

        adcout = 0
        # read in one empty bit, one null bit and 10 ADC bits
        for i in range(12):
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)
                adcout <<= 1
                if (GPIO.input(misopin)):
                        adcout |= 0x1

        GPIO.output(cspin, True)

        adcout >>= 1       # first bit is 'null' so drop it
        return adcout



def runFSR():
        # change these as desired - they're the pins connected from the
        # SPI port on the ADC to the Cobbler
        SPICLK = 18
        SPIMISO = 23
        SPIMOSI = 24
        SPICS = [5,6,13,19,26,25]
		 
		
        GPIO.setwarnings(False)
        # set up the SPI interface pins
        GPIO.setup(SPIMOSI, GPIO.OUT)
        GPIO.setup(SPIMISO, GPIO.IN)
        GPIO.setup(SPICLK, GPIO.OUT)
        GPIO.setup(SPICS, GPIO.OUT)

        # 10k trim pot connected to adc #0
        potentiometer_adc = 0;

        #trim_pot = [0,0,0,0,0,0]
        last_read = [0,0,0,0,0,0]      # this keeps track of the last potentiometer value
        incorrect_weight = [0,0,0,0,0,0]
        tolerance = 5       # to keep from being jittery we'll only change
                            # volume when the pot has moved more than 5 'counts'
        i = 0
        j = 0

        t_end = time.time() + 15
        while(time.time() < t_end):
            cs = SPICS[i]
         # read the analog pin
            global trim_pot
	    trim_pot[i][j] = readadc(potentiometer_adc, SPICLK, SPIMOSI, SPIMISO, cs)
         # how much has it changed since the last read?
            global pot_adjust
            pot_adjust[i][j] = (trim_pot[i][j]- last_read[i])
            print trim_pot
            print j
            tolerance = pot_adjust[i][j]*.1

     # Store last value
            last_read[i] = trim_pot[i][j]

     # Increment i to move through SPI
            if j < 5:
                j += 1
            else:
                j = 0
                if(i < 4):
                    i += 1
                else:
                    i = 0


     # hang out and do nothing for a half second
            time.sleep(0.5)
        return pot_adjust

def  misplace():
	waitwrong = [0,0,0,0,0,0]		#
        col = [0,0,0,0,0]						#array to store a single fsr's weight readings
	ad = 0
		
        i = 0                            #location of item
        j = 0                            #iteration of reading of the one item
	runFSR()

        while(i < 6):					#code checks if weight as changed from the original set weight 
            while(j < 5):
                global trim_pot
                col[j] = trim_pot[j][i]
                ad = sum(col)
                j += 1
        
            tolerance = ogwait[i] * .1
            pot_change = abs(ogwait[i] - (ad/5))
            
            if(pot_change > tolerance):
                waitwrong[i] = 1
            else:
                waitwrong[i] = 0
            i += 1
            j = 0
        print waitwrong
        return waitwrong
misplace()




