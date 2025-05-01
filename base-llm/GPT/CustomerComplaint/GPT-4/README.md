# GPT-4

[Generated ontology](./ontology.owl)
<br>
![](./ontology.png)


## [Errors](./ontology_notes.txt)

Ontology without syntax errors, but semantic errors. For example, schema:identifier and dcterms:date are properties, but are used as range of Object properties.

Also wrong URIs. For examples: dcterms:date.


## [URIs](./ontology_URIs.xlsx)

| Prefix  | URI                                         | Validity | Corrected |
|---------|---------------------------------------------|----------|-----------|
| rdf     | http://www.w3.org/1999/02/22-rdf-syntax-ns# | X        | -         |
| rdfs    | http://www.w3.org/2000/01/rdf-schema#       | X        | -         |
| owl     | http://www.w3.org/2002/07/owl#              | X        | -         |
| xsd     |	http://www.w3.org/2001/XMLSchema#           | X        | -         |
| skos	  | http://www.w3.org/2004/02/skos/core#        | X        | -         |
| foaf    |	http://xmlns.com/foaf/0.1/                  | X        | -         |
| dcterms |	http://purl.org/dc/terms/                   | X        | -         |
| schema  |	http://schema.org/                          | X        | -         |
|         |                                             | **8**    | **0**     |


| URI                      | Validity | Corrected       |
|--------------------------|----------|-----------------|
| rdf:type (a)             | X        | -               |
| owl:Class                | X        | -               |
| owl:ObjectProperty       | X        | -               |
| rdfs:domain              | X        | -               |
| rdfs:range               | X        | -               |
| schema:Organization      | X        | -               |
| foaf:Person              | X        | -               |
| schema:Product           | X        | -               |
| skos:Concept             | X        | -               |
| schema:ProductModel      | X        | -               |
| schema:ReplyAction       | X        | -               |
| schema:Article           | X        | -               |
| schema:Boolean           | X        | -               |
| dcterms:date             | X        | -               |
| schema:State             | X        | -               |
| schema:PostalCode        | X        | base:PostalCode |
| schema:identifier        | X        | -               |
| schema:keywords          | X        | -               |
| schema:CreativeWork      | X        | -               |
| **Total**                | **18**   | **1**           |
