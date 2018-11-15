#!/usr/bin/python2.7
#Senior Design project Team A
#Store Navigation System GUI with code to run different instances of the program
#Author: Elijah Simmons
#Written from: 10/29/18-
#Creates a window using tkinter in python that allows for a customer or employee to login
#Each kind of user has a different list of options
#	The customer has the option to search the list to find the location of the item
#		then if they would like, they have the option to light up the location of the item
#	The employee has the options of adding items to the shelves, removing items, printing the list 
#		or checking for misplaced items
from Tkinter import *
import ReadDatabase
import Search
import UpdateDatabase
import ColorSensorTest
import time
import strandtest
import pixy
from ctypes import *
from pixy import *

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
	def __init__(self, inUserName):
		self.userName = inUserName
		self.RGBW = []


class Window(Frame):
	#initializes the window and starts the initial setup
	def __init__(self,master=None):
		Frame.__init__(self,master)
		self.master = master
		
		self.init_window()
	#Creates the Customer Employee window choices
	def init_window(self):
		#Change the title
		self.master.title('GUI for Store Naviagtion System')
		
		#allow the widget to take full space of the window
		self.pack(fill=BOTH,expand=1)
		
		self.text = Label(self,text="What kind of user are you?",font=("Times",32))
		self.text.grid(row=0,column=3)
		self.text.pack()
		#self.text.place(relx = .35,rely=.2)
		
		#Create the Customer button
		self.customerButton = Button(self, text='Customer',font=("Times",18),command=self.clientCustomer,height=2,width=10)
		self.customerButton.place(relx = .175,rely = .4)
		
		#Create the Employee button
		self.empButton = Button(self,text='Employee',font=("Times",18),command=lambda type=1: self.clientEmployee(type),height=2,width=10)
		self.empButton.place(relx = .55,rely=.4)
		
	def clientCustomer(self):		
		#destroy what was there previously
		self.customerButton.destroy()
		self.text.destroy()
		self.empButton.destroy()
		
		#Create the options and interface
		self.text = Label(self,text="What is your name?",font=("Times",14))
		self.text.place(relx=0,rely=.45)
		self.username = Entry(self)
		self.username.place(relx=.35,rely=0.45)
		#Send to clientAccept if the accept button is pressed
		self.acceptButton = Button(self,text='Enter',font=("Times",14),command=self.clientAccept,height=2,width=10)
		self.acceptButton.place(relx=.725,rely=.4)
		
	def clientAccept(self):
		#Set the username for the user
		user.userName = self.username.get()
		self.text.destroy()
		self.username.destroy()
		self.acceptButton.destroy()
		
		#Send to client Color after destroying the previous widgets
		self.clientColor()
	
	def clientColor(self):
		self.text = Label(self,text='What color would you like to light LEDs with?',font=("Times",18))
		self.text.grid(row=0,column=3)
		self.text.pack()
		
		#Create the different options of colors for the LEDs and send the to set the color for the user
		self.blueButton = Button(self,text='Blue',font=("Times",18),command=lambda color = 'blue': self.setColor(color),height=2,width=8)
		self.blueButton.place(relx=0.05,rely=.2)
		self.redButton=Button(self,text='Red',font=("Times",18),command=lambda color = 'red': self.setColor(color),height=2,width=8)
		self.redButton.place(relx=.4,rely=.2)
		self.purpleButton=Button(self,text='Purple',font=("Times",18),command=lambda color ='purple': self.setColor(color),height=2,width=8)
		self.purpleButton.place(relx=.725,rely=.2)
		self.whiteButton=Button(self,text='White',font=("Times",18),command=lambda color ='white': self.setColor(color),height=2,width=8)
		self.whiteButton.place(relx=.725,rely=.65)
		self.yellowButton=Button(self,text='Yellow',font=("Times",18),command=lambda color ='yellow': self.setColor(color),height=2,width=8)
		self.yellowButton.place(relx=.4,rely=.65)
		self.greenButton=Button(self,text='Green',font=("Times",18),command=lambda color ='green': self.setColor(color),height=2,width=8)
		self.greenButton.place(relx=0.05,rely=.65)
		
	def setColor(self,color):
		#Sets the color for the global user
		if(color in 'red'.lower()):
			user.RGBW = [255,0,0,0]
		if(color in 'green'.lower()):
			user.RGBW = [0,255,0,0]
		if(color in 'blue'.lower()):
			user.RGBW = [0,0,255,0]
		if(color in 'white'.lower()):
			user.RGBW = [255,255,255]
		if(color in 'yellow'.lower()):
			user.RGBW = [255,255,0,0]
		if(color in 'purple'.lower()):
			user.RGBW = [255,0,255,0]
		#Send to the initial search window
		self.clientInitSearch(1)
		
	def clientInitSearch(self,type):
		#Need to know what the previous client was so that we can destroy the widgets properly
		if(type==1):
			self.text.destroy()
			self.blueButton.destroy()
			self.redButton.destroy()
			self.purpleButton.destroy()
			self.whiteButton.destroy()
			self.yellowButton.destroy()
			self.greenButton.destroy()
		elif(type == 0):
			self.text.destroy()
			self.lightLEDs.destroy()
			self.searchAgain.destroy()
		elif(type==2):
			self.text = Label(self,text='No item was found by that name')
			self.text.place(relx=0,rely=0)
			time.sleep(3)
			self.text.destroy()
		
		#Cutsomer has simple options of logging off or searching which sends it to the respective field
		self.logOffButton = Button(self,text='Log Off',font=("Times",14),command=self.customerLogOff,height=2,width=8)
		self.logOffButton.place(relx=.75,rely=.75)
		
		self.searchButton = Button(self,text='Search',font=("Times",14),command=self.clientSearch,height=2,width=8)
		self.searchButton.place(relx=.65,rely=.4)
		
		self.searchEntry = Entry(self)
		self.searchEntry.place(relx=.25,rely=0.45)
		
	def clientSearch(self):
		#Client search is to check the location of the item and see if it is in the list of items 
		search = self.searchEntry.get()
		if(search == ''):
			search = 'asdf'
		self.logOffButton.destroy()
		self.searchButton.destroy()
		self.searchEntry.destroy()
		#Search database and make a place where they can light up the item
		location = Search.searchNameList(listOfItems,search)
		#if the item is not found follow this line 
		if(location == -1):
			#Sends them back to the previous client to try again
			self.clientInitSearch(2)
		else:
			#If the item is found, we need to give an option of lighting LEDs or searching again
			self.text = Label(self,text='%s can be found in Aisle %s, Row %s, and Column %s\n'%(listOfItems[location].name,listOfItems[location].locAisle,listOfItems[location].locRow,listOfItems[location].locCol),font=("Times",14))
			self.text.grid()
			self.text.pack()
			#self.text.place(relx=.25,rely=0)
			self.lightLEDs = Button(self,text='Light LEDs',font=("Times",16),command=lambda loc = location: self.litLEDs(loc),height=2,width=10)
			self.lightLEDs.place(relx=.15,rely=.35)
			self.searchAgain = Button(self,text='Search again',font=("Times",16),command=lambda ty=0: self.clientInitSearch(ty),height=2,width=10)
			self.searchAgain.place(relx=.6,rely=.35)
		
							   
	def litLEDs(self,loc):
		#Sets the correct pin assignment based on the aisle and row of the item to light up the proper section
		pinLoc = 0
		if(listOfItems[loc].locAisle == '1' and listOfItems[loc].locRow == '1'):
			pinLoc = 21
		elif(listOfItems[loc].locAisle == '1' and listOfItems[loc].locRow == '2'):
			pinLoc = 20
		elif(listOfItems[loc].locAisle == '2' and listOfItems[loc].locRow == '1'):
			pinLoc = 16
		elif(listOfItems[loc].locAisle == '2' and listOfItems[loc].locRow == '2'):
			pinLoc = 15
		strandtest.setColors(user.RGBW,int(float((listOfItems[loc].locCol))*10),20,pinLoc)
		time.sleep(5)
		strandtest.setColors([0,0,0],0,60,pinLoc)
		
	def customerLogOff(self):
		self.logOffButton.destroy()
		self.searchButton.destroy()
		self.searchEntry.destroy()
		
		#Send you back to the original selection of which kind of user
		self.init_window()
	
	def clientEmployee(self,ty):
		#destroy what was there previously based on previous client
		global used
		if(ty==1):
			self.customerButton.destroy()
			self.text.destroy()
			self.empButton.destroy()
		elif(ty==2):
			#Add a label to let the user know what has happened
			#self.textLabel.destroy()
			if(used==1):
				self.printLabel.destroy()
				updateUsed(0)
			self.returnButton.destroy()
			self.enterButton.destroy()
			self.itemName.destroy()
			self.itemNameEntry.destroy()
			self.itemAisle.destroy()
			self.itemAisleEntry.destroy()
			self.itemRow.destroy()
			self.itemRowEntry.destroy()
			self.itemColumn.destroy()
			self.itemColumnEntry.destroy()
		elif(ty==3):
			#Add a label to let the user know what has happened
			if(used==1):
				self.printLabel.destroy()	
				updateUsed(0)
			self.returnButton.destroy()
			self.enterButton.destroy()
			self.itemName.destroy()
			self.itemNameEntry.destroy()
			self.itemAisle.destroy()
			self.itemAisleEntry.destroy()
			self.itemRow.destroy()
			self.itemRowEntry.destroy()
			self.itemColumn.destroy()
			self.itemColumnEntry.destroy()
		elif(ty==4):
			#Add a label to let the user know what has happened
			if(used==1):
				self.printLabel.destroy()
				updateUsed(0)
			self.returnButton.destroy()
			self.text.destroy()
			self.removeButton.destroy()
			self.removeEntry.destroy()
		elif(ty==5):
			#Add a label to let the user know what has happened
			if(used==1):
				self.printLabel.destroy()
				updateUsed(0)
			self.returnButton.destroy()
			self.text.destroy()
			self.removeButton.destroy()
			self.removeEntry.destroy()
		elif(ty==6):
			self.listbox.destroy()
			self.scrollbar.destroy()
			self.returnButton.destroy()
			self.checkButton.destroy()
			
		self.text = Label(self,text='What would you like to do?',font=("Times",24))
		#self.text.place(relx=.3,rely=.2)
		self.text.pack()
		
		self.addItemButton = Button(self,text='Add an item',font=("Times",12),command=self.clientAddItem,height=2,width=12)
		self.addItemButton.place(relx=.15,rely=.3)
		self.removeItemButton = Button(self,text='Remove an item',font=("Times",12),command=self.clientRemoveItem,height=2,width=12)
		self.removeItemButton.place(relx =.55,rely=.3)
		self.printListButton = Button(self,text='Print list',font=("Times",12),command=self.clientPrintList,height=2,width=12)
		self.printListButton.place(relx=.15,rely=.55)
		self.checkMisplacedButton = Button(self,text='Misplaced mode',font=("Times",12),command=self.clientCheckItems,height=2,width=12)
		self.checkMisplacedButton.place(relx=.55,rely=.55)
		self.logOffButton = Button(self,text='Log Off',font=("Times",12),command=self.employeeLogOff,height=2,width=12)
		self.logOffButton.place(relx=.75,rely=.8)
		
	def clientAddItem(self):
		self.addItemButton.destroy()
		self.removeItemButton.destroy()
		self.printListButton.destroy()
		self.checkMisplacedButton.destroy()
		self.logOffButton.destroy()
		self.text.destroy()
		
		#Get the information of what the item is and its location to store then double check it in addItem
		self.itemName = Label(self,text='Item Name',font=("Times",12))
		self.itemName.place(relx=0,rely=0)
		self.itemNameEntry = Entry(self)
		self.itemNameEntry.place(relx=0.3,rely=0)
									  
		self.itemAisle = Label(self,text='Aisle #',font=("Times",12))
		self.itemAisle.place(relx=0,rely=.2)
		self.itemAisleEntry = Entry(self)
		self.itemAisleEntry.place(relx=.3,rely=.2)
									  
		self.itemRow = Label(self,text='Row #',font=("Times",12))
		self.itemRow.place(relx=0,rely=0.4)
		self.itemRowEntry = Entry(self)
		self.itemRowEntry.place(relx=.3,rely=.4)
									  
		self.itemColumn = Label(self,text='Column #',font=("Times",12))
		self.itemColumn.place(relx=0,rely=0.6)
		self.itemColumnEntry = Entry(self)
		self.itemColumnEntry.place(relx=.3,rely=.6)
									  
		self.enterButton = Button(self,text='Enter all',font=("Times",12),command=self.addItem)
		self.enterButton.place(relx=.7,rely=.7)
		
		self.returnButton = Button(self,text='Return',font=("Times",12),command=lambda ty = 2: self.clientEmployee(ty),height=2,width=5)
		self.returnButton.place(relx=.825,rely=.825)
									  
		
	def addItem(self):
		#Double check that the location isn't used already
		updateUsed(1)
		item = Item(self.itemNameEntry.get(),self.itemColumnEntry.get(),self.itemRowEntry.get(),self.itemAisleEntry.get())
		locationUsed = Search.searchLocationList(listOfItems,item.locCol,item.locRow,item.locAisle)
		#If the item location is open and it is within the boundaries, put the item in the list and update the database
		if(item.name == '' or item.locAisle =='' or item.locRow=='' or item.locCol==''):
			self.clientPrintStatus(3,'Item did not get added')
		elif(locationUsed == -1 and (item.name != '' or (int(item.locAisle)) <= 2 and int(item.locAisle)>0) or (int(item.locRow) <= 2 and int(item.locRow)>0) or (int(item.locCol) <= 3 and int(item.locCol>0))):
			listOfItems.append(item)
			UpdateDatabase.updateWrittenList(listOfItems)
			self.clientPrintStatus(2,'Item %s has been added to the list'%item.name)
		else:
			self.clientPrintStatus(3,'Item did not get added')
		
	def clientRemoveItem(self):
		self.addItemButton.destroy()
		self.removeItemButton.destroy()
		self.printListButton.destroy()
		self.checkMisplacedButton.destroy()
		self.logOffButton.destroy()
		self.text.destroy()
									  
		self.text = Label(self,text='What is the name of the item you would like to remove?',font=("Times",16))
		self.text.pack()
		#self.text.place(relx=.1,rely=.3)
									  
		self.removeButton = Button(self,text='Remove',font=("Times",12),command=self.removeItem,height=2,width=10)
		self.removeButton.place(relx=.65,rely=.4)
		
		self.removeEntry = Entry(self)
		self.removeEntry.place(relx=.25,rely=0.45)
		
		self.returnButton = Button(self,text='Return',font=("Times",12),command=lambda ty = 4: self.clientEmployee(ty),height=2,width=5)
		self.returnButton.place(relx=.825,rely=.825)
									  
	def removeItem(self):
		delete = self.removeEntry.get()
		updateUsed(1)
		if(delete == ''):
			delete = 'asdf'
		location = Search.searchListDel(listOfItems,delete)
		#Check to make sure that the item exists
		if(location != -1):
			#Takes out the item and allows us to see the deleted item
			item = listOfItems.pop(location)
			UpdateDatabase.updateWrittenList(listOfItems)
			self.clientPrintStatus(4,'The item %s was removed'%(item.name))
			used = 1
		else:
			self.clientPrintStatus(5,'No item existed with that name')
			used = 1
									  
	def clientPrintList(self):
		self.addItemButton.destroy()
		self.removeItemButton.destroy()
		self.printListButton.destroy()
		self.checkMisplacedButton.destroy()
		self.logOffButton.destroy()
		self.text.destroy()
		
		i = 0
		printArray = []
		while i < len(listOfItems)-1:
			printArray.append('Name %s, Aisle %s, Column %s, Row %s'%(listOfItems[i].name,listOfItems[i].locAisle,listOfItems[i].locCol,listOfItems[i].locRow))
			i+=1
		self.scrollbar = Scrollbar(self)
		self.scrollbar.pack(side=RIGHT,fill=Y)
		
		self.listbox = Listbox(self,width=40,height=20)
		self.listbox.pack(fill=BOTH,expand=True)
		
		i=0
		for i in range(len(listOfItems)-1):
			self.listbox.insert(END,printArray[i])
			
		self.listbox.config(yscrollcommand=self.scrollbar.set)
		self.scrollbar.config(command=self.listbox.yview)
		
		self.returnButton = Button(self,text='Return',font=("Times",14),command=lambda ty = 6: self.clientEmployee(ty),height=2,width=5)
		self.returnButton.place(relx=.825,rely=.775)
		
			
			
	def clientPrintStatus(self,ty,label):
		self.printLabel = Label(self,text=label,font=("Times",14))
		self.printLabel.place(relx=.3,rely=.9)
									  
	def clientCheckItems(self):
		self.addItemButton.destroy()
		self.removeItemButton.destroy()
		self.printListButton.destroy()
		self.checkMisplacedButton.destroy()
		self.logOffButton.destroy()
		self.text.destroy()
		
		self.scrollbar = Scrollbar(self)
		self.scrollbar.pack(side=RIGHT,fill=Y)
		
		self.listbox = Listbox(self,width=40,height=20)
		self.listbox.pack(fill=BOTH,expand=True)
		
		self.listbox.config(yscrollcommand=self.scrollbar.set)
		self.scrollbar.config(command=self.listbox.yview)
		
		self.returnButton = Button(self,text='Return',font=("Times",14),command=lambda ty = 6: self.clientEmployee(ty),height=2,width=5)
		self.returnButton.place(relx=.825,rely=.775)
		
		self.checkButton = Button(self,text='Check Again',font=("Times",14),command=self.checkAgain,height=2,width=8)
		self.checkButton.place(relx=.025,rely=.775)
		
		i=0
		colorSensor=ColorSensorTest.ColorSensor()
		print colorSensor
		while i < 3:
			if(colorSensor[i] == 0):#fFSR ==1
				self.listbox.insert(END,'Item at Row: 1 and Column: %s is misplaced'%(i+1))
			elif(colorSensor[i] == 0):#FSR!=1
				self.listbox.insert(END,'Item at Row: 1 and Column: %s has a color difference'%(i+1))
			i+=1
		
	def checkAgain(self):
		self.listbox.destroy()
		self.scrollbar.destroy()
		self.checkButton.destroy()
		self.returnButton.destroy()
		
		self.scrollbar = Scrollbar(self)
		self.scrollbar.pack(side=RIGHT,fill=Y)
		
		self.listbox = Listbox(self,width=40,height=20)
		self.listbox.pack(fill=BOTH,expand=True)
		
		self.listbox.config(yscrollcommand=self.scrollbar.set)
		self.scrollbar.config(command=self.listbox.yview)
		
		self.returnButton = Button(self,text='Return',font=("Times",14),command=lambda ty = 6: self.clientEmployee(ty),height=2,width=5)
		self.returnButton.place(relx=.825,rely=.775)
		
		self.checkButton = Button(self,text='Check Again',font=("Times",14),command=self.checkAgain,height=2,width=8)
		self.checkButton.place(relx=.025,rely=.775)
		
		i=0
		colorSensor=ColorSensorTest.ColorSensor()
		print colorSensor
		while i < 3:
			if(colorSensor[i] == 0):#fFSR ==1
				self.listbox.insert(END,'Item at Row: 1 and Column: %s is misplaced'%(i+1))
			elif(colorSensor[i] == 0):#FSR!=1
				self.listbox.insert(END,'Item at Row: 1 and Column: %s has a color difference'%(i+1))
			i+=1
									  
	def employeeLogOff(self):
		self.addItemButton.destroy()
		self.removeItemButton.destroy()
		self.printListButton.destroy()
		self.checkMisplacedButton.destroy()
		self.logOffButton.destroy()
		self.text.destroy()		
		self.init_window()
									  

def updateUsed(num):
	global used
	used=num

user = User('')
listOfItems = []
arrayOfItems = []
used = 0
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


root = Tk()
root.geometry("550x300")
root.resizable(0,0)

app = Window(root)

root.mainloop()