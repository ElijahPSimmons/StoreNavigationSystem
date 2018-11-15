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
			strandtest.setColors([0,100,0],10,20,21)
			time.sleep(5)
			strandtest.setColors([0,100,0],30,20,21)
			time.sleep(5)
	except KeyboardInterrupt:
		if args.clear:
			colorWipe(strip, Color(0,0,0), 10)
			
			
main()