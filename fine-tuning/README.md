## Introduction
The following LLMs will be used:
* Llama 2 (7B) quantized at 4 bits
* Llama 2 (7B) quantized at 8 bits
* Llama 2 (7B) without quantization
* Llama 2 (13B)
* Llama 3 (8B) quantized at 4 bits
* Llama 3 (8B) quantized at 8 bits
* Llama 3 (8B) without quantization
* GPT-3.5-turbo (GPT-3.5-turbo-0125)
* GPT-4o (GPT-4o-2024-08-06)
* GPT-4o-mini (GPT-4o-mini-2024-07-18)


## Preparation of the training dataset
For the fine-tuning process, a **training dataset** is required, consisting of a collection of CSV files and their corresponding ontologies. The steps to construct this dataset are as follows:
* Identify 40 CSV files related to commercial activities, which are sourced from the Kaggle website, known for providing datasets for data science purposes.
* Manually build an ontology for each of the CSV files.

Need a total of **40 examples (pairs CSV file-ontology)** for the fine-tuning process of the LLMs. 
* A total of 30 examples as [**training data**](./training_data/train_data.jsonl).
* A total of 10 examples as [**validation data**](./training_data/validation_data.jsonl).
  
Additionally, 6 datasets related to commercial activities from Ontogenix paper will be used as [**test data**](./test_files).

This process is reflected in the Python script named [preparation_training_dataset.py](./scripts/fine_tuning_gpt/preparation_training_dataset.py). To use the script, the following code is needed:
`python preparation_training_dataset.py input_folder output_folder`

Where `input_folder` is the path to the folder containing the CSV files and their corresponding ontologies that will be used for the training process, and the `output_folder` is the path to the folder where the training and validation data are going to be stored in JSONL format.

## Launch of the fine-tuning job 
For OpenAI models, launching a fine-tuning job using GPT models involves the following steps:
1. Upload the training and validation files to the OpenAI platform.
2. Define the hyperparameters for the fine-tuning job (n_epochs,batch_size,learning_rate_multiplier).
3. Create the fine-tuning job with the selected model and the provided training and validation data.
 
This process is reflected in the Python script named [ft_ontobuilder_creation.py](./scripts/fine_tuning_gpt/ft_ontobuilder_creation.py). To use the script, the following code is needed:
`python ft_ontobuilder_creation.py input_folder suffix`

Where `input_folder` is the path to the folder containing the training and validation data, and the `suffix` is used to identify the fine-tuned model. 

## Use of the fine-tuned model 
Querying the fine-tuned model to translate the CSV files to an ontology involves the following steps:
1. Build the prompt with the CSV file to be translated into an ontology in TTL format.
2. Get the ontology built by the fine-tuned model and store it as an OWL file.

This process is reflected in the Python script named [response_ft_ontobuilder.py](./scripts/fine_tuning_gpt/response_ft_ontobuilder.py). To use the script, the following code is needed:
`python response_ft_ontobuilder.py ft_model input_folder output_folder`

Where `ft_model` is the name of the fine-tuned model, `input_folder` is the path to the folder containing the CSV files to be translated into ontologies, and `output_folder` is the path to the folder where ontologies built by the fine-tuned model will be stored in OWL format.

