from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
from os.path import isfile, join
from os import listdir
import os
import re
import sys

i = 0


def getReuter(text, filePostPath):
    global i
    noTagsList = re.findall("<REUTERS(.*?)>(.*?)</REUTERS>", text, re.DOTALL)
    noTags = ""
    for lines in noTagsList:
        print("Processing: Article ", i)
        body = getBody(lines[1])
        # Delete all symbols in the body and title
        body = deleteSymbols(body)
        # Lower the body
        body = body.lower()
        # Delete all common words
        wordList = str(body).split()
        wordList = deleteStopList(wordList)

        # Write the file
        f = open((filePostPath+str(i)), 'w+')
        i += 1
        for word in wordList:
            f.write(word+"\n")
        f.close()

    return noTags


def getBody(text):
    noTagsList = re.findall("<BODY>(.*?)</BODY>", text, re.DOTALL)
    noTags = ""
    for lines in noTagsList:
        noTags += lines
    return noTags


def getTitle(text):
    noTagsList = re.findall("<TITLE>(.*?)</TITLE>", text, re.DOTALL)
    noTags = ""
    for lines in noTagsList:
        noTags += lines
    return noTags


def deleteSymbols(text):
    noSymbols = re.sub(r'[^\w]', '\n', text)
    noSymbols = ''.join([i for i in noSymbols if not i.isdigit()])
    return noSymbols


def deleteStopList(wordList):
    stop_words = set(stopwords.words('english'))
    word_tokens = wordList

    filtered_sentence = [w for w in word_tokens if not w in stop_words]

    filtered_sentence = []

    for w in word_tokens:
        if w not in stop_words:
            filtered_sentence.append(w)
    return filtered_sentence


def preprocessFile(filePrePath, fileName, filePostPath):

    print("Prepocessing file: "+str(filePrePath+fileName))

    f = open(filePrePath+fileName, 'r')
    # Read the content
    content = f.read()
    # Get only the body tag value
    text = getReuter(content, filePostPath)
    f.close()


def main():
    folderPrePath = sys.argv[1]
    folderPostPath = sys.argv[2]

    if not os.path.exists(folderPostPath):
        os.makedirs(folderPostPath)

    onlyfiles = [f for f in listdir(
        folderPrePath) if isfile(join(folderPrePath, f))]
    for fileName in onlyfiles:
        preprocessFile(folderPrePath, fileName, folderPostPath)


if __name__ == "__main__":
    main()
