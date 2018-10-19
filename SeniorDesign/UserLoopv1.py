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

#Used to create an item class
#Name of the item with the aisle number, row and column of the item's location
class Item:
	def __init__(self, inName, inLocCol, inLocRow, aisle):
		self.name = inName
		self.locCol = inLocCol
		self.locRow = inLocRow
		self.locAisle = aisle
		#self.ledSize = ledSize
		
#User class in order to keep track of users and colors for the user
class User:
	def __init__(self, inUserName, inColor):
		self.userName = inUserName
		self.color = inColor

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
		print 'Here is the item you just read \nName %s\nAisle %s\nColumn %s\nRow %s'%(listOfItems[(len(listOfItems)-1)].name,listOfItems[(len(listOfItems)-1)].locAisle,listOfItems[(len(listOfItems)-1)].locCol,listOfItems[(len(listOfItems)-1)].locRow)

	
	#While loop to make sure the code doesn't stop unless it is killed
	while(1):
		#Need to get input of what kind of user they are with authentification
		userType = raw_input('What kind of user are you? Customer or Employee? \n')
		if(userType == 'Customer' or userType == 'Employee'):
			loggedIn = 'yes'
				#While loop while the user is logged into a specific area
			while(loggedIn == 'yes'): 
				#Find what they want to do
				if(userType == 'Employee'):
					password = raw_input('Password: ')
					if(password == '123'):
						while(loggedIn == 'yes'):
							empAct = raw_input('Would you like to add new objects(1) or monitor misplaced items(2) or delete an item(3) or log out(4)? ')
							print ''
								#if they are employee and in the placement mode
							if(empAct == '1'):
								#Find out all of the information from the employee and make an item and set it in the array
								itemName = raw_input('What is the name of the item?(Full name of item) ')
								print ''	  
								 #Do we want to check the inputs to make sure or accept people's idiocracy?(WNTBD)
								aisle = raw_input('What aisle is it in?(Number location 1) ')
								print ''
								aisleCheck = 0
								#Double check that the aisle exists
								while (aisleCheck == 0):
									if((aisle == '1')):
										aisleCheck = 1
									else:
										aisle = raw_input("The desired aisle doesn't exist, try again ")
										print ''
											#Check that the column input exists
								locCol = raw_input('What column is it in?(Number location 1-3) ')
								colCheck = 0
								print ''
								while (colCheck == 0):
									if(locCol == '1' or locCol == '2' or locCol == '3'):
										colCheck = 1
									else:
										locCol = raw_input("The desired column doesn't exist, try again ")
								#Check that the row actually exists
								locRow = raw_input('What row is it in?(Number location 1-2) ')
								rowCheck = 0
								print ''
								while (rowCheck == 0):
									if(locRow == '1' or locRow == '2'):
										rowCheck = 1
									else:
										locRow = raw_input("The desired row doesn't exist, try again ")
										print ''
									#Check to make sure no other item is in the slot
								locationUsed = Search.searchLocationList(listOfItems,aisle,locRow,locCol)
								if(locationUsed == -1):
									#Add in the new item to the array
									listOfItems.append(Item(itemName,locCol,locRow,aisle))
									#Double check the item that is being added
									print 'Here is the item you just registered \nName %s\nAisle %s\nColumn %s\nRow %s'%(listOfItems[(len(listOfItems)-1)].name,listOfItems[(len(listOfItems)-1)].locAisle,listOfItems[(len(listOfItems)-1)].locCol,listOfItems[(len(listOfItems)-1)].locRow)
									UpdateDatabase.updateWrittenList(listOfItems)
								else:
									print 'Location is already being used, nothing was done.'
							if(empAct == '2'):
								#This is where we will continually look for another input while checking the other sets for anything misplaced(WNTBD)
								check = 0
							if(empAct == '3'):
								delete = raw_input('What is name of the item you would like to delete from the inventory? ')
								location = Search.searchListDel(listOfItems,delete)
								#Check to make sure that the item exists
								if(location != -1):
									#Takes out the item and allows us to see the deleted item
									item = listOfItems.pop(location)
									print '%s item has been removed.'%(item.name)
									UpdateDatabase.updateWrittenList(listOfItems)
								else:
									print "That item didn't exist in our inventory."
							if(empAct == '4'):
								loggedIn = 'no'
								print 'Logged off'
				#Find if the user is a customer		
				if(userType == 'Customer'):
					#Now we need to make a profile for them
					username = raw_input('What username would you like to use? ')
					userColor = raw_input('What color would you like to light up with ')
					user = User(username,userColor)
					while(loggedIn == 'yes'):
						userAction = raw_input('Would you like to Search(1) or log out(2)? ')
						if(userAction == '1'):
							location = Search.searchNameList(listOfItems)
							if(location != -1):
								print '%s, we found %s in the inventory.'%(user.userName,listOfItems[location].name)
							else:
								print'%s, unfortunately that item is not in our stock.'%(user.userName)
							#Send to LED strip as we have the location in the list to light up(WNTBD)
						if(userAction == '2'):
							loggedIn = 'no'
							print 'Logged off'
				else:
					print 'Your input was invalid\n'
	
			
main()
