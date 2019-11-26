import sys
from os.path import isfile, join
from os import listdir
import os
import re

tdMatrix = []

listDocs = []

def readFile(folderPrePath, fileName):
    global listDocs
    print("Prepocessing file: "+str(folderPrePath+fileName))
    # Read the content
    proccessedWords = []
    f = folderPrePath + fileName
    with open(f) as fp:
        line = fp.readline()
        while line:
            line = fp.readline()
            line = line.replace("\n", "")
            proccessedWords.append(line)
    listDocs.append(proccessedWords)


def main():
    global listDocs
    if len(sys.argv) > 2:
        folderPrePath = sys.argv[1]
        folderPostPath = sys.argv[2]

        if not os.path.exists(folderPostPath):
            os.makedirs(folderPostPath)

        onlyfiles = [f for f in listdir(
            folderPrePath) if isfile(join(folderPrePath, f))]
        
        onlyfiles.sort(key = int) 

        for fileName in onlyfiles:
            readFile(folderPrePath, fileName)
        
    else:
        print("Usage: \n main.py \"folder\" \"destination folder\" ")


if __name__ == "__main__":
    main()
