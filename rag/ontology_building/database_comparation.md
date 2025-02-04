# Comparasion of external databases - Ontology building
## The external databases
1. Arango. Allows the semantic and structural similarity search, weighing 0.7 for semantic similarity and 0.3 for structural similarity.
2. Chroma. Allows vector similarity search.
In both databases, 39 ontologies related to E-Commerce are stored.
## Evaluation of the performance 
The performance of each approach will be evaluated using [**OOPS! tool**](https://oops.linkeddata.es/catalogue.jsp)
for ontology assessment. The objective is to identify potential issues that may result in modeling errors in each of the 
ontologies built by the LLM using these external databases.
### Summary table - general performance 
This table shows the pitfalls (common errors) for each approach in the construction of 5 different ontologies from 5 different CSV files related to E-Commerce.
| Pitfall  | Arango  | Chroma  |
|------------|------------|------------|
| Critical | 0 | 0 |
| Important | 9 | 6 |
| Minor | 9 | 13 |

Arango has 3 more Important pitfalls but 4 less Minor pitfalls compared to Chroma.
### Pitfalls by CSV test file
![Arango pitfalls](../images/ArangoDB_pifalls.png)
![Chroma pitfalls](../images/ChromaDB_pifalls.png)

