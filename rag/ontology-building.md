# RAG experiments for ontology building

## Objective
The goal of these experiments is to study the contribution of the **Retrival-Augmented Generation** (RAG) process to the ontology building capabilities of the LLM models. 

## The RAG process
In RAG, the model is provided with files to use as a reference for the queries. In this case, some ontologies are made available to the model to serve as references that the model will consult to accurately translate a given CSV file into an ontology. 


## The RAG GPT models

### GPT-builder (GPT-4)
Due to the limitations of the API regarding file upload formats, the RAG process will be tested using the GPT-builder tool instead. This tool, available on the OpenAI website, is currently powered by GPT-4 and supports the use of the Turtle format, which is necessary for uploading various ontology files. These ontology files will serve as references that the model will consult to accurately translate a given CSV file into an ontology.

### RAG through OpenAI API (GPT-4o)
Using OpenAI's API, the RAG process is performed through an **assistant agent**. Assistants can call OpenAI’s models with specific instructions to tune their personality and capabilities and can also access multiple tools in parallel, like the File Search tool. The **File Search tool** augments the Assistant with knowledge from outside its model, such as proprietary product information or documents provided by your users.

In this case, the assistant will use the **GPT-4o model** and five ontologies will be provided as a reference for the ontology-building task. So, when the model is asked to translate a CSV file to an ontology, it will consult the ontologies of reference to understand the structure of an ontology.

<p align="center">
  <img width="586" alt="image" src="https://github.com/user-attachments/assets/419e90f7-e802-4c3a-88ea-f742bda65a58" />
</p>

The steps to perform the RAG process are as follows:

**1. Create an assistant with the File Search tool enabled.**
  * An assistant is a purpose-built AI that uses OpenAI’s models and calls tools.
  * File Search is a tool that augments the Assistant with knowledge from outside its model, such as proprietary product information or documents provided by your users.
  * Once the file_search tool is enabled, the model decides when to retrieve content based on user messages.
    
**2. Make the files available for the assistant.**
  * Create a vector store.
  * Upload the files.
  * Add the files to the vector store.
  * Update the assistant with the new vector store.
    
**3. Launch the query (translate CSV file into an ontology) using the assistant.**

Additionally, six datasets related to commercial activities (Airlines, Amazon, Brazilian, BigBasket, Consumer, and E-commerce) will be used as test data to evaluate the ontology construction of the ragged model.

#### Limitations of the RAG process using the OpenAI API
* The maximum file size is **512 MB**. 
* Each file should contain no more than **2 million tokens per file** (computed automatically when you attach a file).
* Each vector_store can hold up to **10,000 files**.
* You can attach **at most one vector store** to an assistant.


### Evaluation of the RAG models

The capacity of the RAG models to create the ontologies are tested using **six datasets** related to commercial activities:

* Airlines
* Amazon
* Brazilian
* BigBasket
* Consumer
* E-commerce


### Findings
* The ontologies obtained with the RAG process are more concise than the base model using the prompt, that is, the redundancy observed with the base model is solved.
* The RAG process is the best or one of the best methods for the ontology-building process.
