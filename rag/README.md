# RAG experiments
## Ontology building
Study the ontology-building capabilities of the **Retrival-Augmented Generation** (RAG) process, where the model is provided with files to use as a reference for future queries. In this case, some ontologies are made available to the model to serve as references that the model will consult to accurately translate a given CSV file into an ontology.
***
### GPT models
Due to the limitations of the API regarding file upload formats, the RAG process will be tested using the GPT-builder tool instead. This tool, available on the OpenAI website, is currently powered by GPT-4 and supports the use of the Turtle format, which is necessary for uploading various ontology files. These ontology files will serve as references that the model will consult to accurately translate a given CSV file into an ontology.

**The implementation of RAG via API is still pending.**
### Findings
* Similar results are obtained in both the RAG and fine-tuning processes. In both cases the ontologies are more concise than the base model using the prompt, that is, the redundancy observed with the base model is solved.
***
## Ontology population - Instruct the model to use a specific ontology of interest
Explore the capabilities of a RAG process using a specific ontology of interest and compare it to a baseline model that directly integrates this ontology into its prompt. The goal is to perform ontology population, which involves updating an ontology with new facts extracted from an input knowledge resource. To achieve this, each line of a CSV file is translated into an RDF graph that aligns with the ontology of interest.

### GPT models
As in the other experiment, the RAG process will be tested using the GPT-builder tool. The ontology of interest is made available to the model to use it to translate each line of the CSV file to an RDF graph that conforms to the ontology of interest.

**The implementation of RAG via API is still pending.**
### Findings
* Instruct the model to use a specific ontology of interest through an RAG process, which allows the model to use the properties of the ontology of interest adequately (without creating new ones). However, it only uses one class of the ontology, ignoring the others. Nor does it create new classes.

