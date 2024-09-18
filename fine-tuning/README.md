# Fine-tuning experiments
## Ontology building
Study the ontology-building capabilities of a fine-tuned model, where a base LLM is trained on new, targeted data, allowing it to adapt effectively to a specific context, such as ontology building.

For the fine-tuning process, a **training dataset** is required, consisting of a collection of CSV files and their corresponding ontologies. The steps to construct this dataset are as follows:
1. Identify 40 CSV files related to commercial activities, which are sourced from the [Kaggle](https://www.kaggle.com/) website, known for providing datasets for data science purposes.
2. Manually build an ontology for each of the CSV files.

Of the training dataset containing 40 pairs of CSV files and their corresponding ontologies:
* 30 pairs will be used for training.
* The remaining 10 pairs will be reserved for validation.

Additionally, **six datasets** related to commercial activities (Airlines, Amazon, Brazilian, BigBasket, Consumer, and E-commerce) will be used as **test data** to evaluate the ontology construction of the fine-tuned model.

### GPT models
The **GPT-4o-mini model** is trained using the training dataset to learn how to translate a CSV file into an ontology. 

First, the training and validation data are transformed into the JSONL format required by the OpenAI model to perform the fine-tuning task. This message format consists of three roles (a message is generated for each CSV file from the training and validation subset): 
* **system**, to indicate the function the model will perform.
* **user**, to indicate the prompt of the task to be performed.
* **assistant**, to indicate the output that the model should display.

Next, using the API provided by OpenAI, the training and validation data are uploaded to the OpenAI platform, and the fine-tuning job is launched with the following hyperparameters:
* n_epochs = 6: An epoch refers to one complete iteration through the entire training dataset. This means the dataset will be used 6 times to adjust the model's parameters. This is relatively high because the task at hand has a single ideal completion (or a small set of similar ideal completions).
* batch_size = 3: The batch size refers to the number of data samples processed before the model updates its parameters. Thus, it indicates that three samples from the data will be taken for a training pass before making adjustments to the model's parameters.
* learning_rate_multiplier = 0.3: This adjusts the rate at which the model learns from the data, influencing how quickly and effectively the model can optimize its parameters.

Once the new fine-tuned model is created using the data of interest, the **learning curves** are analyzed. These learning curves are mathematical representations of the model's learning process during training, helping to assess whether the fine-tuned model is overfitted or underfitted. They provide insight into the model's performance over time, guiding further adjustments if necessary.

### Open-source models (collaboration with Ronghao Pan)
The **Llama 3 (8B) model** is trained and tested using the same method as the GPT-4o model to compare the results of the fine-tuning process in both models. The Llama 3 (8B) model is quantized at both **4-bit** and **8-bit** levels, and the comparison of the fine-tuning process will be conducted to assess how quantization impacts the accuracy of the Llama 3 (8B) model.

The **Llama 2 (13B) model** (without being quantized) is trained and tested using the same method as the GPT-4o model to compare the results of the fine-tuning process in both models.

With this, nearly the entire family of Llama models will have been evaluated, providing a comprehensive understanding of their performance across different versions and sizes. This analysis will offer valuable insights into the strengths and weaknesses of each model, particularly in tasks such as ontology building, helping to determine the most suitable model for achieving optimal results in such specialized tasks.

### Findings
* The main challenge lies in the creation of the training dataset, as it requires manually constructing an ontology for each CSV file included. This process is time-consuming and labor-intensive, demanding a detailed understanding of the data to accurately define the relationships and structures within each ontology.
* From the fine-tuning process, the ontologies are more concise than the base model using the prompt, that is, the redundancy observed with the base model is solved.
* The fine-tuning process addresses the issue where open-source tools failed to display the correct standardized format during ontology building.
* With the same training, the GPT-4o-mini model outperforms the Llama 3 model (8B) quantized at 4 bits, particularly in its ability to create classes that are related through object properties. However, given that the training dataset is small, increasing the dataset size could potentially enhance the performance of the Llama 3 model, allowing it to compete more effectively with the GPT-4o-mini model.
* With the same training, the Llama 3 (8B) model quantized at 8 bits outperforms the Llama 3 (8B) model quantized at 4 bits, having fewer single classes, tending to relate classes by object properties. Also, quantized at 8 bits is capable of defining sub-classes.
* The Llama 2 (13B) is twice as large as the Llama 3 (8B) model and therefore has required more time for its training.
* With the same training, the Llama 2 (13B) model without quantization outperforms the Llama 3 (8B) model quantized at 8 bits, having better performance in identifying appropriate classes from the CSV file, offering more precise and concrete classes compared to the Llama 3 (8B) model when quantized at 8 bits. 
***
## Ontology population - Instruct the model to use a specific ontology of interest
Explore the capabilities of a fine-tuned model using a specific ontology of interest and compare it to a baseline model that directly integrates this ontology into its prompt. The goal is to perform ontology population, which involves updating an ontology with new facts extracted from an input knowledge resource. To achieve this, each line of a CSV file is translated into an RDF graph that aligns with the ontology of interest.

The two approaches are explained below:
* **Through prompt**: The complete ontology is included in the prompt in turtle format, as the model is able to understand ontologies in RDF, RDFS and OWL. 
There is a considerable **token cost** in the system prompt, as the full ontology must be included for each piece of unstructured text at the user prompt.
* **Fine-tuning process**: Train the model with pairs unstructured text-KG where the KG conforms to the ontology of interest. It is like showing the model's use cases.
The system prompt can be very concise, so most of the token cost comes from the unstructured text to be transformed.

The LLM model itself (**GPT-4o**) is asked to build the training dataset for the fine-tuning process in the JSONL format, generating 187 examples (pairs unstructured text-KG) corresponding to the custom ontology. In this case, for the fine-tuning process, the LLM model GPT-4o is asked to build the **training dataset** in the JSONL format, generating 187 examples (pairs unstructured text-KG) corresponding to the custom ontology. 
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

Additionally, a dataset containing information on various countries will be used as **test data** to evaluate the fine-tuned model's ability to utilize the new ontology of interest. For this evaluation, only the first line of the dataset, which contains information about Afghanistan, will be used. 

### GPT models
The **GPT-4o-mini model** is trained using the training dataset to learn how to use a specific ontology. 

First, the training and validation data are transformed into the JSONL format required by the OpenAI model to perform the fine-tuning task. This message format consists of three roles: 
* **system**, to indicate the function the model will perform.
* **user**, to indicate the prompt of the task to be performed.
* **assistant**, to indicate the output that the model should display.

Next, using the API provided by OpenAI, the training and validation data are uploaded to the OpenAI platform, and the fine-tuning job is launched with the following hyperparameters:
* n_epochs = 3.
* batch_size = 3.
* learning_rate_multiplier = 0.3.

### Findings
* Instruct the model to use a specific ontology of interest through the prompt fits perfectly with the ontology of interest, not including new classes or properties. However, some of the information contained in the text is lost.
* Instruct the model to use a specific ontology of interest through a fine-tuning process, the fine-tuned model tends to create new properties that do not exist in the ontology of interest, gathering more information from the text. This could be useful for updating the ontology with new information.

