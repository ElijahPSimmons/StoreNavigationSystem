#!/usr/bin/python2.7

def searchNameList(listOfItems):
	itemName = raw_input('What item are you looking for? ')
	location = -1
	i=0
	for item in listOfItems:
		if(itemName.lower() in (listOfItems[i].name).lower()):#Find how to check inside of a string for the itemName
			location = i
		i+=1
	return location
	#take the color and the item location from the listOfItems and set the LED's on with the color (WNTBD)

def searchListDel(listOfItems,delete):
	location = -1
	i=0
	for item in listOfItems:
		if(delete.lower() in (listOfItems[i].name).lower()):#Find how to check inside of a string for the itemName
			location = i
		i+=1
	return location
	
def searchLocationList(listOfItems,aisle,row,col):
	i = 0
	for item in listOfItems:
		if(listOfItems[i].locAisle == aisle):
			if(listOfItems[i].locCol == col):
				if(listOfItems[i].locRow == row):
					return i
				else:
					i+=1
			else:
				i+=1
		else:
			i+=1
	return -1