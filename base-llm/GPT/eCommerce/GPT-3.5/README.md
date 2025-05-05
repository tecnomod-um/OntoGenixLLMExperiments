# GPT-3.5

[Generated ontology](./ontology.ttl)
<br>
![](./ontology.png)
<br>
[Corrected ontology](./ontology_corrected.ttl)
<br>
![](./ontology_corrected.png)


## [Errors](./ontology_notes.txt)

Ontology without syntax errors, but semantic errors because Datatype properties are declarated as Object properties. Example:
```
base:hasNonNullCount rdf:type owl:ObjectProperty ;
    rdfs:domain base:Country ;
    rdfs:range xsd:float .
```


## [URIs](./ontology_URIs.xlsx)

| Prefix  | URI                                         | Validity | Corrected |
|---------|---------------------------------------------|----------|-----------|
| rdf     | http://www.w3.org/1999/02/22-rdf-syntax-ns# | X        | -         |
| rdfs    | http://www.w3.org/2000/01/rdf-schema#       | X        | -         |
| owl     | http://www.w3.org/2002/07/owl#              | X        | -         |
| xsd     |	http://www.w3.org/2001/XMLSchema#           | X        | -         |
|         |                                             | **4**    | **0**     |


| URI                      | Validity | Corrected |
|--------------------------|----------|-----------|
| rdf:type (a)             | X        | -         |
| owl:Class                | X        | -         |
| owl:ObjectProperty       | X        | -         |
| rdfs:domain              | X        | -         |
| rdfs:range               | X        | -         |
| xsd:float                | X        | -         |
| xsd:string               | X        | -         |
| **Total**                | **7**    | **0**     |
