# Mistral-7B

[Generated ontology](./ontology.txt)


## Errors

Incorrect serialization:
-   Incorrect use of shortnames and number of elements in the triplets. Example:
    ```
    :ProductId hasEntityNameValue rdf:id "ProductId" ;
        rdfs:domain :ProductId ;
        rdfs:range rdf:String .
    ```
-   Wrong URIs. Example: rdf:id


## URIs

| Prefix | URI                                           | Validity | Corrected                                   |
|--------|-----------------------------------------------|----------|---------------------------------------------|
| rdf    | http://www.w3.org/1999/02/22-rdf-syntax-ns/   | -        | http://www.w3.org/1999/02/22-rdf-syntax-ns# |
| rdfs   | http://www.w3.org/2000/01/rdf-schema/         | -        | http://www.w3.org/2000/01/rdf-schema#       |
| owl    | http://www.w3.org/2002/07/owl/                | -        | http://www.w3.org/2002/07/owl#              |
|        |                                               | **0**    | **3**                                       |


| URI                   | Validity | Corrected              |
|-----------------------|----------|------------------------|
| rdf:type (a)          | X        | -                      |
| owl:Class             | X        | -                      |
| rdfs:DatatypeProperty | -        | owl:DatatypeProperty   |
| rdfs:domain           | X        | -                      |
| rdfs:range            | X        | -                      | 
| rdfs:subPropertyOf    | X        | -                      |
| owl:hasValue          | X        | -                      |
| rdf:String            | -        | xsd:string             |
| rdf:id                | -        | :id                    |
| rdfs:propertyChain    | -        | owl:propertyChainAxiom |
| rdfs:property         | -        | rdf:Property           |
| rdf:Property          | X        | -                      |
| *Total*               | **7**    | **5**                  |

- Incorrect use of owl:hasValue