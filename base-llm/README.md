# Experiments with base openLLMs

## Objective

The objective of these experiments is to study the ontology generation capacity of different base openLLMs


## The approach

The aim of this experiment is to use the OntoGenix approach and the the defined [OntoGenix](https://github.com/tecnomod-um/OntoGenix_BASF/tree/main/GUI) prompts, but changing the generation engine. Instead of GPT-4, an opensource LLM is used for high-level description generation, ontology generation and ontology mapping to YML format in each experiment

All the experiments used the same generation parameters for different LLMs to ensure comparability of results and to fairly assess the performance of each model under similar conditions. 

The generation parameters are: 

- top_p=0.8: The value of top_p controls the probabilistic sampling in text generation. A value of 0.8 allows for more diversity in the generation by restricting the sampling to a relevant subset of words, preventing the model from becoming too predictable or choosing words that are too unlikely.
- top_k=40: The value of top_k limits the number of candidate words from which the model can choose. This value reduces the possibility of selecting low probability words, which helps to control the consistency and quality of the generated text. Therefore, a value of 40 allows for sufficient diversity without making the generation too random.
- temperature=0.5: Temperature adjusts the level of ‘creativity’ of the model. A lower temperature (close to 0) makes the model more conservative and chooses the most likely options, while a higher temperature (close to 1 or more) makes it more likely to explore less likely options. Thus, a value of 0.5 balances creativity and accuracy, providing coherent and sensible answers without the text being monotonous or too predictable.
- max_new_tokens=4096: This parameter defines the maximum number of tokens.  A limit of 4096 is relatively large and allows the model to generate long or continuous responses without truncating the text.

## Experiments by openLLM

For each LLM, we have evaluated a series of Kaggle datasets related to commercial activities of organizations (Airlines, Amazon, Brazilian, BigBasket, Consumer, and E-commerce), which are the same as those evaluated in the [Ontogenix Evaluation](https://github.com/tecnomod-um/OntoGenixEvaluation) project (without ontology quality analysis which will come later).

* [LLama-2-7b](./llama-2-7b/README.md)
* [LLama-2-70b](./llama-2-70b/README.md)
* [LLama-3-8b](./llama-3-8b/README.md)
* [LLama-3-70b](./llama-3-70b/README.md)
* [Mistral-7b](./mistral-7b/README.md)
* [Mixtral](./mixtral/README.md)

## Summary of the findings

- The Mixtral, Mistral and Llama-2 family models produce numerous hallucinations and generate response that do not align with the standardized format specified in the prompt. Therefore, we discarded them for detailed analysis. 
- The Llama-3 family was trained on over 15 trillion tokens, resulting in fewer hallucinations and generally aligning with the standardized format defined in the prompt. 
- Main limitations include the tendency of the latest open-source LLMs used as ontology generation engines to produce hallucinations and deviate from the prompt's defined standardization, as well as the difficulty in evaluating the generated ontologies.
- Proposed solutions to address the identified limitations include fine-tuning LLMs to model new data within the same domain of interest and in a specified format, and implementing a RAG (Retrieval-Augmented Generation) architecture with sample ontologies and schemas stored in a vector database.

