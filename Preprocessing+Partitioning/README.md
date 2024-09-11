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
In this section we're going to explain the methodology followed to determine the relationships between columns of a dataset and the 
cardinality of that relationship. However, right now, the results are experimental and maybe not all the cases can be represented here.

The used methodolgy in this step is treating two columns of the dataset `A` and `B` where we'll somehow transform these columns to 
mathematical sets and study its possible relationships. In order to do so, we study if they follow the definition of function or not,
in the following way:

![image](https://github.com/user-attachments/assets/68ca8305-cef5-4bad-9386-d7e874d40fde)
Source: https://en.wikipedia.org/wiki/Bijection,_injection_and_surjection

![image](https://github.com/user-attachments/assets/9d537924-5dcd-4bd6-a054-50c2ce34d536)
Source: https://www.mathsisfun.com/sets/injective-surjective-bijective.html

As we can see, there's 4 cases where the relation `A -> B` can be a function and 1 where it's not a function. Among these cases, we
also study the data, i.e. if it contains duplicates, if it contains NAs, etc.

# 3. Feature vector (doc)

# 4. Functional Dependencies (doc)

# 5. Final conclusions (and future work?)
