#!/usr/bin/env python

# Written by Limor "Ladyada" Fried for Adafruit Industries, (c) 2015
# This code is released into the public domain
import numpy as np
import time
import os
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
DEBUG = 1

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

	trim_pot = [0,0,0,0,0,0]
	last_read = [0,0,0,0,0,0]      # this keeps track of the last potentiometer value
	pot_adjust = [0,0,0,0,0,0]
	incorrect_weight = [0,0,0,0,0,0]
	tolerance = 5       # to keep from being jittery we'll only change
			    # volume when the pot has moved more than 5 'counts'
	i = 0
	iteration = 0
	t_end = time.time() + 15
	while(time.time() < t_end):
		cs = SPICS[i]
		# read the analog pin
		trim_pot[i] = readadc(potentiometer_adc, SPICLK, SPIMOSI, SPIMISO, cs)
		# how much has it changed since the last read?
		pot_adjust[i] = (trim_pot[i]- last_read[i])
		print trim_pot
		print ' '
		print 'For values above %s: ' %(i)
			# Only report if weight changed more than tolerance
		tolerance = pot_adjust[i]*.1
		if(pot_adjust[i] > tolerance):
			incorrect_weight[i] +=1
			print "Misplaced Item!\n"
		else:
			print "No Misplaced Item Detected\n"
			    # Store last value
		last_read[i] = trim_pot[i]
				# Increment i to move through SPI
		if i < 5:
			i += 1
		else:
			i = 0
			iteration +=1

		# hang out and do nothing for a half second
		time.sleep(0.5)
		
	return incorrect_weight
runFSR()