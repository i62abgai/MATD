import sys
import time
import os.path


def patternPreprocess(pattern, lenPattern):
    #Defined with bad character heuristic
    searchTable = [-1]*256

    for i in range(lenPattern):
        searchTable[ord(pattern[i])] = i

    return searchTable

def searchBoyer(file, pattern):
    matches = []
    lenPattern = len(pattern)
    searchTable = patternPreprocess(pattern, lenPattern)
    for index, line in enumerate(file):
        lenLine = len(line)
        i = 0
        while i <= lenLine-lenPattern:
            j = lenPattern - 1
            #We search from the last character
            while j >= 0 and pattern[j] == line[j+i]:
                j -= 1
            #We found a match so we shift the number of chars
            if j < 0:
                matches.append([index, i])
                i += (lenPattern - searchTable[ord(line[i+lenPattern])] if i+lenPattern<lenLine else 1)
            else:
                #We shift the max between 1 and the position in the pattern that missmatched
                i += max(1, j-searchTable[ord(line[i+j])])    
    return matches

def main():

    fileName = sys.argv[1]
    file=open(fileName, "r")

    pattern = sys.argv[2]

    time_start = time.process_time()
    pos=searchBoyer(file, pattern)
    time_elapsed = time.process_time()
    #If file exists we append the result, if not we create it and write the measure of time
    if os.path.exists('measures.txt'):
        f= open("measures.txt","a+")
    else:
        f= open("measures.txt","w+")
    f.write("Algorithm: Boyer Moore \t Time: "+str(time_elapsed)+" secs \t Pattern: " + str(pattern)+" \t N_Matches: "+ str(len(pos)) +"\n")

if __name__ == "__main__":
    main()