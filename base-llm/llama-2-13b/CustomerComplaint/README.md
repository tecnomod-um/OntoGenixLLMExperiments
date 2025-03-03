# Llama-2-13B

## Llama-2-13B-4bits

[Generated ontology](./4bits_ontology.txt)


### Errors

-   Incorrect format and serialization (shortnames, dots). Example: <br>
    class CompanyPublicResponse {
        owl:Class(CompanyPublicResponse)
        rdf:type owl:Class
        xsd:string text
        owl:oneOf(
            owl:NamedIndividual(CompanyPublicResponse)
        )
    }

-   Wrong URIs


## Llama-2-13B-8bits

[Generated ontology](./8bits_ontology.txt) 
<br>
[Corrected ontology](./8bits_ontology_corrected.txt)
<br>
![](./8bits_ontology_corrected.png)


### Errors

-   Uncommented text: <br>
    Here is the proposed ontology for the given JSON data in TURTLE syntax:

-   And loop at the end of the file: <br>
    <http://baseontology.com/Company> owl:hasValue <http://baseontology.com/non_null_count": 35699984167, "type": "text": "3", "3": "3" ...

-   Wrong URIs and used incorrectly.


### URIs

| Prefix | URI                                         | Validity | Corrected |
|--------|---------------------------------------------|----------|-----------|
| rdf    | http://www.w3.org/1999/02/22-rdf-syntax-ns# | X        | -         |
| owl    | http://www.w3.org/2002/07/owl#              | X        | -         |
| xsd    | http://www.w3.org/2001/XMLSchema#           | X        | -         |
|        |                                             | **3**    | **0**     |

| URI                | Validity | Corrected   |
|--------------------|----------|-------------|
| owl:Ontology       | X        | -           |
| owl:imports        | X        | -           |
| owl:Class          | X        | -           |
| owl:class          | -        | owl:Class   |
| owl:hasValue       | X        | -           |
| owl:ObjectProperty | X        | -           |
| owl:domain         | -        | rdfs:domain |
| owl:range          | -        | rdfs:range  |
| xsd:integer        | X        | -           |
| xsd:string         | X        | -           |
| xsd:boolean        | X        | -           |
| rdf:type (a)       | X        | -           |
| *Total*            | **9**    | **3**       |

-   owl:hasValue used incorrectly.
-   ObjectProperties and DatatypeProperties share the same URIs.



## Llama-2-13B without quantization

[Generated ontology](./all_ontology.txt)
<br>
[Corrected ontology](./all_ontology_corrected.txt)
<br>
![](./all_ontology_corrected.png)


### Errors

-   Incorrect serialization (number of elements and ending loop). Example: <br>
    <http://example.com/Company> owl:type owl:Class> , <br>
    ...
    <http://example.com/Company> owl:Class> , 
    <http://Company> owl:Class> , 
    <http://Company> , 
    ...
    
-   Uncommented text. Example: <br>
    Here is the TURTLE syntax for the proposed ontology:

-   Wrong URIs and incorrect use. Example: owl:has_value instead of owl:hasValue.

-   Statements duplicated. Example: <br>
    <http://example.com/CompanyPublicResponse> a owl:Class .
    <http://example.com/CompanyPublicResponse> rdf:type owl:Class .


### URIs

| Prefix | URI                                         | Validity | Corrected |
|--------|---------------------------------------------|----------|-----------|
| rdf    | http://www.w3.org/1999/02/22-rdf-syntax-ns# | X        | -         |
| owl    | http://www.w3.org/2002/07/owl#              | X        | -         |
| xsd    | http://www.w3.org/2001/XMLSchema#           | X        | -         |
|        |                                             | **3**    | **0**     |

| URI           | Validity | Corrected    |
|---------------|---------|---------------|
| rdf:type      | X       | -             |
| owl:Class     | X       | -             |
| owl:has_value | -       | owl:hasValue  |
| *Total*       | **2**   | **1**         |

- owl:hasValue used incorrectly.