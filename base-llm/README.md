# Experiments with base openLLMs

## Objective

The objective of these experiments is to study the ontology generation capacity of different base openLLMs


## The approach

The aim of this experiment is to use the OntoGenix approach and the the defined [OntoGenix](https://github.com/tecnomod-um/OntoGenix_BASF/tree/main/GUI) prompts, but changing the generation engine. Instead of GPT-4, an opensource LLM is used for high-level description generation, ontology generation and ontology mapping to YML format in each experiment

All the experiments used the same generation parameters for different LLMs to ensure comparability of results and to fairly assess the performance of each model under similar conditions. 

The generation parameters are: 

- top_p=0.8: The value of top_p controls the probabilistic sampling in text generation. A value of 0.8 allows for more diversity in the generation by restricting the sampling to a relevant subset of words, preventing the model from becoming too predictable or choosing words that are too unlikely.
- top_k=40: The value of top_k limits the number of candidate words from which the model can choose. This value reduces the possibility of selecting low probability words, which helps to control the consistency and quality of the generated text. Therefore, a value of 40 allows for sufficient diversity without making the generation too random.
- temperature=0.5: Temperature adjusts the level of ‘creativity’ of the model. A lower temperature (close to 0) makes the model more conservative and chooses the most likely options, while a higher temperature (close to 1 or more) makes it more likely to explore less likely options. Thus, a value of 0.5 balances creativity and accuracy, providing coherent and sensible answers without the text being monotonous or too predictable.
- max_new_tokens=4096: This parameter defines the maximum number of tokens.  A limit of 4096 is relatively large and allows the model to generate long or continuous responses without truncating the text.

## Experiments by openLLM

For each LLM, we have evaluated a series of Kaggle datasets related to commercial activities of organizations (Airlines, Amazon, Brazilian, BigBasket, Consumer, and E-commerce), which are the same as those evaluated in the [Ontogenix Evaluation](https://github.com/tecnomod-um/OntoGenixEvaluation) project (without ontology quality analysis which will come later).

* [LLama-2-7b](./llama-2-7b/README.md): The ontologies generated from this model of different datasets are available in the [LLama-2-7b ontologies directory](./llama-2-7b).
* [LLama-2-70b](./llama-2-70b/README.md): The ontologies generated from this model of different datasets are available in the [LLama-2-70b ontologies directory](./llama-2-70b).
* [LLama-3-8b](./llama-3-8b/README.md): The ontologies generated from this model of different datasets are available in the [LLama-3-8b ontologies directory](./llama-3-8b).
* [LLama-3-70b](./llama-3-70b/README.md): The ontologies generated from this model of different datasets are available in the [LLama-3-70b ontologies directory](./llama-3-70b).
* [Mistral-7b](./mistral-7b/README.md): The ontologies generated from this model of different datasets are available in the [Mistral-7b ontologies directory](./Mistral-7b).
* [Mixtral](./mixtral/README.md): The ontologies generated from this model of different datasets are available in the [Mixtral ontologies directory](./Mixtral). 

## Summary of the findings

- The Mixtral, Mistral and Llama-2 family models produce numerous hallucinations and generate response that do not align with the standardized format specified in the prompt. Therefore, we discarded them for detailed analysis. 
- The Llama-3 family was trained on over 15 trillion tokens, resulting in fewer hallucinations and generally aligning with the standardized format defined in the prompt. 
- Main limitations include the tendency of the latest open-source LLMs used as ontology generation engines to produce hallucinations and deviate from the prompt's defined standardization, as well as the difficulty in evaluating the generated ontologies.
- Proposed solutions to address the identified limitations include fine-tuning LLMs to model new data within the same domain of interest and in a specified format, and implementing a RAG (Retrieval-Augmented Generation) architecture with sample ontologies and schemas stored in a vector database.

The following table shows with an X when the LLM model was able to generate the ontology in question with an appropiate syntax. We also include the total number of these ontologies:

| LLM model         | AirlinesCustomerSatisfaction | AmazonRating | BigBasketProducts | BrazilianE-commerce | CustomerComplaint | eCommerce | Total |
|-------------------|------------------------------|--------------|-------------------|---------------------|-------------------|-----------|-------|
| Llama-2-7b        | -                            | -            | -                 | -                   | -                 | -         | 0     |
| Llama-2-13b-4bits | -                            | -            | -                 | -                   | -                 | -         | 0     |
| Llama-2-13b-8bits | -                            | -            | -                 | -                   | -                 | -         | 0     |
| Llama-2-13b-all   | -                            | -            | -                 | -                   | -                 | -         | 0     |
| Llama-2-70b       | -                            | -            | -                 | -                   | -                 | -         | 0     |
| Llama-3-8b-4bits  | -                            | -            | -                 | X                   | -                 | -         | 1     |
| Llama-3-8b-8bits  | -                            | X            | -                 | -                   | -                 | -         | 1     |
| Llama-3-8b        | -                            | -            | -                 | -                   | -                 | -         | 0     |
| Llama-3-70b       | -                            | -            | X                 | X                   | -                 | X         | 3     |
| Mistral-7b        | -                            | -            | -                 | -                   | -                 | -         | 0     |
| Mixtral           | -                            | -            | -                 | -                   | X                 | -         | 1     |
| **Total**         | **0**                        | **1**        | **1**             | **2**               | **1**             | **1**     | **6** |


The following table shows the main errors made by LLM models in the generation of ontologies:

| LLM model         | AirlinesCustomerSatisfaction                         | AmazonRating                                                | BigBasketProducts                                        | BrazilianE-commerce                                      | CustomerComplaint                                       | eCommerce                                               |
|-------------------|------------------------------------------------------|-------------------------------------------------------------|----------------------------------------------------------|----------------------------------------------------------|---------------------------------------------------------|---------------------------------------------------------|
| Llama-2-7b        | Incorrect format                                     | Incorrect format, and uncommented text                      | Incorrect format, and uncommented text                   | Incorrect format, and uncommented text                   | Incorrect format, and uncommented text                  | Incorrect format, and uncommented text                  |
| Llama-2-13b-4bits | Incorrect serialization (number of elements, loop at the end, and wrong URIs) | Incorrect format and serialization (shortnames, IDs and dots) | Incorrect serialization (number of elements in the triples, and wrong URIs) | Incorrect format and serialization (number of elements, shortnames and dots), and uncommented text | Incorrect format and serialization (shortnames, dots, URIs) | Incorrect format and serialization (number of elements, shortnames, and dots), and wrong URIs |
| Llama-2-13b-8bits | Incorrect format and serialization (number of elements in the triples, ending loop, and wrong URIs), and uncommented text | Uncommented text | Uncommented text and wrong URIs | Incorrect format and serialization (shortnames, dots, URIs), and uncommented text | Incorrect serialization (loop at the end), and uncommented text | Incorrect serialization (number of elements, shortnames, and dots), uncommented text, and wrong URIs |
| Llama-2-13b       | Incorrect format                                     | Incorrect serialization (number of elements in the triples) and uncommented text | Incorrect serialization (number of elements, shortnames, dots), and uncommented text | Incorrect serialization (number of elements, shortnames and dots), and uncommented text | Incorrect serialization (number of elements and ending loop), and uncommented text | Incorrect serialization (number of elements, shortnames, and dots), and uncommented text |
| Llama-2-70b       | Incorrect serialization (loop, shortnames, IDs, and numeric values) | Incorrect format, and uncommented text | Incorrect format, and uncommented text | Incorrect format, and uncommented text | Incorrect format, and uncommented text  | Incorrect format, and uncommented text |
| Llama-3-8b-4bits  | Incorrect rdf/xml serialization                      | Incorrect format and serialization (number of elements, and dots) | Incorrect serialization (missing end dots in the prefix declarations) | X | Incorrect rdf/xml serialization   | Incorrect serialization (dots) |
| Llama-3-8b-8bits  | Incorrect serialization (number of elements)         | X                                                           | Incorrect serialization (number of elements and dots)    | Incorrect serialization (dots, prefix used but not defined) | Incorrect serialization (shortnames) | Incorrect serialization (missing end dots in the prefix declarations) |
| Llama-3-8b        | Incorrect serialization (shortnames)                 | Incorrect serialization (missing end dots in the prefix declarations) | Incorrect serialization (dots) | Incorrect rdf/xml serialization | Incorrect serialization (dots, and shortnames) | Incorrect rdf/xml serialization |
| Llama-3-70b       | Incorrect serialization (dots, prefix and owl:Ontology declarations), and uncommented text | Incorrect serialization (blank nodes declarations) | X | X | Uncommented text, and prefix used but not declared | X |
| Mistral-7b        | Incorrect serialization (prefix not defined)         | Incorrect format and serialization (shortnames, wrong URIs, and number of elements in the triples) | Incorrect serialization (missing end dots, prefix not defined, syntax error) | Incorrect serialization (shortnames, and wrong URIs) | Incorrect format and serialization (number of elements in the triples, IDs with spaces, and wrong URIs) | Incorrect serialization (number of elements, dots, shortnames, wrong URIs, prefix used but not declared) |
| Mixtral           | Uncommented text                                     | Incorrect serialization (restrictions)                      | Incorrect format                                         | Incorrect serialization (prefix declarations, number of elements, use of shortnames) | X | Incorrect serialization (number of elements, shortnames, dots, prefix declarations, wrong IDs) |


We talk about:
- 'Incorrect format' when the model returns a serialization of RDF triples that does not correspond to the requested turtle, or other alternative ontology serialization format. Instead, it returns another inappropriate format that cannot be converted, i.e., the result generates an output that does not pass the validation tests, and therefore cannot be converted to a different type of RDF serialization. These errors were not corrected in most cases due to the incomprehensible output or the relatively high effort required by the user, based on the size of the ontology.
- 'Incorrect serialization' when the model returns a turtle serialization, but contains syntax errors that hinder the validation of the ontology. The type of the error is included in brackets. some of these errors can be corrected manually with relatively little effort, depending on the size of the ontology.
- 'Uncommented text' when the model does not return only the requested ontology, but includes text messages that are not properly included as comments. This result also prevents the validation of the ontology. These errors can be corrected easily
- 'Incorrect rdf/xml serialization' when the model returns an ontology with incorrect rdf/xml serialization instead of turtle. These errors were not corrected.

Errors associated with incorrect serialization are usually common, being:
- Incorrect number of elements in a triplet (2 or more than 3). When the triplet includes two elements it is because the model omits the property rdf:type (a). When the triplet has more than 3 elements, it is typically due to an inadequate concatenation of statements, inclusion of redundancies ( repeating the type of entity: Class, ObjectProperty, DatatypeProperty) or wrong syntax constraints/axioms.
- Loop at the end: the model is not able to finalize the ontology and includes random characters, or repeats a triplet or a fragment of it.
- Shortnames: shortnames without the prefix (only ID is included).
- IDs: lack of IDs, only the prefix is included. It is the inverse error of the previous one.
- Dots: mistakes in the ending dots. This includes lack of dots and/or semicolons at the end of statements, or an inappropriate use ( dot instead of semicolon). 
- Prefix: prefix used but not declarated.
- Wrong URIs: incorrect or inexistent URIs when a certain vocabulary such as rdf, rdfs, owl or xsd is reused. Inappropriate uses of resources are also frequent.

Below we include a new table with those ontologies that could be developed after a human intervention. These were the ontologies with serialization, and format errors, where a human intervention for correction implies a lower effort than a de novo development.

| LLM model         | AirlinesCustomerSatisfaction | AmazonRating | BigBasketProducts | BrazilianE-commerce | CustomerComplaint | eCommerce | Total |
|-------------------|------------------------------|--------------|-------------------|---------------------|-------------------|-----------|-------|
| Llama-2-7b        | -                            | -            | -                 | -                   | -                 | -         | 0     |
| Llama-2-13b-4bits | X                            | -            | X                 | X                   | -                 | -         | 2     |
| Llama-2-13b-8bits | -                            | X            | X                 | -                   | X                 | X         | 4     |
| Llama-2-13b       | -                            | X            | X                 | X                   | X                 | X         | 5     |
| Llama-2-70b       | X                            | -            | -                 | -                   | -                 | -         | 1     |
| Llama-3-8b-4bits  | -                            | -            | X                 | X                   | -                 | X         | 3     |
| Llama-3-8b-8bits  | X                            | X            | X                 | X                   | X                 | X         | 6     |
| Llama-3-8b        | X                            | X            | X                 | -                   | X                 | -         | 4     |
| Llama-3-70b       | X                            | X            | X                 | X                   | X                 | X         | 6     |
| Mistral-7b        | X                            | -            | X                 | X                   | -                 | X         | 4     |
| Mixtral           | X                            | X            | -                 | X                   | X                 | X         | 5     |
| *Total*           | **7**                        | **6**        | **8**             | **6**               | **6**             | **7**     | **40**|
