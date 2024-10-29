# Fine-tuning experiments for ontology building

##  Objective

The objective is to study the ontology building capability of fine-tuned LLM models, where a base LLM is trained on new, targeted data, allowing it to adapt effectively to a specific context.

##  The fine-tuning process

For the fine-tuning process, a **training dataset** is required, consisting of a collection of CSV files and their corresponding ontologies. The steps to construct this dataset are as follows:
1. Identify 40 CSV files related to commercial activities, which are sourced from the [Kaggle](https://www.kaggle.com/) website, known for providing datasets for data science purposes.
2. Manually build an ontology for each of the CSV files.

The training dataset containing 40 pairs of CSV files and their corresponding ontologies are split as follows:
* 30 pairs will be used for training.
* The remaining 10 pairs will be reserved for validation.

## The fine-tuned models

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

### The open-source models 

#### Llama 3 (8B)
The **Llama 3 (8B) model** is trained and tested using the same method as the GPT-4o model to compare the results of the fine-tuning process in both models. The Llama 3 (8B) model is quantized at both **4-bit** and **8-bit** levels, and the comparison of the fine-tuning process will be conducted to assess how quantization impacts the accuracy of the Llama 3 (8B) model. In addition, the model without quantization is also evaluated and compared with the Llama 2 (13B) model.

#### Llama 2 (13B)

The **Llama 2 (13B) model** (non-quantized) is trained and tested using the same method as the GPT-4o model to compare the results of the fine-tuning process in both models.

With this, nearly the entire family of Llama models will have been evaluated, providing a comprehensive understanding of their performance across different versions and sizes. This analysis will offer valuable insights into the strengths and weaknesses of each model, particularly in tasks such as ontology building, helping to determine the most suitable model for achieving optimal results in such specialized tasks.


## Evaluation of the fine-tuned models

The capacity of the fine-tuned models to create the ontologies are tested using **six datasets** related to commercial activities:

* Airlines
* Amazon
* Brazilian
* BigBasket
* Consumer
* E-commerce

## Findings
* The main challenge lies in the creation of the training dataset, as it requires manually constructing an ontology for each CSV file included. This process is time-consuming and labor-intensive, demanding a detailed understanding of the data to accurately define the relationships and structures within each ontology.
* From the fine-tuning process, the ontologies are more concise than the base model using the prompt, that is, the redundancy observed with the base model is solved.
* The fine-tuning process addresses the issue where open-source tools failed to display the correct standardized format during ontology building.
* With the same training, the GPT-4o-mini model outperforms the Llama 3 model (8B) quantized at 4 bits, particularly in its ability to create classes that are related through object properties. However, given that the training dataset is small, increasing the dataset size could potentially enhance the performance of the Llama 3 model, allowing it to compete more effectively with the GPT-4o-mini model.
* With the same training, the Llama 3 (8B) model quantized at 8 bits outperforms the Llama 3 (8B) model quantized at 4 bits, having fewer single classes, tending to relate classes by object properties. Also, quantized at 8 bits is capable of defining sub-classes.
* The Llama 2 (13B) is twice as large as the Llama 3 (8B) model and therefore has required more time for its training.
* With the same training, the Llama 2 (13B) model without quantization outperforms the Llama 3 (8B) model quantized at 8 bits, having better performance in identifying appropriate classes from the CSV file, offering more precise and concrete classes compared to the Llama 3 (8B) model when quantized at 8 bits. 
