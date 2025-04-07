# Ontology building
## Introduction
When referring to **ontology building capacity**, we refer to the model's ability to understand, generate, and organize structured knowledge by identifying relationships, categories, and hierarchies within a specific domain.

This includes the model's proficiency in accurately mapping data to concepts, defining classes, properties, and relationships, and constructing a coherent framework that represents the information in a meaningful and logically consistent way.

We have studied the ontology-building capabilities of:
* GPT base models from OpenAI and open-source LLMs through the **prompt**.
* **Fine-tuning**, the model is trained on new, targeted data, allowing it to adapt effectively to a specific context, such as the ontology building.

## Fine-tuning process
The Python scripts mencioned in this part cannot be executed due to using a model developed within the Tecnomod department's API, as well as the department's own API key. Then, they are shown to illustrate what the execution line of the fine-tuning process would be like.
### Preparation of the training dataset
For the fine-tuning process, a **training dataset** is required, consisting of a collection of CSV files and their corresponding ontologies. The steps to construct this dataset are as follows:
* Identify 40 CSV files related to commercial activities, which are sourced from the Kaggle website, known for providing datasets for data science purposes.
* Manually build an ontology for each of the CSV files.

Need a total of **40 examples (pairs CSV file-ontology)** for the fine-tuning process of the LLMs. 
* A total of 30 examples as [**training data**](./training_data/train_data.jsonl).
* A total of 10 examples as [**validation data**](./training_data/validation.jsonl).
* 6 datasets related to commercial activities from Ontogenix paper as [**test data**](./test_files).

This process is reflected in the Python script named [preparation_training_dataset.py](./scripts/preparation_training_dataset.py?ref_type=heads). To use the script, the next line code is needed:
`python preparation_training_dataset.py input_folder output_folder`

Where **input_folder** is the path to the folder containing the CSV files and their corresponding ontologies that will be used for the training process, and the **output_folder** is the path to the folder where the training and validation data is going to be stored in JSONL format.

The following LLMs will be used:
* Llama 2 (13B)
* Llama 3 (8B) quantized at 4 bits
* Llama 3 (8B) quantized at 8 bits
* Llama 3 (8B) without quantization
* GPT-4o-mini

### Launch of the fine-tuning job (GPT model via OpenAI)
For OpenAI models, launching a fine-tuning job using the **GPT-4o-mini** model involves the following steps:
1. Upload the training and validation files to the OpenAI platform.
2. Define the hyperparameters for the fine-tuning job (n_epochs,batch_size,learning_rate_multiplier).
3. Create the fine-tuning job with the selected model and the provided training and validation data.
 
This process is reflected in the Python script named [ft_ontobuilder_creation.py](./scripts/ft_ontobuilder_creation.py?ref_type=heads). To use the script, the next line code is needed:
`python ft_ontobuilder_creation.py input_folder suffix`

Where **input_folder** is the path to the folder containing the training and validation data and the **suffix** that is, a suffix to identify the fine-tuned model. 

### Use of the fine-tuned model (via OpenAI)
Querying the fine-tuned model to translate the CSV files to an ontology involves the following steps:
1. Build the prompt with the CSV file to be translated into an ontology in TTL format.
2. Get the ontology built by the fine-tuned model and store it as an OWL file.

This process is reflected in the Python script named [response_ft_ontobuilder.py](./scripts/response_ft_ontobuilder.py?ref_type=heads). To use the script, the next line code is needed:
`python response_ft_ontobuilder.py ft_model input_folder output_folder`

Where **ft_model** is the name of the fine-tuned model, **input_folder** is the path to the folder containing the CSV files to be translated into ontologies and the **output_folder** is the path to the folder where ontologies built by the fine-tuned model will be stored in OWL format.

## Findings
* The fine-tuning process addresses the issue where open-source tools failed to display the correct standardized format during ontology building.
* This is the ranking of the fine-tuned models with respect to ontology building (The higher a model ranks, the better its ontology building capacity):
    1. GPT-4o-mini
    2. Llama 3 (8B)
    3. Llama 2 (13B)
    4. Llama 3 (8B) quantized at 8 bits
    5. Llama 3 (8B) quantized at 4 bits

* Open-source LLMs should be trained with more data than GPT to have similar accuracy.
* Classes:
    - Not all columns derive in classes.
    - Quantized LLMs do not improve non-quantized ones.
    - Some LLMs use general names.
    - For some LLMs the distinction between entities and properties is not very clear.
* Object properties:
    - Different levels of performance in the connection of classes through OPs.
* Enrichment of the training data:
    - Llama LLMs tend to create classes that are not present in the CSV file, inferring them from the training dataset.







