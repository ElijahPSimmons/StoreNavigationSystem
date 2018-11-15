#!/usr/bin/python2.7

#Read in the list of items so that you don't have to add a new item everytime									
def readWrittenList():									
	#open the file to work on
	file = open('database.txt', 'r')
	#This takes the line of the text document and separates it into the substrings with the delimiter of a space
	lines = file.read().split(',')
	place = 0
	iteration = 0
	ret = []
	for item in lines:
		#Need to get rid of \n in case the document has wrapping text
		if(iteration == 0):
			#Can be simplified by just appending the array this code was for the listOfItems originally(WNTBD)
			item = item.replace('\n','')
			ret.append(item)	
			iteration = iteration + 1
		#Read in the aisle and place it at the location 				
		elif(iteration == 1):
			ret.append(item)
			iteration = iteration + 1
			
		elif(iteration == 2):
			ret.append(item)
			iteration = iteration + 1								
			
		elif(iteration == 3):
			ret.append(item)
			iteration = 0
			place = place + 1
		file.close()
	return ret