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

## The fine-tuned GPT models

The **GPT-3.5 model** and **GPT-4o-mini model** are trained using the training dataset to learn how to translate a CSV file into an ontology. 

First, the training and validation data are transformed into the JSONL format required by the OpenAI model to perform the fine-tuning task. This message format consists of three roles (a message is generated for each CSV file from the training and validation subset): 
* **system**, to indicate the function the model will perform.
* **user**, to indicate the prompt of the task to be performed.
* **assistant**, to indicate the output that the model should display.

Next, using the API provided by OpenAI, the training and validation data are uploaded to the OpenAI platform, and the fine-tuning job is launched with the following hyperparameters:
* n_epochs = 6: An epoch refers to one complete iteration through the entire training dataset. This means the dataset will be used 6 times to adjust the model's parameters. This is relatively high because the task at hand has a single ideal completion (or a small set of similar ideal completions).
* batch_size = 3: The batch size refers to the number of data samples processed before the model updates its parameters. Thus, it indicates that three samples from the data will be taken for a training pass before making adjustments to the model's parameters.
* learning_rate_multiplier = 0.3: This adjusts the rate at which the model learns from the data, influencing how quickly and effectively the model can optimize its parameters.

Once the new fine-tuned model is created using the data of interest, the **learning curves** are analyzed. These learning curves are mathematical representations of the model's learning process during training, helping to assess whether the fine-tuned model is overfitted or underfitted. They provide insight into the model's performance over time, guiding further adjustments if necessary.

The ontologies obtained with the fine-tuned GPT-4o-mini model are located in the directory [GPT_ft](./GPT_ft/4o-mini).

The ontologies obtained with the fine-tuned GPT-3.5 model are located in the directory [GPT_ft](./GPT_ft/3_5).


## Executability

The following table shows with an X when the LLM model was able to generate the ontology in question with an appropiate syntax. We also include the total number of these ontologies:

| LLM model   | AirlinesCustomerSatisfaction | AmazonRating | BigBasketProducts | BrazilianE-commerce | CustomerComplaint | eCommerce | Total  |
|-------------|------------------------------|--------------|-------------------|---------------------|-------------------|-----------|--------|
| GPT-3.5     | X                            | X            | -                 | X                   | X                 | X         | 5      |
| GPT-4o      | X                            | X            | X                 | -                   | X                 | X         | 5      |
| GPT-4o-mini | X                            | X            | X                 | X                   | X                 | X         | 6      |
| **Total**   | **3**                        | **3**        | **2**             | **2**               | **3**             | **3**     | **16** |


The following table shows the main errors made by LLM models in the generation of ontologies:

| LLM model   | AirlinesCustomerSatisfaction | AmazonRating | BigBasketProducts                            | BrazilianE-commerce                  | CustomerComplaint | eCommerce |
|-------------|------------------------------|--------------|----------------------------------------------|--------------------------------------|-------------------|-----------|
| GPT-3.5     | X                            | X            | Incorrect serialization (prefix not defined) | X                                    | X                 | X         |
| GPT-4o      | X                            | X            | X                                            | Incorrect serialization (shortnames) | X                 | X         |
| GPT-4o-mini | X                            | X            | X                                            | X                                    | X                 | X         |


Below we include a new table with those ontologies that could be developed after a human intervention. These were the ontologies with serialization, and format errors, where a human intervention for correction implies a lower effort than a de novo development.

| LLM model   | AirlinesCustomerSatisfaction | AmazonRating | BigBasketProducts | BrazilianE-commerce | CustomerComplaint | eCommerce | Total  |
|-------------|------------------------------|--------------|-------------------|---------------------|-------------------|-----------|--------|
| GPT-3.5     | X                            | X            | X                 | X                   | X                 | X         | 6      |
| GPT-4o      | X                            | X            | X                 | X                   | X                 | X         | 6      |
| GPT-4o-mini | X                            | X            | X                 | X                   | X                 | X         | 6      |
| **Total**   | **3**                        | **3**        | **3**             | **3**               | **3**             | **3**     | **18** |



## Findings
