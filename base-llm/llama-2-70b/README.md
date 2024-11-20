# Use of OntoGenix prompt with the Llama-2-70B

## Setting up Llama-2-70B

LLama-2 is a set of pre-trained and tuned generative text models ranging from 7 to 70 billion parameters. These models are designed for a wide range of natural language processing (NLP) tasks such as text generation, summarization, question answering, and dialog systems. It is the largest Llama-2 model, with a total of 70 billion parameters, and is designed in an autoregressive model language using an optimized transformer architecture. 

For the experiment, we have used the chat version, called **Llama-2-70b-chat-hf**, which is the fine-tuned and dialog case-optimized version of Llama-2-70b. This version uses supervised fine tuning (SFT) and reinforcement learning with human feedback (RLHF) to match human preferences for utility and safety.

To optimize the use of hardware resources, the model has been quantized to 4 bits in order to optimize its efficiency during inference.  In addition, four NVIDIA RTX 4090 GPUs, each with 24 GB of VRAM, were used to perform the quantized model inference. Quantization is a technique that reduces the precision of the computations and data stored in the model without significantly reducing the performance or accuracy of the tasks for which the model was trained. In this way, the model is more efficient in terms of storage, computation, and power consumption, while maintaining a high level of performance. 


## Adaptation of OntoGenix prompts

Each model has its own structure for prompts, so to adapt the OntoGenix prompts in Llama-2, we had to rewrite the prompt adapting the structure defined by Llama-2. 

To do this, we have used the AutoTokenizer class from the Transformers library, which allows us to use the chat template defined by the model.  Chat templates are part of the tokenizer and specify how to convert conversations, represented as lists of messages, into a single tokenizable string according to the format expected by the model. 

In a chat context, instead of continuing a single string of text (as is the case with a standard language template), the template continues a conversation consisting of one or more messages, each of which includes a role, such as *user* or *assistant*, as well as the message text. Therefore, the following three roles are defined for each prompt:

- **system**: Indicates the function that the model is supposed to perform. This role provides guidelines or instructions on how the model should behave within the conversation.
- **user**:  Indicates the prompt or the task to be performed. This role represents the user's input or the questions that the model needs to respond to.
- **assistant**:  Indicates the output that the model should generate. This role is the response or information that the model should provide in reply to the user's prompt.

## Results obtained

### Airlines Customer satisfaction

Link: https://github.com/tecnomod-um/OntoGenixOpenSourceLLM/tree/main/base-llm/llama-2-70b/AirlinesCustomerSatisfaction

Description: Customers who have already flown with them, including the feedback of the customers on various contexts. 

Analysis: 

### Amazon Rating

Link: https://github.com/tecnomod-um/OntoGenixOpenSourceLLM/tree/main/base-llm/llama-2-70b/AmazonRating

Description: Customer reviews and ratings of Beauty related products sold on their website.

Analysis: 

### BigBasket Products

Link: https://github.com/tecnomod-um/OntoGenixOpenSourceLLM/tree/main/base-llm/llama-2-70b/BigBasketProducts

Description: Products listed on the website of online grocery store Big Basket.

Analysis: 

###  Brazilian e-commerce

Link: https://github.com/tecnomod-um/OntoGenixOpenSourceLLM/tree/main/base-llm/llama-2-70b/BrazilianE-commerce

Description: Brazilian e-commerce public dataset of orders made at Olist Store.

Analysis: 

### Customer complaint

Link: https://github.com/tecnomod-um/OntoGenixOpenSourceLLM/tree/main/base-llm/llama-2-70b/CustomerComplaint

Description: Collection of complaints about consumer financial products.

Analysis: 

### E-commerce

Link: https://github.com/tecnomod-um/OntoGenixOpenSourceLLM/tree/main/base-llm/llama-2-70b/eCommerce

Description: Transactions for a UK-based and registered non-store online retail.

Analysis: 

## Summary of the findings

- As a model with 70 billion parameters, it requires a greater amount of hardware resources to infer.
- The model generates the high-level description correctly.
- The model does not correctly interpret the instructions to generate ontologies in Turtle and map to RML or YAML.
