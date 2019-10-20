import sys
import time
import os.path

def getNext(pattern, lenPattern, state, char):
    #If the character to process is the same as the one in the state position of the pattern we return the actual state+1
    if state < lenPattern and char == ord(pattern[state]):
        return state+1
    i = 0
    #We have to find the longest prefix that is also sufix
    #We start from the number state (Is the largest value) and we decrease it in each iteration
    for nextState in range(state,0,-1): 
        if ord(pattern[nextState-1]) == char: 
            while(i<nextState-1): 
                if pattern[i] != pattern[state-nextState+1+i]: 
                    break
                i+=1
            #If it matches then we return it, this should be the next state
            if i == nextState-1: 
                return nextState  
    #If we dont get here means that in this state this character doesnt goes to another state
    return 0


def buildSearchTable(pattern, lenPattern):
    NCHARS = 256
    #We build the table that allows us to look up for the next state
    #The rows is the number of states, and the cols are the pattern + 1
    searchTable = [[0 for i in range(NCHARS)] for _ in range(lenPattern+1)]

    for state in range(lenPattern+1): 
        for char in range(NCHARS):
            #For the position [state][char] in the table we get the next state
            nextState = getNext(pattern, lenPattern, state, char) 
            searchTable[state][char] = nextState 

    return searchTable

def searchDFA(file, pattern):
    matches = []
    lenPattern = len(pattern)
    # Build the search table which make us able to search the next state
    searchTable = buildSearchTable(pattern, lenPattern)
    for index, line in enumerate(file):
        lenLine = len(line)
        state = 0
        for i in range(lenLine):
            #We get the next state for each character in line
            state = searchTable[state][ord(line[i])]
            #If the state matches the length of the pattern-1 this means there is a match
            if state == (lenPattern-1):
                matches.append([index, i])
    return matches

def main():

    fileName = sys.argv[1]
    file=open(fileName, "r")

    pattern = sys.argv[2]

    time_start = time.process_time()
    pos=searchDFA(file, pattern)
    time_elapsed = time.process_time()
    #If file exists we append the result, if not we create it and write the measure of time
    if os.path.exists('measures.txt'):
        f= open("measures.txt","a+")
    else:
        f= open("measures.txt","w+")
    f.write("Algorithm: DFA \t Time: "+str(time_elapsed)+" secs \t Pattern: " + str(pattern)+"\t N_Matches: "+str(len(pos))+"\n")

if __name__ == "__main__":
    main()