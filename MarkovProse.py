import random
import sys
import codecs

input = open("shakespeare.txt", "r", encoding="utf-8").read()
#input = input.replace("\n"," ").replace(":"," ")
words = input.split(' ')

wordDict = {}
length = 1000
index = 1

for w in words[index:]:
    key = words[index - 1]
    if key in wordDict:
        wordDict[key].append(w)
    else:
        wordDict[key] = [w]
    index += 1

currentWord = random.choice(list(wordDict.keys()))
poem = currentWord.capitalize()

while len(poem.split(' ')) < length:
    nextWord = random.choice(wordDict[currentWord])
    currentWord = nextWord
    poem += ' ' + nextWord

output = codecs.open("test.txt", "w+", "utf-8")
output.write(poem)
output.close()