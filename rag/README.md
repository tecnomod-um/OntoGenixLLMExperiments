# RAG experiments
## Ontology building
Study the ontology-building capabilities of the **Retrival-Augmented Generation** (RAG) process, where the model is provided with files to use as a reference for future queries. In this case, some ontologies are made available to the model to serve as references that the model will consult to accurately translate a given CSV file into an ontology.
***
### GPT models
Due to the limitations of the API regarding file upload formats, the RAG process will be tested using the GPT-builder tool instead. This tool, available on the OpenAI website, is currently powered by GPT-4 and supports the use of the Turtle format, which is necessary for uploading various ontology files. These ontology files will serve as references that the model will consult to accurately translate a given CSV file into an ontology.

Using OpenAI's API, the RAG process is performed through an **assistant agent**. Assistants can call OpenAI’s models with specific instructions to tune their personality and capabilities and can also access multiple tools in parallel, like the File Search tool. The **File Search tool** augments the Assistant with knowledge from outside its model, such as proprietary product information or documents provided by your users.

In this case, the assistant will use the **GPT-4o model** and five ontologies will be provided as a reference for the ontology-building task. So, when the model is asked to translate a CSV file to an ontology, it will consult the ontologies of reference to understand the structure of an ontology.

<img width="586" alt="image" src="https://github.com/user-attachments/assets/419e90f7-e802-4c3a-88ea-f742bda65a58">

### Findings
* The ontologies obtained with the RAG process are more concise than the base model using the prompt, that is, the redundancy observed with the base model is solved.
* The RAG process is the best or one of the best methods to carry out the ontology-building process.
***
## Ontology population - Instruct the model to use a specific ontology of interest
Explore the capabilities of a RAG process using a specific ontology of interest and compare it to a baseline model that directly integrates this ontology into its prompt. The goal is to perform ontology population, which involves updating an ontology with new facts extracted from an input knowledge resource. To achieve this, each line of a CSV file is translated into an RDF graph that aligns with the ontology of interest.

In this experiment, an ontology about countries is used as the ontology of interest. The CSV file utilized for the ontology population contains information about various countries around the world. Since the CSV is large and we aim to conduct a pilot experiment, we will use information from only three countries (three lines of the CSV).

### GPT models
As in the other experiment, the RAG process will be tested using the GPT-builder tool. The ontology of interest is made available to the model to use it to translate each line of the CSV file to an RDF graph that conforms to the ontology of interest.

**The implementation of RAG via API is still pending.**
### Findings
* Instruct the model to use a specific ontology of interest through an RAG process, which allows the model to use the properties of the ontology of interest adequately (without creating new ones). However, it only uses one class of the ontology, ignoring the others. Nor does it create new classes.

