# TODO: Document and explain the code
In this file I'll try to deeepen in and tackle all the topics related to the current preprocessing and partitioning steps of the 
OntoGenix pipeline/workflow.

# 0. Introduction/Abstract
This briefing section is needed for people who suffer from "tldr;" condition and want the conclusions before even started reading it. 
So, in conclusion, all the code implemented in this folder helps us have a better understandment of how the data behave and is related 
without a prior knowledge of the area that the data is modeling. In other words, and thanks to human+LLM work, we're now able to provide 
an efficient and improved way to tackle larger datasets so that we can provide to the LLM with more specific information to tackle the 
ontology creation problem. 

To help us achieve this efficiency we had use Machine Learning (ML) and statistical approaches, such as "Domain Knowledge and Practical 
constraints", while some known methods like Clustering-based K-means were discarted for its time and resource cosumption. These methods
helped us find herustics to determine what rows of the dataset were really relevant for the later study of the data. Doing so, we reduce
larger datasets, i.e. half million rows with multiple columns, into more manageable smaller datasets without too much information loss.

# 1. Preprocessing (niy: not implemented yet)
Basically, treating all data as characters (or strings) and converting them to factors (or numbers). After that, we eliminated the 
duplicated rows and (optionaly) removed the rows that contained null data (NA). However, it's possible to not do so if we know beforehand
that NAs have indeed a meaning while interpreting the data. Doing so helped us reduce the size of the dataset by removing redundant data.

[...]

# 2. Cardinality matrix (doc)

# 3. Feature vector (doc)

# 4. Functional Dependencies (doc)

# 5. Final conclusions (and future work?)
