# Use of OntoGenix prompt with the Llama-2-7B

## Setting up Llama-2-7B

LLama-2 is a set of pre-trained and tuned generative text models ranging from 7 to 70 billion parameters. These models are designed for a wide range of natural language processing (NLP) tasks such as text generation, summarization, question answering, and dialog systems. Model 7B is the smallest in the series and is optimized for dialog use cases, making it ideal for chatbots, virtual assistants, and conversational AI. For the experiment, we used the **Llama-2-7B-Chat-hf** version, which is a variant of Llama 2 specifically optimized for conversational applications and interactive natural language tasks. 

To optimize the use of hardware resources, the model was quantized to 8 bits. Quantization is a technique that reduces the precision of the computations and data stored in the model without significantly reducing the performance or accuracy of the tasks for which the model was trained. In this way, the model is more efficient in terms of storage, computation, and power consumption, while maintaining a high level of performance. 


## Adaptation of OntoGenix prompts

Each model has its own structure for prompts, so to adapt the OntoGenix prompts in Llama-2, we had to rewrite the prompt adapting the structure defined by Llama-2. 

To do this, we have used the AutoTokenizer class from the Transformers library, which allows us to use the chat template defined by the model.  Chat templates are part of the tokenizer and specify how to convert conversations, represented as lists of messages, into a single tokenizable string according to the format expected by the model. 

In a chat context, instead of continuing a single string of text (as is the case with a standard language template), the template continues a conversation consisting of one or more messages, each of which includes a role, such as *user* or *assistant*, as well as the message text. Therefore, the following three roles are defined for each prompt:

- **system**: Indicates the function that the model is supposed to perform. This role provides guidelines or instructions on how the model should behave within the conversation.
- **user**:  Indicates the prompt or the task to be performed. This role represents the user's input or the questions that the model needs to respond to.
- **assistant**:  Indicates the output that the model should generate. This role is the response or information that the model should provide in reply to the user's prompt.

## Results obtained

The results obtained with this LLM are shown next, although the model was discarded for a detailed analysis, as explained in the general summary of findings.

### Airlines Customer satisfaction

Link: https://github.com/tecnomod-um/OntoGenixOpenSourceLLM/tree/main/base-llm/llama-2-7b/AirlinesCustomerSatisfaction

Description: Customers who have already flown with them, including the feedback of the customers on various contexts. 

### Amazon Rating

Link: https://github.com/tecnomod-um/OntoGenixOpenSourceLLM/tree/main/base-llm/llama-2-7b/AmazonRating

Description: Customer reviews and ratings of Beauty related products sold on their website.


### BigBasket Products

Link: https://github.com/tecnomod-um/OntoGenixOpenSourceLLM/tree/main/base-llm/llama-2-7b/BigBasketProducts

Description: Products listed on the website of online grocery store Big Basket.


###  Brazilian e-commerce

Link: https://github.com/tecnomod-um/OntoGenixOpenSourceLLM/tree/main/base-llm/llama-2-7b/BrazilianE-commerce

Description: Brazilian e-commerce public dataset of orders made at Olist Store.


### Customer complaint

Link: https://github.com/tecnomod-um/OntoGenixOpenSourceLLM/tree/main/base-llm/llama-2-7b/CustomerComplaint

Description: Collection of complaints about consumer financial products.


### E-commerce

Link: https://github.com/tecnomod-um/OntoGenixOpenSourceLLM/tree/main/base-llm/llama-2-7b/eCommerce

Description: Transactions for a UK-based and registered non-store online retail.


## Summary of the findings

- Correctly generates high level description.
- The model does not generate an ontology with a valid syntax in any of the 6 datasets. It generates a lot of hallucinations because it does not understand the instructions based on the TURTLE format for ontology generation.
- The model does not correctly generate the mapping to RML format.


