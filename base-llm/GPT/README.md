# GPT model comparison

## Introduction
In this section we address the comparison of GPT models (GTP-3.5, GPT-4 and GPT-4o) in order to identify which model offers better results, and the main characteristics of each of them.

## Methodology
- Ontology building based on e-commerce CSVs with each GPT version (GPT-3.5, GPT-4 and GPT-4o). Three replicates per experiment to have also information about the reproducibility of the results.
- Datasets: [6 Kaggle datasets](https://github.com/jesualdotomasfernandezbreis/KGCF/blob/66d0dac8e32ff5671cd90b254394fbfafadb0dba/workpackages/WP1/Deliverables/D1.2/Datasets/README.md).
    -   Airlines Customer Satisfaction.
    -   Amazon Rating.
    -   BigBasket Products.
    -   Brazilian E-commerce.
    -   Customer Complaint.
    -   eCommerce.
- Comparison of generated ontologies with respect to [human-generated ontologies](https://github.com/jesualdotomasfernandezbreis/KGCF/tree/66d0dac8e32ff5671cd90b254394fbfafadb0dba/workpackages/WP1/Deliverables/D1.2/Datasets) (desired ontologies).

The files used to generate the ontologies are also included in the [datasets](../datasets/) folder.


## Results
These results allow us to identify which GTP version gives the best results. The ontologies generated are included in their corresponding folders:
-   Airlines Customer Satisfaction. [GPT-3.5](./AirlinesCustomerSatisfaction/3.5/), [GPT-4](./AirlinesCustomerSatisfaction/4/), [GPT-4o](./AirlinesCustomerSatisfaction/4o/).
-   Amazon Rating. [GPT-3.5](./AmazonRating/3.5/), [GPT-4](./AmazonRating/4/), [GPT-4o](./AmazonRating/4o/).
-   BigBasket Products. [GPT-3.5](./BigBasketProducts/3.5/), [GPT-4](./BigBasketProducts/4/), [GPT-4o](./BigBasketProducts/4o/).
-   Brazilian E-commerce. [GPT-3.5](./BrazilianE-commerce/3.5/), [GPT-4](./BrazilianE-commerce/4/), [GPT-4o](./BrazilianE-commerce/4o/).
-   Customer Complaint. [GPT-3.5](./CustomerComplaint/3.5/), [GPT-4](./CustomerComplaint/4/), [GPT-4o](./CustomerComplaint/4o/).
-   eCommerce. [GPT-3.5](./eCommerce/3.5/), [GPT-4](./eCommerce/4/), [GPT-4o](./eCommerce/4o/).

Below, to facilitate the interpretation of results, we provide summary tables of the patterns observed between datasets. We also divide this report by Classes, Object properties and Datatype properties.

**Note:** GPT-4 and GPT-4o were unified because they had similar patterns, although GPT-4o showed higher reproducibility, i.e. replicates were more similar between than in GPT-4o. 


### Executability

The following table shows with an X when the LLM model was able to generate the ontology in question with an appropiate syntax. We also include the total number of these ontologies:

| LLM model   | AirlinesCustomerSatisfaction | AmazonRating | BigBasketProducts | BrazilianE-commerce | CustomerComplaint | eCommerce | Total  |
|-------------|------------------------------|--------------|-------------------|---------------------|-------------------|-----------|--------|
| GPT-3.5     | X                            | X            | -                 | X                   | X                 | X         | 5      |
| GPT-4       | X                            | X            | X                 | X                   | X                 | X         | 6      |
| GPT-4o      | X                            | X            | X                 | X                   | X                 | X         | 6      |
| **Total**   | **3**                        | **3**        | **2**             | **3**               | **3**             | **3**     | **17** |


The following table shows the main errors made by LLM models in the generation of ontologies:

| LLM model | AirlinesCustomerSatisfaction | AmazonRating | BigBasketProducts                            | BrazilianE-commerce | CustomerComplaint | eCommerce |
|-----------|------------------------------|--------------|----------------------------------------------|---------------------|-------------------|-----------|
| GPT-3.5   | X                            | X            | Incorrect serialization (prefix not defined) | Wrong URIs          | X                 | X         |
| GPT-4     | Wrong URIs                   | X            | Wrong URIs                                   | X                   | Wrong URIs        | X         |
| GPT-4o    | Wrong URIs                   | X            | Wrong URIs                                   | X                   | Wrong URIs        | X         |


Below we include a new table with those ontologies that could be developed after a human intervention. These were the ontologies with serialization, and format errors, where a human intervention for correction implies a lower effort than a de novo development.

| LLM model | AirlinesCustomerSatisfaction | AmazonRating | BigBasketProducts | BrazilianE-commerce | CustomerComplaint | eCommerce | Total  |
|-----------|------------------------------|--------------|-------------------|---------------------|-------------------|-----------|--------|
| GPT-3.5   | X                            | X            | X                 | X                   | X                 | X         | 6      |
| GPT-4     | X                            | X            | X                 | X                   | X                 | X         | 6      |
| GPT-4o    | X                            | X            | X                 | X                   | X                 | X         | 6      |
| **Total** | 3                            | 3            | 3                 | 3                   | 3                 | 3         | 18     |



### Pattern in the design of Classes:

|                       | **GPT-3.5**                                                      | **GPT-4 and GPT-4o**                                                                                   |
|-----------------------|------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------|
| **Number of classes** | Each csv column usually derives into a specific class. <br>The existence of entities and associated attributes is not properly recognized. | Not all columns derive into classes. <br>The existence of different entities and attributes is better recognized. |
| **Hallucinations**    | High                                                             | Low                                                                                                    |
| **Enrichment**        | No external enrichment                                           | Entities are enriched with external resources, <br>but hierarchical relationships (subClassOf) are established rather than <br>equivalence relationships. <br>External entities are not always correct (properties as classes). |


### Pattern in the design of Object Properties:

|                        | **GPT-3.5**                                                         | **GPT-4 and GPT-4o**                                                                                            |
|------------------------|---------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------|
| **Number of OP**       | Trend to generate one OP for each column of the CSV, <br>linking a central entity to the rest of entities acting as <br>peripheral nodes (ontologies with star form). | There is no one OP for each column of the CSV. <br>Better recognition of relationships between entities, <br>and distinction between OP and DP. | There is no one OP for each column of the CSV. <br>Better recognition of relationships between entities, and distinction between OP and DP. |
| **Domain and range**   | Not always defined, and not always coherent: not always <br>connect all entities (isolated entities). | Typically defined, but not always coherent. | 
| **Hallucinations**     | Low                             | Low                        |
| **Enrichment**         | No external enrichment.         | Properties enriched with external resources, <br>but with hierarchical relationships (subClassOf) rather than <br>equivalence relationships. |


### Pattern in the design of Datatype Properties:

|                        | **GPT-3.5**                                                   | **GPT-4 and GPT-4o**                                                                                   |
|------------------------|---------------------------------------------------------------|--------------------------------------------------------------------------------------------------------|
| **Number of DP**       | Two typical situations: (1) One DF for each column of <br>the CSV to link the attribute (string/number) to its entity. <br>(2) Incorrect DPs with statistical values from data preprocessing. | One DP for each column of the CSV to link the attribute (string/number) to its entity.      |
| **Domain and range**   | Not always defined, and not always coherent.                  | Typically defined, but not always coherent.                                                            |
| **Hallucinations**     | Low                                                           | Low                                                                                                    |
| **Enrichment**         | No external enrichment                                        | Properties enriched with external resources, <br>but with hierarchical relationships (subClassOf) rather than <br>equivalence relationships. |


### Similarity with human gold standard

Next, we indicate which GTP model presents results closer to the human gold standard:

| **Dataset**                       | **GPT-3.5** | **GPT-4** | **GPT-4o** |
|-----------------------------------|-------------|-----------|------------|
| Airlines Customer Satisfaction    |             |           |     X      |
| Amazon Rating                     |             |     X     |     X      |
| BigBasket Products                |             |     X     |            |
| Brazilian E-commerce              |             |     X     |            |
| Customer Complaint                |             |           |     X      |
| eCommerce                         |             |     X     |            |

Sometimes two models are marked. This is because the generated schemas are similar between the two models. This is the case with Amazon Rating.


## Valorations

- GPT-4 and GPT-4o generate ontologies with a design more similar to the manually generated ontology, being the results with GTP-4 slightly better.
- GPT-4 and GPT-4o tend to generate similar ontologies within the inherent variability of the methods. However, the cost per token is lower in GPT4o, making it more cost-effective to use.
- In addition, GPT-4o has a higher reproducibility than GPT4, and this reproducibility is higher when CSVs are not highly complex (many columns).


## Limitations

- Although GPT-4o is the best performing method with respect to cost per token, it still has problems in detecting the internal structure of the files.
- Need to emphasize tasks indicated in the workflow that the LLM tends to omit or does not follow strictly.
- The model is not yet able to build appropriate hierarchical relationships and enrichments with external entities.


Proposals to resolve the found limitations:
-   Emphasize that the input CSV data correspond to attributes of entities that OntoGenix must model. Not every column corresponds to a different entity, so not every column needs to derive in an entity and an object property.
-   Emphasize that all properties must have a range and a domain.
-   Preprocessing values from the feature vector should never be included in the schema.
-   The use of external entities should be used to generate equivalence relationships.
