#!/usr/bin/python2.7
import strandtest
import argparse
import time

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
	args = parser.parse_args()
	try:
		while True:
			#Top
			strandtest.setColors([0,100,0],0,20,18)
			time.sleep(1)
			strandtest.setColors([100,0,0],20,20,18)
			time.sleep(1)
			strandtest.setColors([0,0,100],40,20,18)
			time.sleep(1)
			strandtest.setColors([0,100,0],59,20,18)
			time.sleep(1)
			#Bottom
			strandtest.setColors([0,100,0],82,20,18)
			time.sleep(1)
			strandtest.setColors([100,0,0],102,20,18)
			time.sleep(1)
			strandtest.setColors([0,0,100],122,20,18)
			time.sleep(1)
			#strandtest.setColors([0,100,0],30,20,12)
			#time.sleep(1)
			strandtest.setColors([0,100,0],141,20,18)
			time.sleep(1)
	except KeyboardInterrupt:
		if args.clear:
			colorWipe(strip, Color(0,0,0), 10)
			
			
main()