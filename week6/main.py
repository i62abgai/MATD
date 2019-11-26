import sys
from os.path import isfile, join
from os import listdir
import os
import re
import itertools

listDocs = []

def invertIndex(folderPrePath, fileName, folderPostPath):
    """Function that creates the inverted index for each document 
    
    Arguments:
        folderPrePath {[string]} -- [String with the path of the folder with the documents]
        fileName {[string]} -- [String with the name of the file to create the inverted index]
        folderPostPath {[string]} -- [String with the path of the folder where the documents are going to be saved]
    """    
    #print("Prepocessing file: "+str(folderPrePath+fileName))
    global listDocs
    # Read the content
    f = folderPrePath + fileName
    with open(f) as fp:
        line = fp.readline()
        while line:
            line = fp.readline()
            line = line.replace("\n", "")
            listDocs.append([line, fileName])



def takeWord(elem):
    """[Function that returns the first element (key) from an 2D array]
    
    Arguments:
        elem {[Array]} -- [Array of two elements (key and document)]
    
    Returns:
        [String] -- [key]
    """    
    return elem[0]


def sortList():
    """[Order the list]
    """    
    global listDocs
    listDocs.sort(key=takeWord)


def getDistinct():
    """[Get the unique elements from the list]
    """    
    global listDocs
    unique_data = [list(x) for x in set(tuple(x) for x in listDocs)]
    listDocs = unique_data


def mergeItems():
    """[Merge the items in the listdocs so the documents where they are is the same for each element]
    """    
    global listDocs
    result = [
        [k, [x[1] for x in g]]
        for k, g in itertools.groupby(listDocs, takeWord)
    ]
    listDocs = result


def main():
    """[Main function]"""        
    global listDocs
        
    if len(sys.argv) > 2:
        folderPrePath = sys.argv[1]
        folderPostPath = sys.argv[2]

        if not os.path.exists(folderPostPath):
            os.makedirs(folderPostPath)

        onlyfiles = [f for f in listdir(
            folderPrePath) if isfile(join(folderPrePath, f))]

        for fileName in onlyfiles:
            invertIndex(folderPrePath, fileName, folderPostPath)
            
        sortList()
        getDistinct()
        sortList()
        mergeItems()
        
        query = input("Search: ")
        splitted = query.split()
        dictionary = dict(listDocs)
        saveList = []
        for word in splitted:
            if word in dictionary:
                if not saveList:
                    saveList = dictionary[word]
                else:
                    saveList = set(dictionary[word]).intersection(saveList)
            else:
                print("Couldn't find results for '"+ word+"'")
        queryDocs = set(saveList)
        queryDocs = sorted(queryDocs)
        
        print("You can find these words in: ")
        for word in queryDocs:
            print(word)
        
        # Write the file
        f = open((folderPostPath+"list.txt"), 'w+')
        for word in listDocs:
            f.write(str(word)+"\n")
        f.close()
        
    else:
        print("Usage: \n main.py \"original folder\" \"destination folder\" ")


if __name__ == "__main__":
    main()
