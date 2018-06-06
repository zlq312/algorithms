import dt
testFile = 'wdbc-test.csv'
examFile = 'wdbc-train.csv'
attrFile = 'wdbc.names'
def predict (tree, example, attributes):
    result = 0
    # if not a leaf node, go thought branch; if is leaf node, then it is the result
    if (isinstance(tree, dict)):
        att = tree[tree.keys()[0]]
        # get the index of current attribute
        index = attributes.index(tree.keys()[0])
        if att.keys()[0][0] == ">=":
            if example[index] >= att.keys()[0][1]:
                result = predict(att[att.keys()[0]], example, attributes)
            else:
                result = predict(att[att.keys()[1]], example, attributes)
        elif att.keys()[1][0] == ">=":
            if example[index] >= att.keys()[1][1]:
                result = predict(att[att.keys()[1]], example, attributes)
            else:
                result = predict(att[att.keys()[0]], example, attributes)
    else:
        result = tree
    return result

def test (tree, examples, attributes, classAttr):
    classIndex = attributes.index(classAttr)
    wrongCount = 0
    for e in examples:
       if(predict(tree, e, attributes) != e[classIndex]):
           wrongCount += 1
    print "total test examples:", len(examples)
    print "wrong class:", wrongCount
    print "accuracy rate:",1 - (wrongCount*1.0/len(examples))

myTree = dt.generate(examFile,attrFile)
exampleFile = open(testFile)
example = [[]]
for line in exampleFile:
    line = line.strip("\r\n")
    example.append(line.split(','))
example.remove([])
# get attributes
attrFile = open(attrFile)
attrFile.readline()
line = attrFile.readline().strip("\r\n ")
# get rid of potential "space"
line = line.translate(None, " ")
attrs = line.split(',')
# the last attribute as class attribute
attrs.append("class")
test(myTree, example, attrs, "class")

