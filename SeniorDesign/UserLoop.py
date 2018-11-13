#!/usr/bin/python2.7
#Need to get the different import files figured out
#Team A, Store Navigation System initial code 
#Creates a class Item and User in order to allow for maintaining the items and people using the device
#Allows for item location, addition and searching based on LED's
#Also allows for checking of misplaced items
#Start date: 9/27/2018
#End date:
#Author: Elijah Simmons

import ReadDatabase
import Search
import UpdateDatabase
import strandtest
import time

#Used to create an item class
#Name of the item with the aisle number, row and column of the item's location
class Item:
	def __init__(self, inName, inLocCol, inLocRow, aisle):
		self.name = inName
		self.locCol = inLocCol
		self.locRow = inLocRow
		self.locAisle = aisle
		#self.weight = itemWeight
		#self.color = inColor
		
#User class in order to keep track of users and colors for the user
class User:
	def __init__(self, inUserName, inColor):
		self.userName = inUserName
		self.color = inColor
		self.RGBW = []
		if(inColor.lower() in 'red'.lower()):
			self.RGB = [255,0,0]
		if(inColor.lower() in 'blue'.lower()):
			self.RGB = [0,0,255]
		if(inColor.lower() in 'green'.lower()):
			self.RGB = [0,255,0]
		if(inColor.lower() in 'white'.lower()):
			self.RGB = [255,255,255]
		if(inColor.lower() in 'yellow'.lower()):
			self.RGB = [255,255,0]
		if(inColor.lower() in 'purple'.lower()):
			self.RGB = [128,0,128]

	#Main function to be called to start all code
def main():
	#Make a list to hold the values of the aisle
	listOfItems = []
	arrayOfItems = []
	#Get an array of the items from the txt file
	arrayOfItems = ReadDatabase.readWrittenList()
	#iterate through that array to populate the list of items
	i = 0
	while i < len(arrayOfItems)-4:
		itemName = arrayOfItems[i]
		i+=1
		locAisle = arrayOfItems[i]
		i+=1
		locCol = arrayOfItems[i]
		i+=1
		locRow = arrayOfItems[i]
		i+=1
		listOfItems.append(Item(itemName,locCol,locRow,locAisle))
	printList(listOfItems)
	
	#While loop to make sure the code doesn't stop unless it is killed
	while(1):
		#Need to get input of what kind of user they are with authentification
		userType = raw_input('What kind of user are you? Customer or Employee? \n')
		if(userType.lower() == 'customer' or userType.lower() == 'employee'):
			loggedIn = 'yes'
				#While loop while the user is logged into a specific area
			while(loggedIn == 'yes'): 
				#Find what they want to do
				if(userType.lower() == 'employee'):
					password = raw_input('Password: ')
					if(password == '123'):
						while(loggedIn == 'yes'):
							empAct = raw_input('Would you like to add new objects(1) or monitor misplaced items(2) or delete an item(3) or print the list(4) or log out(5)? ')
							print '\n'
							#if they are employee and in the placement mode
							if(empAct == '1'):
								#Find out all of the information from the employee and make an item and set it in the array
								itemName = raw_input('What is the name of the item?(Full name of item) ')
								print '\n'  
								aisle = raw_input('What aisle is it in?(Number location 1) ')
								print '\n'
								aisleCheck = 0
								#Double check that the aisle exists
								while (aisleCheck == 0):
									if((aisle == '1')):
										aisleCheck = 1
									else:
										aisle = raw_input("The desired aisle doesn't exist, try again ")
										print '\n'
								#Check that the column input exists
								locCol = raw_input('What column is it in?(Number location 1-3) ')
								print '\n'
								colCheck = 0
								while (colCheck == 0):
									if(locCol == '1' or locCol == '2' or locCol == '3'):
										colCheck = 1
									else:
										locCol = raw_input("The desired column doesn't exist, try again ")
										print '\n'
								#Check that the row actually exists
								locRow = raw_input('What row is it in?(Number location 1-2) ')
								print '\n'
								rowCheck = 0
								while (rowCheck == 0):
									if(locRow == '1' or locRow == '2'):
										rowCheck = 1
									else:
										locRow = raw_input("The desired row doesn't exist, try again ")
										print '\n'
								#Check to make sure no other item is in the slot
								locationUsed = Search.searchLocationList(listOfItems,aisle,locRow,locCol)
								if(locationUsed == -1):
									#Add in the new item to the array
									#WNTBD find the weight of the item from the FSR code
									#WNTBD find the color differences and save what is needed
									listOfItems.append(Item(itemName,locCol,locRow,aisle))
									#Double check the item that is being added
									print 'Here is the item you just registered \nName %s\nAisle %s\nColumn %s\nRow %s\n'%(listOfItems[(len(listOfItems)-1)].name,listOfItems[(len(listOfItems)-1)].locAisle,listOfItems[(len(listOfItems)-1)].locCol,listOfItems[(len(listOfItems)-1)].locRow)
									UpdateDatabase.updateWrittenList(listOfItems)
								else:
									print 'Location is already being used, nothing was done.\n'
							if(empAct == '2'):
								#This is where we will continually look for another input while checking the other sets for anything misplaced(WNTBD)
								#WNTBD How can we take a kill input while it runs other code?
								iteration = 0
								#for item in listOfItems:
								#	misplaced = 0
									#if(listOfItems[iteration].weight != FSR check at the location)
									#	misplaced = 1
									#if(listOfItems[iteration].color != Check color sensor at location)
									#	misplaced += 1
									#
									#if(misplaced == 2):
									#	print 'There is an item misplaced in Aisle %s, Row %s, Column %s'%(listOfItems[iteration].locAisle,listOfItmes[iteration].locRow,listOfItems[iteration].locCol)
									#iteration+=1
								check = 0
							if(empAct == '3'):
								delete = raw_input('What is name of the item you would like to delete from the inventory? ')
								print '\n'
								location = Search.searchListDel(listOfItems,delete)
								#Check to make sure that the item exists
								if(location != -1):
									#Takes out the item and allows us to see the deleted item
									item = listOfItems.pop(location)
									print '%s item has been removed.\n'%(item.name)
									UpdateDatabase.updateWrittenList(listOfItems)
								else:
									print "That item didn't exist in our inventory.\n"
							if(empAct == '4'):
								printList(listOfItems)
							if(empAct == '5'):
								loggedIn = 'no'
								print 'Logged off\n\n'
				#Find if the user is a customer		
				if(userType.lower() == 'customer'):
					#Now we need to make a profile for them
					username = raw_input('What username would you like to use? ')
					print '\n'
					userColor = '0'
					colorCheck = 0
					#Go through the checking process for what color they want to use
					while (colorCheck == 0):
						userColor = raw_input('What color would you like to light up with?(red, green, blue, white, yellow, purple): ')
						print '\n'
						if(userColor.lower() == 'red' or userColor.lower() == 'green' or userColor.lower() == 'blue' or userColor.lower() == 'white' or userColor.lower() == 'yellow' or userColor.lower() == 'purple'):
							colorCheck = 1
						else:
							locRow = raw_input("The desired color doesn't exist, try again ")
							print '\n'
					#Set the username and the color
					user = User(username,userColor)
					while(loggedIn == 'yes'):
						userAction = raw_input('Would you like to Search(1) or log out(2)? ')
						print '\n'
						if(userAction == '1'):
							location = Search.searchNameList(listOfItems)
							if(location != -1):
								print '%s, we found %s in the inventory.\n'%(user.userName,listOfItems[location].name)
								print '%s can be found in Aisle %s, Row %s, and Column %s\n'%(listOfItems[location].name,listOfItems[location].locAisle,listOfItems[location].locRow,listOfItems[location].locCol)
								search = raw_input('Would you like the item location to light up? (y or n): ')
								print '\n'
								while(search == 'y'):
									#Runs the LEDs to light up for a period of time
									strandtest.setColors(user.RGB,int(float((listOfItems[location].locCol))*10),20,21)
									time.sleep(5)
									strandtest.setColors([0,0,0],0,60,21)
									#Run the LED code for dark across all of them
									search = raw_input('Would you like to light the item location up again?(y or n): ')
							else:
								print'%s, unfortunately that item is not in our stock.\n'%(user.userName)
						if(userAction == '2'):
							loggedIn = 'no'
							print 'Logged off\n\n'
				if(userType.lower() != 'customer' and userType.lower() != 'employee'):
					print 'Your input was invalid\n'
					
def printList(list):
	i = 0
	while i < len(list):
		print 'Here is the item you just read \nName %s\nAisle %s\nColumn %s\nRow %s'%(list[i].name,list[i].locAisle,list[i].locCol,list[i].locRow)
		i+=1
	
			
main()
