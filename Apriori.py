%%time

#import libraries
import pandas as pd
import numpy as np


#initialize path for files
path1 = ""
path2 = ""
path3 = ""
path4 = ""
path5 = ""
    
data = pd.read_csv(path2, header = None)
#rename columns to make it look cleaner
data.rename(columns = {0: 'Items'}, inplace = True)
    
#split data into list
dataList = data.Items.str.split(',')
#print(dataList)


# count individual items and eliminate any that dont meet user support
def countItems(dataList):
    #create dictionary
    itemCount = dict()
    #loop through individual items
    for row in dataList:
        for i in range(len(row)):
            if row[i] in itemCount.keys():
                itemCount[row[i]] += 1
            else:
                itemCount[row[i]] = 1
    
    #create a dataframe
    itemData = pd.DataFrame()
    itemData['Item_Sets'] = itemCount.keys()
    itemData['Support'] = itemCount.values()
    #convert to integer
    itemData['Support'] = itemData['Support'].astype(int)
    
    return itemData

def count2Items(LiItems):
    item_list = []
    for i in range(len(LiItems)):
        for j in range(len(LiItems)):
            if i != j:
                item_list.append((LiItems[i],LiItems[j]))
    return item_list

def count3Items(LiItems,dataList):
    multItemSets = []
    #print(LiItems)
    c = 1
    for item1 in LiItems:
        prevItems = LiItems[c:]
        #print(item1)
        for item2 in prevItems:
            #print(item2)
            if (item1[0:-1] == item2[0:-1]) and (item1[-1] != item2[-1]):
                if item1[0:-1] > item2[0:-1]:
                    multItemSets.append((item2 + item1[1:]))
                else:
                    multItemSets.append((item1 + item2[1:]))  
        c += 1
    return multItemSets

#count Itemsets and support for two or more items
def freq(LiItems,dataList):
    item_dict = {}
    #print(Li)
    for entry in LiItems:
        #create a set to compare sets from original list 
        setEntry = set(entry)
        for row in dataList:
            #create a set for the rows
            setRow = set(row)
            #find where both sets contain similar sets and add to dictionary
            if setEntry.intersection(setRow) == setEntry:
                if entry in item_dict.keys():
                    item_dict[entry] += 1
                else:
                    item_dict[entry] = 1
            #print(item_dict)
    #create a dataframe
    itemsetsData = pd.DataFrame()
    itemsetsData['Item_Sets'] = item_dict.keys()
    itemsetsData['Support'] = item_dict.values()
    #convert to integer
    itemsetsData['Support'] = itemsetsData['Support'].astype(int)

    return itemsetsData

#eliminate support
def comp_Supp(df,supp):
    #eliminate supp < minsupp
    df = df[df.Support.astype(int) >= supp] 
    return df

#calculate confidence
def compute_conf(suppx,suppy):
    c = round(int(suppx)/int(suppy)*100,2)
    return c

#compute confidence
def confidence(Li,L1,conf):
    #create dictionary
    confDict = {}
    for row in Li.Item_Sets:
        for item in range(len(row)):
            for entry in range(len(row)):
                 if item != entry:
                        suppx = Li[Li.Item_Sets == row].Support
                        suppy = L1[L1.Item_Sets == row[item]].Support
                        confid = compute_conf(suppx,suppy)
                        confDict[(row[item], row[entry])] = confid
                        #print(confDict)
        
    confData = pd.DataFrame()
    confData['Item_Sets'] = confDict.keys()
    #print(confData.Item_Sets)
    confData['Confidence'] = confDict.values()
    
    #eliminate confidence
    return confData[confData.Confidence >= conf]
    
#support and confidence
supp = int(input("Choose a support in percentages(%):"))
#convert support to number
supp = int((supp/100)*len(dataList))
#print(supp)
conf = int(input("Choose a confidence level in percentages(%):"))



#L1
L1df = countItems(dataList)
L1 = comp_Supp(L1df,supp)
L1List = (L1.Item_Sets).tolist()

#L2
L2List = count2Items(L1List)
L2Freq = freq(L2List,dataList)
L2 = comp_Supp(L2Freq,supp)
L2Items = L2.Item_Sets.tolist()
#print(L2)
#L3
L3List = count3Items(L2Items,dataList)
L3Freq = freq(L3List,dataList)
L3 = comp_Supp(L3Freq,supp)
L3Items = L3.Item_Sets.tolist()
#print(L3)


    
confidence(L2,L1,conf)