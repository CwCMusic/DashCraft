import json, ast


with open('masterList.txt', encoding="utf-8") as f:
    lines = f.readlines()
    finalList = [ast.literal_eval(i) for i in lines]

#print("Last tracks: " + str(finalList[-10:-1]))
#print("10000th track: " + str(finalList[9999]))
#print("Length: " + str(len(finalList)))

nameDict = {}

for i in finalList:
    a = i['user']['username']
    if a in nameDict:
        nameDict[a] += 1
    else:
        nameDict[a] = 1

print(sorted(nameDict.items(), key=lambda x:x[1]))