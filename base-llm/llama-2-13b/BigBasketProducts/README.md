# Llama-2-13B

## Llama-2-13B-4bits

[Generated ontology](./4bits_ontology.txt)
[Corrected ontology](./4bits_ontology_corrected.txt)
![](./4bits_ontology_corrected.png)

### Errors

-   Incorrect serialization (number of elements in the triples). Example:
    <http://base_ontology.com/class_entity> owl:hasValue <http://base_ontology.com/Absolute_Url_idx> "count" ;

-   Wrong URIs and inappropriate reuse. Examples: owl:domain and owl:ranges, and the use of owl:inverseOf.


### URIs

| Prefix | URI                                           | Validity | Corrected |
|--------|-----------------------------------------------|----------|-----------|
| rdf    | http://www.w3.org/1999/02/22-rdf-syntax-ns#   | X        | -         |
| owl    | http://www.w3.org/2002/07/owl#                | X        | -         |
| xsd    | http://www.w3.org/2001/XMLSchema#             | X        | -         |
|        |                                               | **3**    | **0**     |

| URI                | Validity | Corrected   |
|--------------------|----------|-------------|
| owl:Class          | X        | -           |
| owl:inverseOf      | X        | -           |
| owl:ObjectProperty | X        | -           |
| owl:domain         | -        | rdfs:domain |
| owl:range          | -        | rdfs:range  |
| rdf:type (a)       | X        | -           |
| xsd:string         | X        | -           |
| *Total*            | **5**    | **2**       |

owl:inverseOf used in an inappropriate way.
<http://base_ontology.com/entity_name> and <http://base_ontology.com/data_type> used as nodes and properties.


## Llama-2-13B-8bits

[Generated ontology](./8bits_ontology.txt)
[Corrected ontology](./8bits_ontology_corrected.txt)
![](./8bits_ontology_corrected.png)

### Errors



### URIs







## Llama-2-13B without quantization

[Generated ontology](./all_ontology.txt)
[Corrected ontology](./all_ontology_corrected.txt)
![](./all_ontology_corrected.png)

### Errors

