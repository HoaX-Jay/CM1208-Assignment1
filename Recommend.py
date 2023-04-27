import math

def ReadInHistoryFile (fileName):
    f = open (fileName,"r")
    firstLine = f.readline().split()
    numCustomers = int(firstLine[0])
    numItems = int(firstLine[1])
    numTransactions = int(firstLine[2])

    historyTable = [[0] * numItems for _ in range (numCustomers)]

    for _ in range(numTransactions):
        nextLine = f.readline().split()
        customerID = int(nextLine[0])
        itemID = int(nextLine[1])
        historyTable[customerID - 1][itemID - 1] = 1
    
    counter = 0
    for row in historyTable:
        for item in row:
            if item != 0:
                counter +=1
    print("Positive Entries : ", counter)
    
    # print(numCustomers)
    # print(numItems)
    # print(numTransactions)
    #print(historyTable)
    return historyTable

def PrecomputeAngles (historyTable):
    anglesOfItems = {}
    numCustomers, numItems = len(historyTable), len(historyTable[0])
    allAngles = 0
    for i in range(numItems):
        for j in range (i +1, numItems):
            dotProduct = 0
            for k in range(numCustomers):
                dotProduct += historyTable[k][i] * historyTable[k][j]
            normOne = math.sqrt(sum([historyTable[k][i] ** 2 for k in range(numCustomers)]))
            normTwo = math.sqrt(sum([historyTable[k][j] ** 2 for k in range(numCustomers)]))
            angle = math.degrees(math.acos(dotProduct/(normOne*normTwo)))
            anglesOfItems[(i+1, j+1)] = angle
            allAngles +=angle

            print(angle)
    averageAngle = allAngles/len(anglesOfItems)
    print("Average angle : ", round(averageAngle,2))
    return(anglesOfItems)




def ReadInQueriesFile(fileName,historyTable,anglesOfItems):
    f = open (fileName,'r')
    for i in f:
        shoppingCart = [int(x) for x in i.split()]
        print("Shopping Cart: ", shoppingCart)
        Recommendations(shoppingCart, historyTable, anglesOfItems)


def Recommendations(shoppingCart, historyTable, anglesOfItems):
    candidates = []
    for item in shoppingCart:
        minAngle = 90  
        matchId = -1
        for i in range(len(historyTable[0])):
            if i+1 not in shoppingCart:
                if (i+1, item) in anglesOfItems:
                    angle = anglesOfItems[(i+1, item)]
                elif (item, i+1) in anglesOfItems:
                    angle = anglesOfItems[(item, i+1)]
                else:
                    angle = 90  
                if angle < minAngle:
                    minAngle = angle
                    matchId = i+1
        if matchId != -1:  
            candidates.append((matchId, minAngle))
            print("Item: {}; match: {}; angle: {}".format(item, matchId, round(minAngle,2)))
        else:
            print("Item: {}; no match".format(item))
    
    
    uniqueItems = set()
    recommendationList = []
    for candidate in sorted(candidates, key=lambda x: x[1]):
        if candidate[0] not in uniqueItems:
            recommendationList.append(candidate[0])
            uniqueItems.add(candidate[0])
    print("Recommend: {}".format(recommendationList))
    


historyTable = ReadInHistoryFile("history.txt") 
anglesOfItems = PrecomputeAngles(historyTable)
ReadInQueriesFile("queries.txt",historyTable,anglesOfItems)
