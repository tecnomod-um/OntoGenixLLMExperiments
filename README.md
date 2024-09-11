# Evaluation of Open Source LLMs for OntoGenix
This repository describes and reports the results obtained by applying the OntoGenix pipeline with open source large language models (openLLMs).

## openLLMs used
* [Llama-2](https://huggingface.co/meta-llama/Llama-2-7b): 7B and 70B
* [Llama-3](https://github.com/meta-llama/llama3): 8B and 70B
* [Mixtral](https://huggingface.co/docs/transformers/en/model_doc/mixtral): base and 7B

## Experiments 

The experiments consisted in generating ontologies for the Kaggle datasets used in the [original experiments with OpenAI GPT](https://github.com/tecnomod-um/OntoGenixEvaluation).

Therefore, each experiment with a particular configuration of an OpenLLM consisted in generating an ontology from one of those datasets. A page will describe each type of experiment, and the results of each openLLM will be found in a specific folder. 

There are the types of experiments performed:

* [Base openLLM](./base-llm/README.md): Use of the OntoGenix prompts with the base distribution of the openLLM. These experiments are performed only with openLLMs
 
* [Fine-tuning](./fine-tuning/README.md): Use of the OntoGenix prompts with fine-tuned LLMs. These experiments are performed with both openLLMs and openAI GPT.

* [RAG](./rag/README.md): Use of the OntoGenix prompts with base LLMs with Retrieved Augmented Generation (RAG). These experiments are performed with both openLLMs and openAI GPT.
