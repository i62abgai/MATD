import sys
from os.path import isfile, join
from os import listdir
import os
import re


class PorterStemmer:
    def isCons(self, l):
        if l == "a" or l == "e" or l == "i" or l == "o" or l == "u":
            return False
        else:
            return True

    def isConsonant(self, word, i):
        l = word[i]
        if self.isCons(l):
            if l == "y":
                if i - 1 < 0:
                    return True
                else:
                    if self.isCons(word[i-1]):
                        return False
                    else:
                        return True
            else:
                return True
        else:
            return False

    def isVowel(self, word, i):
        return not(self.isConsonant(word, i))

    # *S the stem ends with S -> is done with the prebuid function from python: endswith

    # *v* the stem contains a vowel

    def containsVowel(self, stem):
        for i in stem:
            if not self.isCons(i):
                return True
        return False

    # *d  the stem ends with a double consonant
    def doubleCons(self, stem):
        if len(stem) >= 2:
            if self.isConsonant(stem, -1) and self.isConsonant(stem, -2):
                return True
            else:
                return False
        else:
            return False

    def getForm(self, word):
        form = []
        formStr = ""
        for i in range(len(word)):
            if self.isConsonant(word, i):
                if i != 0:
                    prev = form[-1]
                    if prev != "C":
                        form.append("C")
                else:
                    form.append("C")
            else:
                if i != 0:
                    prev = form[-1]
                    if prev != "V":
                        form.append("V")
                else:
                    form.append("V")
        for j in form:
            formStr += j
        return formStr

    def getM(self, word):
        form = self.getForm(word)
        m = form.count("VC")
        return m

    # *o he stem ends cvc, where the second c is not W, X or Y
    def cvc(self, word):
        if len(word) >= 3:
            f = -3
            s = -2
            t = -1
            third = word[t]
            if self.isConsonant(word, f) and self.isVowel(word, s) and self.isConsonant(word, t):
                if third != "w" and third != "x" and third != "y":
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def replace(self, orig, rem, rep):
        result = orig.rfind(rem)
        base = orig[:result]
        replaced = base + rep
        return replaced

    def replaceM0(self, orig, rem, rep):
        result = orig.rfind(rem)
        base = orig[:result]
        if self.getM(base) > 0:
            replaced = base + rep
            return replaced
        else:
            return orig

    def replaceM1(self, orig, rem, rep):
        result = orig.rfind(rem)
        base = orig[:result]
        if self.getM(base) > 1:
            replaced = base + rep
            return replaced
        else:
            return orig
    # SSES -> SS
    # IES -> I
    # SS -> SS
    # S -> ""

    def step1a(self, word):
        if word.endswith("sses"):
            word = self.replace(word, "sses", "ss")
        elif word.endswith("ies"):
            word = self.replace(word, "ies", "i")
        elif word.endswith("ss"):
            word = self.replace(word, "ss", "ss")
        elif word.endswith("s"):
            word = self.replace(word, "s", "")
        else:
            pass
        return word
    # (m>0) EED -> EE
    # (*v*) ED -> ""
    # (*v*) ING -> ""

    def step1b_p1(self, word):
        if word.endswith("eed"):
            result = word.rfind("eed")
            base = word[:result]
            if self.getM(base) > 0:
                word = base
                word += "ee"
        elif word.endswith("ed"):
            result = word.rfind("ed")
            base = word[:result]
            if self.containsVowel(base):
                word = base
                word = self.step1b_p2(word)
        elif word.endswith("ing"):
            result = word.rfind("ing")
            base = word[:result]
            if self.containsVowel(base):
                word = base
                word = self.step1b_p2(word)
        else:
            pass
        return word
    # If  the  second  or  third  of  the  rules  in  Step  1b  is  successfull

    def step1b_p2(self, word):
        if word.endswith("at") or word.endswith("bl") or word.endswith("iz"):
            word += "e"
        elif self.doubleCons(word) and not word.endswith("l") and not word.endswith("s") and not word.endswith("z"):
            word = word[:-1]
        elif self.getM(word) == 1 and self.cvc(word):
            word += "e"
        else:
            pass
        return word
    # If ends in "y" and also has a vowel we replace it with "i"
    # If not we let them be

    def step1c(self, word):
        if word.endswith("y"):
            result = word.rfind("y")
            base = word[:result]
            if self.containsVowel(base):
                word = base
                word += "i"
        return word

    def step2(self, word):
        if word.endswith("ational"):
            word = self.replaceM0(word, "ational", "ate")
        elif word.endswith("tional"):
            word = self.replaceM0(word, "tional", "tion")
        elif word.endswith("enci"):
            word = self.replaceM0(word, "enci", "ence")
        elif word.endswith("anci"):
            word = self.replaceM0(word, "anci", "ance")
        elif word.endswith("izer"):
            word = self.replaceM0(word, "izer", "ize")
        elif word.endswith("abli"):
            word = self.replaceM0(word, "abli", "able")
        elif word.endswith("alli"):
            word = self.replaceM0(word, "alli", "al")
        elif word.endswith("entli"):
            word = self.replaceM0(word, "entli", "ent")
        elif word.endswith("eli"):
            word = self.replaceM0(word, "eli", "e")
        elif word.endswith("ousli"):
            word = self.replaceM0(word, "ousli", "ous")
        elif word.endswith("ization"):
            word = self.replaceM0(word, "ization", "ize")
        elif word.endswith("ation"):
            word = self.replaceM0(word, "ation", "ate")
        elif word.endswith("ator"):
            word = self.replaceM0(word, "ator", "ate")
        elif word.endswith("alism"):
            word = self.replaceM0(word, "alism", "al")
        elif word.endswith("iveness"):
            word = self.replaceM0(word, "iveness", "ive")
        elif word.endswith("fulness"):
            word = self.replaceM0(word, "fulness", "ful")
        elif word.endswith("ousness"):
            word = self.replaceM0(word, "ousness", "ous")
        elif word.endswith("aliti"):
            word = self.replaceM0(word, "aliti", "al")
        elif word.endswith("iviti"):
            word = self.replaceM0(word, "iviti", "ive")
        elif word.endswith("biliti"):
            word = self.replaceM0(word, "biliti", "ble")
        return word

    def step3(self, word):
        if word.endswith("icate"):
            word = self.replaceM0(word, "icate", "ic")
        elif word.endswith("ative"):
            word = self.replaceM0(word, "ative", "")
        elif word.endswith("alize"):
            word = self.replaceM0(word, "alize", "al")
        elif word.endswith("iciti"):
            word = self.replaceM0(word, "iciti", "ic")
        elif word.endswith("ful"):
            word = self.replaceM0(word, "ful", "")
        elif word.endswith("ness"):
            word = self.replaceM0(word, "ness", "")
        elif word.endswith("ical"):
            word = self.replaceM0(word, "ical", "ic")
        return word

    def step4(self, word):
        if word.endswith("al"):
            word = self.replaceM1(word, "al", "")
        elif word.endswith("ance"):
            word = self.replaceM1(word, "ance", "")
        elif word.endswith("ence"):
            word = self.replaceM1(word, "ence", "")
        elif word.endswith("er"):
            word = self.replaceM1(word, "er", "")
        elif word.endswith("ic"):
            word = self.replaceM1(word, "ic", "")
        elif word.endswith("able"):
            word = self.replaceM1(word, "able", "")
        elif word.endswith("ible"):
            word = self.replaceM1(word, "ible", "")
        elif word.endswith("ant"):
            word = self.replaceM1(word, "ant", "")
        elif word.endswith("ement"):
            word = self.replaceM1(word, "ement", "")
        elif word.endswith("ment"):
            word = self.replaceM1(word, "ment", "")
        elif word.endswith("ent"):
            word = self.replaceM1(word, "ent", "")
        elif word.endswith("ou"):
            word = self.replaceM1(word, "ou", "")
        elif word.endswith("ism"):
            word = self.replaceM1(word, "ism", "")
        elif word.endswith("ate"):
            word = self.replaceM1(word, "ate", "")
        elif word.endswith("iti"):
            word = self.replaceM1(word, "iti", "")
        elif word.endswith("ous"):
            word = self.replaceM1(word, "ous", "")
        elif word.endswith("ive"):
            word = self.replaceM1(word, "ive", "")
        elif word.endswith("ize"):
            word = self.replaceM1(word, "ize", "")
        elif word.endswith("ion"):
            result = word.rfind("ion")
            base = word[:result]
            if self.getM(base) > 1 and (base.endswith("s") or base.endswith("t")):
                word = base
            word = self.replaceM1(word, "", "")
        return word

    def step5a(self, word):
        if word.endswith("e"):
            base = word[:-1]
            if self.getM(base) > 1:
                word = base
            elif self.getM(base) == 1 and not self.cvc(base):
                word = base
        return word

    def step5b(self, word):
        if self.getM(word) > 1 and self.doubleCons(word) and word.endswith("l"):
            word = word[:-1]
        return word

    def step1(self, word):
        word = self.step1a(word)
        word = self.step1b_p1(word)
        word = self.step1c(word)
        return word

    def stem(self, word):
        word = self.step1(word)
        word = self.step2(word)
        word = self.step3(word)
        word = self.step4(word)
        word = self.step5a(word)
        word = self.step5b(word)
        return word


def makeStem(folderPrePath, fileName, folderPostPath):
    print("Prepocessing file: "+str(folderPrePath+fileName))
    # Read the content
    proccessedWords = []
    p = PorterStemmer()
    f = folderPrePath + fileName
    with open(f) as fp:
        line = fp.readline()
        while line:
            line = fp.readline()
            line = line.replace("\n", "")
            proccessed = p.stem(line)
            proccessedWords.append(proccessed)
    # Delete all empty spaces
    proccessedWords = [x for x in proccessedWords if x]

    # Write the file
    f = open((folderPostPath+fileName), 'w+')
    for word in proccessedWords:
        f.write(word+"\n")
    f.close()


def main():

    if len(sys.argv) > 2:
        folderPrePath = sys.argv[1]
        folderPostPath = sys.argv[2]

        if not os.path.exists(folderPostPath):
            os.makedirs(folderPostPath)

        onlyfiles = [f for f in listdir(
            folderPrePath) if isfile(join(folderPrePath, f))]

        for fileName in onlyfiles:
            makeStem(folderPrePath, fileName, folderPostPath)
    else:
        print("Usage: \n main.py \"folder\" \"destination folder\" ")


if __name__ == "__main__":
    main()
