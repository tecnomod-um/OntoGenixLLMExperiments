# Use of OntoGenix prompt with the mixtral

## Setting up mixtral

Mixtral is an advanced language model developed by Mistral AI, called Mixtral 8x7B, which uses a Sparse Mixture of Experts (SMoE) architecture. This model is designed to provide very efficient performance in terms of cost and speed, outperforming even Llama-2-70B in most benchmarks and being up to six times faster in inference.

Mixtral is a *decoder-only* model, meaning that it focuses only on text decoding. It uses a set of 8 different parameter sets, called "experts", and at each layer a routing network selects two of these experts to process each token (unit of text). This technique allows the model to have a total of 46.7 billion parameters, but only uses 12.9 billion of these parameters per token. 

Mixtral is based on an architecture that increases the number of available parameters without increasing the processing cost. Only a fraction of the parameters are used at each step, reducing computational cost while maintaining high performance.

The experiment uses a version called **Mixtral 8x7B Instruct**, which is specifically tuned to follow instructions more precisely, with performance similar to GPT-3.5. 

To optimize the use of hardware resources, the model was quantized to 4 bits, improving its efficiency during inference. Inference was performed using four NVIDIA RTX 4090 GPUs, each with 24 GB of VRAM. While quantization reduces the precision of computation and data storage, it does so without significantly affecting the model's performance or accuracy on the tasks it was trained for. This approach improves the model's storage, computation, and power efficiency while maintaining high performance.

## Adaptation of OntoGenix prompts

We have modified the OntoGenix prompts to fit the official mixtral template format. To achieve this, we used the AutoTokenizer class from the Transformers library, which enables the use of the conversation template defined by the model. These templates are integrated into the tokenizer and determine how interactions, structured as lists of messages, are converted into tokenizable text strings in the format expected by the model.

In a conversational context, rather than continuing a single text string (as with standard language templates), the template manages a conversation made up of multiple messages, each with an assigned role. These roles include:

- **System**: Defines the template's function and provides guidelines or instructions on how it should behave during the conversation.
- **User**: Represents the user's input or prompt, such as the task to be completed or the question to be answered.
- **Assistant**: Represents the model's response, delivering the requested information or solution to the user.

The official template follows this format:

```
<s> [INST] Instruction [/INST] Model answer</s> [INST] Follow-up instruction [/INST]
```

Note that `<s>` and `</s>` are special tokens for beginning of string (BOS) and end of string (EOS) while [INST] and [/INST] are regular strings.

## Results obtained

### Airlines Customer satisfaction

Link: https://github.com/tecnomod-um/OntoGenixOpenSourceLLM/tree/main/base-llm/mixtral/AirlinesCustomerSatisfaction

Description: Customers who have already flown with them, including the feedback of the customers on various contexts. 

Analysis: 

### Amazon Rating

Link: https://github.com/tecnomod-um/OntoGenixOpenSourceLLM/tree/main/base-llm/mixtral/AmazonRating

Description: Customer reviews and ratings of Beauty related products sold on their website.

Analysis: 

### BigBasket Products

Link: https://github.com/tecnomod-um/OntoGenixOpenSourceLLM/tree/main/base-llm/mixtral/BigBasketProducts

Description: Products listed on the website of online grocery store Big Basket.

Analysis: 

###  Brazilian e-commerce

Link: https://github.com/tecnomod-um/OntoGenixOpenSourceLLM/tree/main/base-llm/mixtral/BrazilianE-commerce

Description: Brazilian e-commerce public dataset of orders made at Olist Store.

Analysis: 

### Customer complaint

Link: https://github.com/tecnomod-um/OntoGenixOpenSourceLLM/tree/main/base-llm/mixtral/CustomerComplaint

Description: Collection of complaints about consumer financial products.

Analysis: 

### E-commerce

Link: https://github.com/tecnomod-um/OntoGenixOpenSourceLLM/tree/main/base-llm/mixtral/eCommerce

Description: Transactions for a UK-based and registered non-store online retail.

Analysis: 

## Summary and findings 
- Mixtral is a model that combines 8 models with 7 billion parameters, so it generates the high-level description correctly, but loses some information. 
- It does not generate output in the format defined in the ontology and mapping generation prompt.
- It produces a lot of hallucinations, especially in ontology generation and mapping. 
