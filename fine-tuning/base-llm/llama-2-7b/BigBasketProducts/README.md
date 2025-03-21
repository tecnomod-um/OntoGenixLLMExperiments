# Llama-7B

## Llama-7B-4bits

[Generated ontology](./ontology_4bits.txt)
<br>
[Corrected ontology](./ontology_4bits_corrected.txt)
<br>
![](./ontology_4bits_corrected.png)


### [Errors](./ontology_4bits_notes.txt)

**Incorrect serialization** due to:

-   Incorrect use of dots instead of semicolons:
    ```
    um:ProductLinks a rdf:Property ;
        rdfs:domain um:Product .
        rdfs:range xsd:string .
        rdfs:label "Product Links" .
    ```

-   Incorrect IDs. Example: subProperty of instead of subPropertyOf
    ```
    um:ProductLinksToProductNameLinks a rdf:Class ;
    rdfs:subProperty of um:ProductLinksToProductName .
    ```


### [URIs](./ontology_4bits_URIs.xlsx)

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
| rdf:Class            | -        | owl:Class            |
| rdfs:label           | X        | -                    |
| rdf:Property         | X        | -                    |
| rdfs:domain          | X        | -                    |
| rdfs:range           | X        | -                    |
| rdfs:subProperty     | -        | rdfs:subPropertyOf   |
| xsd:string           | X        | -                    |
| *Total*              | **6**    | **2**                |


## Llama-7B-8bits

[Generated ontology](./ontology_8bits.txt)
<br>
[Corrected ontology](./ontology_8bits_corrected.txt)
<br>
![](./ontology_8bits_corrected.png)


### [Errors](./ontology_8bits_notes.txt)

Ontology without syntax errors.


### [URIs](./ontology_8bits_URIs.xlsx)

| Prefix | URI                                           | Validity | Corrected |
|--------|-----------------------------------------------|----------|-----------|
| rdf    | http://www.w3.org/1999/02/22-rdf-syntax-ns#   | X        | -         |
| rdfs   | http://www.w3.org/2000/01/rdf-schema#         | X        | -         |
| owl    | http://www.w3.org/2002/07/owl#                | X        | -         |
| xsd    | http://www.w3.org/2001/XMLSchema#             | X        | -         |
|        |                                               | **4**    | **0**     |


| URI                  | Validity | Corrected            |
|----------------------|----------|----------------------|
| owl:Ontology         | X        | -                    |
| rdf:type (a)         | X        | -                    |
| owl:Class            | X        | -                    |
| rdfs:label           | X        | -                    |
| rdfs:domain          | X        | -                    |
| rdfs:range           | X        | -                    |
| owl:DatatypeProperty | X        | -                    |
| owl:ObjectProperty   | X        | -                    |
| xsd:string           | X        | -                    |
| xsd:integer          | X        | -                    |
| xsd:decimal          | X        | -                    |
| *Total*              | **11**   | **0**                |


## Llama-7B-without quantization

[Generated ontology](./ontology_all.txt)
<br>
![](./ontology_all.png)


### [Errors](./ontology_all_notes.txt)

Ontology without syntax errors.


### [URIs](./ontology_all_URIs.xlsx)

| Prefix | URI                                           | Validity | Corrected |
|--------|-----------------------------------------------|----------|-----------|
| rdf    | http://www.w3.org/1999/02/22-rdf-syntax-ns#   | X        | -         |
| rdfs   | http://www.w3.org/2000/01/rdf-schema#         | X        | -         |
| owl    | http://www.w3.org/2002/07/owl#                | X        | -         |
| xsd    | http://www.w3.org/2001/XMLSchema#             | X        | -         |
|        |                                               | **4**    | **0**     |

| URI                  | Validity | Corrected            |
|----------------------|----------|----------------------|
| owl:Ontology         | X        | -                    |
| rdf:type (a)         | X        | -                    |
| owl:Class            | X        | -                    |
| rdfs:label           | X        | -                    |
| rdfs:domain          | X        | -                    |
| rdfs:range           | X        | -                    |
| owl:DatatypeProperty | X        | -                    |
| owl:ObjectProperty   | X        | -                    |
| xsd:string           | X        | -                    |
| xsd:decimal          | X        | -                    |
| xsd:date             | X        | -                    |
| *Total*              | **11**   | **0**                |