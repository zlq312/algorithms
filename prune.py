import dt

# input filename with training set
trainFile = "wdbc-train.csv"
# input filename with attribute
attrFileName = "wdbc.names"
# input filename with prune set
pruneFile = "wdbc-prune.csv"

# assume this is a complete binary tree
def traverse(tree, examples, attributes, classAttr, parent, lr):
    # if not leaf node
    if (isinstance(tree, dict)):
        # if child is a leaf
        #if not isinstance(tree[tree.keys()[0]],dict):
            # not useful
         #   print "single"
        #else:
            att = tree[tree.keys()[0]]
            subexa0 = [[]]
            subexa1 = [[]]
            # generate subset for each node
            if ">=" == att.keys()[0][0]:
                for e in examples:
                    if e[attributes.index(tree.keys()[0])] >= att.keys()[0][1]:
                        subexa0.append(e)
                    else:
                        subexa1.append(e)
            if "<" == att.keys()[0][0]:
                for e in examples:
                    if e[attributes.index(tree.keys()[0])] < att.keys()[0][1]:
                        subexa0.append(e)
                    else:
                        subexa1.append(e)
            subexa0.remove([])
            subexa1.remove([])
            # if all chirldren are leaf, then consider pruning
            if( not isinstance(att[att.keys()[0]], dict) and not isinstance(att[att.keys()[1]], dict)):
                pruneFlag = prune(att, examples, subexa0, subexa1, attributes, classAttr)
                if pruneFlag:
                    # if prune, set the node as the major class value
                    major = dt.plurality(examples, attributes, classAttr)
                    # if major is None, then assign a fake value, then it will be prune next time
                    if not major:
                        parent[parent.keys()[lr]] = -1
                    else:
                        parent[parent.keys()[lr]] = major
                    # if prune occur, end the traverse
                    return False
                # if all children are leaf, do not need go futher
                return True
            traverse(att[att.keys()[0]], subexa0, attributes, classAttr, att, 0)
            #    return False
            traverse(att[att.keys()[1]], subexa1, attributes, classAttr, att, 1)
            #    return False
    return True

def prune(att, examples, subexa0, subexa1, attributes, classAttr):

    index = attributes.index(classAttr)
    # compute the accuracy for each node
    errorCount0 = 0.0
    for s0 in subexa0:
        if s0[index] != att[att.keys()[0]]:
            errorCount0 += 1
    errorCount1 = 0.0
    for s1 in subexa1:
        if s1[index] != att[att.keys()[1]]:
            errorCount1 += 1
    lenAll = len(subexa0) + len(subexa1)
    # if no data comes to these children, then prune
    if lenAll == 0:
        return True
    # compute weighted error rate for subnodes
    errsub = 0
    if (len(subexa0) != 0):
        errsub += (len(subexa0)*1.0/lenAll) * (errorCount0/len(subexa0))
    if (len(subexa1) != 0):
        errsub += (len(subexa1)*1.0/lenAll) * (errorCount1/len(subexa1))
    # compute error rate if prune
    major = dt.plurality(examples, attributes, classAttr)
    errorCountAll = 0.0
    for e in examples:
        if e[index] != major:
            errorCountAll += 1
    errParent = errorCountAll*1.0 / lenAll
    if round(errParent,3) > round(errsub,3):
        return False
    else:
        return True

def doPrune(pruneFile, attrFileName, myTree):
    exampleFile = open(pruneFile)
    example = [[]]
    for line in exampleFile:
        line = line.strip("\r\n")
        example.append(line.split(','))
    example.remove([])
    # get attributes
    attrFile = open(attrFileName)
    attrFile.readline()
    line =  attrFile.readline().strip("\r\n ")
    attrs = line.split(', ')
    # the last attribute as class attribute
    attrs.append("class")
    flag = False
    #count = 0
    #while( not flag):
     #   flag = traverse(myTree, example, attrs, "class", None, None)
      #  count += 1
    for i in range(50):
        traverse(myTree, example, attrs, "class", None, None)

myTree = dt.generate(trainFile, attrFileName)
doPrune(pruneFile, attrFileName, myTree)
dt.showTree(myTree)
