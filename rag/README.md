# RAG experiments
## Ontology building
Study the ontology-building capabilities of the **Retrival-Augmented Generation** (RAG) process, where the model is provided with files to use as a reference for future queries. 
***
### RAG
Due to the limitations of the API regarding file upload formats, the RAG process will be tested using the GPT-builder tool instead. This tool, available on the OpenAI website, supports the use of the Turtle format, which is necessary for uploading various ontology files. These ontology files will serve as references that the model will consult to accurately translate a given CSV file into an ontology.
### Findings
* In both the RAG and fine-tuning processes, similar results are obtained. In both cases the ontologies are more concise than the base model using the prompt, that is, the redundancy observed with the base model is solved.
