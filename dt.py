import math
def treeLearning(examples, attributes, parent, classAttr, recursion):
    # control the deepth of the tree
    recursion += 1
    if recursion >= 100:
        return plurality(parent, attributes, classAttr)
    examples = examples[:]
    # get class value for each example
    classVals = [e[attributes.index(classAttr)] for e in examples]
    # if there is no examples in this branch
    # or no attribute left
    # choose majority class value in parent node
    if not examples or (len(attributes) - 1) <= 0:
        return plurality(parent, attributes, classAttr)
    # if all examples under same class value, return that class value
    # (equal to if the length of classVals = # of one value in classVals)
    elif classVals.count(classVals[0]) == len(classVals):
        return classVals[0]
    else:
        # get the best attribute to split, and the split point
        best = importace(attributes, examples, classAttr)
        # use dictionary to repersent a tree
        tree = {best['attr']:{}}
        # generate two subtrees
        # get all examples under a branch
        exsBig = getExamples(attributes, examples, best['attr'], best['splitpoint'], "bigger")
        exsSmall = getExamples(attributes, examples, best['attr'], best['splitpoint'], "smaller")
        # get rid of the attribute already splitted
        #newAttr = attributes[:]
        #newAttr.remove(best['attr'])
        # gnerate two subtrees
        #subtree = treeLearning(exsBig, newAttr, examples, classAttr)
        subtree = treeLearning(exsBig, attributes, examples, classAttr, recursion)
        tree[best['attr']][">=", (best['splitpoint'])] = subtree
        #subtree = treeLearning(exsSmall, newAttr, examples, classAttr)
        subtree = treeLearning(exsSmall, attributes, examples, classAttr, recursion)
        tree[best['attr']]["<", (best['splitpoint'])] = subtree
    return tree

def getExamples(attributes, examples, bestAttr, splitpoint, compare):
    subExs = [[]]
    # get the index of the split attribute
    index = attributes.index(bestAttr)
    for e in examples:
        #find entries with the give value
        if (compare == "bigger"):
            if (e[index] >= splitpoint):
                newExs = []
                # get rid of the best attribute
                for i in range(0,len(e)):
                  #  if(i != index):
                    newExs.append(e[i])
                subExs.append(newExs)
        if(compare == "smaller"):
            if (e[index] < splitpoint):
                 newExs = []
                 # get rid of the best attribute
                 for i in range(0,len(e)):
                     #if(i != index):
                     newExs.append(e[i])
                 subExs.append(newExs)
    subExs.remove([])
    return subExs

def plurality(examples, attributes, classAttr):
    # frequency of class attribute value
    valFreq = {}
    # get the index of class attribute
    index = attributes.index(classAttr)
    # calculate frequency of class value
    for e in examples:
        if (valFreq.has_key(e[index])):
            valFreq[e[index]] += 1
        else:
            valFreq[e[index]] = 1
    max = 0
    major = ""
    for key in valFreq.keys():
        if valFreq[key] > max:
            max = valFreq[key]
            major = key
    return major


# retrun the attribute that have the highest infomation gain among
# given examples
def importace(attributes, examples, classAttr):
    maxGain = 0
    selAttr = ""
    splitpoint = -1
    classIndex = attributes.index(classAttr)
    for i in range(len(attributes)):
        if i == classIndex:
            continue
        # select examples that have different values of attribute i
        # compute entropy for each branch of i
        best = infoGain(attributes, i, examples, classAttr)
        gain = best['gain']
        if gain >= maxGain:
            maxGain = gain
            selAttr = attributes[i]
            splitpoint = best['splitpoint']
    return {'attr':selAttr, 'splitpoint':splitpoint}

# compute infomation gain(continues value only)
def infoGain(attributes, attributeNo, examples, classAttr):
    # a list that have all different values of attribute
    attValues = getDifferentAttr(attributeNo, examples)
    # compute infomation gain for all possible split point
    # then select the highest one
    maxGain = 0.0
    splitPoint = -1
    # try each split point
    for i in range(0,len(attValues)):
        exampleSet1 = []
        exampleSet2 = []
        # split examples
        for e in examples:
            if e[attributeNo] < attValues[i]:
                exampleSet1.append(e)
            if e[attributeNo] >= attValues[i]:
                exampleSet2.append(e)
        # compute entropy for each part
        entropy1 = entropy(attributes, exampleSet1, classAttr)
        entropy2 = entropy(attributes, exampleSet2, classAttr)
        entropyAll = entropy(attributes, examples, classAttr)
        # compute infomation gain
        gain = entropyAll - (len(exampleSet1)*1.0/len(examples))*entropy1-(len(exampleSet2)*1.0/len(examples))*entropy2
        if gain >= maxGain:
            maxGain = gain
            splitPoint = attValues[i]
    best = {'gain': maxGain, 'splitpoint':splitPoint}
    return best

# compute entropy
def entropy(attributes, examples, classAttr):
    freqList = {}
    entropy = 0.0
    # find index of class attribute
    classIndex = 0
    for i in range(len(attributes)):
        if attributes[i] == classAttr:
            classIndex = i
            break
    # compute frequency for each value of class attribute
    for e in examples:
        if (freqList.has_key(e[i])):
            freqList[e[i]] += 1.0
        else:
            freqList[e[i]] = 1.0
    # compute entropy
    for f in freqList.values():
        entropy += (-f/len(examples)) * math.log(f/len(examples), 2)
    return entropy

# return all different values in an attribute
def getDifferentAttr(attributeNo, examples):
    attValues = []
    for e in examples:
        if attValues.count(e[attributeNo]) == 0:
            attValues.append(e[attributeNo])
    attValues.sort()
    return attValues

# gnerate a tree graph, import a function found on GitHub
def showTree(tree):
    import treePlotter
    treePlotter.createPlot(tree)

# input two files, the example file and the attribute file, output the tree
def generate(exaFileName, attrFileName):
    exampleFile = open(exaFileName)
    example = [[]]
    for line in exampleFile:
        line = line.strip("\r\n")
        example.append(line.split(','))
    example.remove([])
    # get attributes
    attrFile = open(attrFileName)
    attrFile.readline()
    line =  attrFile.readline().strip("\r\n ")
    line = line.translate(None, " ")
    attrs = line.split(',')
    # the last attribute as class attribute
    attrs.append("class")
    tree = treeLearning(example, attrs, None, "class", 0)
    return tree
