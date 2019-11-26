from __future__ import division
from struct import pack, unpack
from os.path import isfile, join
from os import listdir
import sys
import os
import re
import itertools


listDocs = []

stopList = ['', 'a', 'an', 'and', 'are', 'as',
            'at', 'be', 'by', 'for', 'from',
            'has', 'he', 'in', 'is', 'it', 'its',
            'of', 'on', 'that', 'the', 'to',
            'was', 'were', 'will', 'with'
            ]


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


def longestSubstringFinder(string1, string2):
    answer = ""
    len1, len2 = len(string1), len(string2)
    for i in range(len1):
        match = ""
        for j in range(len2):
            if (i + j < len1 and string1[i + j] == string2[j]):
                match += string2[j]
            else:
                if (len(match) > len(answer)):
                    answer = match
                match = ""
    return answer


def deleteStopList(wordList):
    global stopList
    wL = []
    for i, word in enumerate(wordList):
        if not word[0] in stopList:
            wL.append(word)
    return wL


def encode_number(number):
    """[Variable byte codes]

    Arguments:
        number {[int]} -- [Int variable to compress]

    Returns:
        [int] -- [Encoded int (Compressed)]
    """
    bytes_list = []
    while True:
        bytes_list.insert(0, number % 128)
        if number < 128:
            break
        number = number // 128
    bytes_list[-1] += 128
    return pack('%di' % len(bytes_list), *bytes_list)


def compressDict(listDocs):
    dictString = ""
    compressedList = []
    for i, x in enumerate(listDocs):
        compressedList.append([len(dictString), x[1]])
        dictString += x[0]
    return compressedList, dictString


def compressPL(listDocs):
    compressed = []
    for i, x in enumerate(listDocs):
        c = encode_number(x[0])
        compressed.append([c, x[1]])
    return compressed


def encode_unary(n):
    return n*'1'+'0'


def compressUC(listDocs):
    compressed = []
    for i, x in enumerate(listDocs):
        c = encode_unary(x[0])
        compressed.append([c, x[1]])
    return compressed


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
        
        # Delete some characters (It's bugged)
        listDocs = deleteStopList(listDocs)

        # Write the file dict
        f = open((folderPostPath+"list.txt"), 'w+')
        for word in listDocs:
            f.write(str(word)+"\n")
        f.close()

        print("Inverted index dictionary compression\n")
        # Compress the dict
        listDocsCompressed, dictString = compressDict(listDocs)
        print("\tNot compressed: ", sys.getsizeof(listDocs)/1024, "kB\n\tDictionary compressed:",
              (sys.getsizeof(listDocsCompressed)+sys.getsizeof(dictString))/1024, "kB ")

        # Write the file dict compressed
        f = open((folderPostPath+"dictCompressed.txt"), 'w+')
        f.write(dictString+"\n")
        for word in listDocsCompressed:
            f.write(str(word)+"\n")
        f.close()

        print("\n\nInverted index posting list compression\n")
        # Compress posting list
        listDocsCompressedPL = compressPL(listDocsCompressed)
        print("\tDictionary compressed: ", (sys.getsizeof(listDocsCompressed)+sys.getsizeof(dictString))/1024,
              "kB\n\tPosting List Compressed:", (sys.getsizeof(listDocsCompressed)+sys.getsizeof(dictString))/1024, "kB ")

        # Write the file posting list compressed
        f = open((folderPostPath+"PostingCompressed.txt"), 'w+')
        f.write(dictString+"\n")
        for word in listDocsCompressedPL:
            f.write(str(word)+"\n")
        f.close()

        print("\n\nInverted index unary coding compression\n")
        # Compress posting list
        listDocsCompressedUC = compressUC(listDocsCompressed)
        print("\tDictionary compressed: ", (sys.getsizeof(listDocsCompressed)+sys.getsizeof(dictString))/1024,
              "kB\n\tUnary Coding List Compressed:", (sys.getsizeof(listDocsCompressedUC)+sys.getsizeof(dictString))/1024, "kB ")

        # Write the file posting list compressed
        f = open((folderPostPath+"UnaryCompressed.txt"), 'w+')
        f.write(dictString+"\n")
        for word in listDocsCompressedUC:
            f.write(str(word)+"\n")
        f.close()

        """query = input("\n\n\tSearch: ")
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
                print("Couldn't find results for '" + word+"'")
        queryDocs = set(saveList)
        queryDocs = sorted(queryDocs)

        print("You can find these words in: ")
        for word in queryDocs:
            print(word)"""

    else:
        print("Usage: \n main.py \"original folder\" \"destination folder\" ")


if __name__ == "__main__":
    main()
