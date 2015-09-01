#Named Entity Recognition

The training program is called nelearn.py and the tagging program is called netag.py.

The NER data format is similar to the POS tagging data format, but also includes a POS tag between each word and its NER BIO tag: WORD/POSTAG/NERTAG WORD/POSTAG/NERTAG ...

The test data will contain POS tags, but no NER tags: WORD/POSTAG WORD/POSTAG ...

Output includes the NER tags produced by the system, and should be in the same format as the training and dev datasets.

###Files:

* nelearn.py
* netag.py
* ner.esp.test.out
