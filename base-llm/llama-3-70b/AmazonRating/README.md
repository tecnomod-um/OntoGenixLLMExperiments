# Llama-3-70B

## Llama-3-70B-4bits

[Generated ontology](./ontology.txt)
<br>
[Corrected ontology](./ontology_corrected.txt)
<br>
![](./ontology_corrected.png)


### Errors

Incorrect serialization:
-   Incorrect blank nodes. Example:
    ```
    base_ontology:hasProductId [ a rdf:Property ; 
        rdfs:domain base_ontology:Product ;
        rdfs:range xsd:string ;
        rdf:type rdf:Property ;
    ].
```


### URIs

| Prefix | URI                                           | Validity | Corrected |
|--------|-----------------------------------------------|----------|-----------|
| rdf    | http://www.w3.org/1999/02/22-rdf-syntax-ns#   | X        | -         |
| rdfs   | http://www.w3.org/2000/01/rdf-schema#         | X        | -         |
| owl    | http://www.w3.org/2002/07/owl#                | X        | -         |
| xsd    | http://www.w3.org/2001/XMLSchema#             | X        | -         |
|        |                                               | **4**    | **0**     |


| URI                  | Validity | Corrected            |
|----------------------|----------|----------------------|
| rdf:type (a)         | X        | -                    |
| rdf:Property         | X        | -                    |
| rdfs:label           | X        | -                    |
| owl:Class            | X        | -                    |
| rdfs:domain          | X        | -                    |
| rdfs:range           | X        | -                    |
| xsd:integer          | X        | -                    |
| xsd:string           | X        | -                    |
| *Total*              | **8**    | **0**                |