# Readme

1. To train a tree, modify`dt.generate(trainingSet, attrFile)`in `main.py` ,`attrFile` means the `*.names` file. And run `python main.py`. It will generate the tree, and then show a graph of the tree(generate graph by using a third-party python application)
2. To test a tree, modify the value of `testFile` : the test set; `examFile`: the training set;`attrFile`: the `*.names` file. And run `python test.py`. It will generate the tree first and then run test.
3. To prune, modify the value of `trainFile`;`attrFileName`;`pruneFile` in `prune.py`, it will generate the tree first and do prune, then show the tree graph.