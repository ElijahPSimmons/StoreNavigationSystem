#!/usr/bin/python2.7
#Update the written list so that it saves what you have added into the list
def updateWrittenList(listOfItems):
	file = open('database.txt','w')
	i = 0
	for item in listOfItems:
		file.write("%s,%s,%s,%s,\n" % (listOfItems[i].name,listOfItems[i].locAisle,listOfItems[i].locCol,listOfItems[i].locRow))
		i += 1
	file.close()