# Fine-tuning experiments for ontology population

##  Objective

Explore the capabilities of a fine-tuned model using a specific ontology of interest and compare it to a baseline model that directly integrates this ontology into its prompt. The goal is to perform ontology population, which involves updating an ontology with new facts extracted from an input knowledge resource. To achieve this, each line of a CSV file is translated into an RDF graph that aligns with the ontology of interest.


##  The fine-tuning process

The two approaches are explained below:
* **Through prompt**: The complete ontology is included in the prompt in turtle format, as the model is able to understand ontologies in RDF, RDFS and OWL. 
There is a considerable **token cost** in the system prompt, as the full ontology must be included for each piece of unstructured text at the user prompt.
* **Fine-tuning process**: Train the model with pairs unstructured text-KG where the KG conforms to the ontology of interest. It is like showing the model's use cases.
The system prompt can be very concise, so most of the token cost comes from the unstructured text to be transformed.

In this case, for the fine-tuning process, the LLM model GPT-4o is asked to build the **training dataset** in the JSONL format, generating 187 examples (pairs unstructured text-KG) corresponding to the custom ontology. 
Here is one of the examples, where "um:" corresponds to the prefix of our ontology of interest:
```
{"messages": [
  {"role": "system", "content": "Translate the user text to an RDF graph using the country1 ontology."}, 
  {"role": "user", "content": "The country with abbreviation 'USA' has its capital in Washington, D.C."}, 
  {"role": "assistant", "content": "<http://example.com/USA> rdf:type um:Country; 
                                      um:hasAbbreviation 'USA'; 
                                      um:hasCapital 'Washington, D.C.'."}
]}
```
Of the training dataset containing 187 pairs of unstructured text and their corresponding knowledge graph corresponding to the custom ontology:
* 144 pairs will be used for training.
* The remaining 43 pairs will be reserved for validation.


## The fine-tuned models

### GPT-4o-mini model

The **GPT-4o-mini model** is trained using the training dataset to learn how to use a specific ontology. 

First, the training and validation data are transformed into the JSONL format required by the OpenAI model to perform the fine-tuning task. This message format consists of three roles: 
* **system**, to indicate the function the model will perform.
* **user**, to indicate the prompt of the task to be performed.
* **assistant**, to indicate the output that the model should display.

Next, using the API provided by OpenAI, the training and validation data are uploaded to the OpenAI platform, and the fine-tuning job is launched with the following hyperparameters:
* n_epochs = 3.
* batch_size = 3.
* learning_rate_multiplier = 0.3.


## Evaluation of the fine-tuned models

In this experiment, an ontology about countries is used as the ontology of interest. Additionally, a dataset containing information on various countries will be used as **test data** to evaluate the fine-tuned model's ability to utilize the new ontology of interest. For this evaluation, only the first three lines of the dataset will be used. 



## Findings
* Instruct the model to use a specific ontology of interest through the prompt fits perfectly with the ontology of interest, not including new classes or properties. However, some of the information contained in the text is lost.
* Instruct the model to use a specific ontology of interest through a fine-tuning process, the fine-tuned model tends to create new properties that do not exist in the ontology of interest, gathering more information from the text. This could be useful for updating the ontology with new information.

