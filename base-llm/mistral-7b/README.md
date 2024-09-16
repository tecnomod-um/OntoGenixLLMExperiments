# Use of OntoGenix prompt with the mistral-7B

## Setting up mistral-7B

Mistral-7B is a 7.3 billion parameter language model designed to perform natural language processing tasks efficiently and accurately. Despite having fewer parameters than other models, such as LLaMa-2-13B, Mistral-7B offers superior performance in several areas, such as inference, text understanding, and code generation. 

One of its main features is the use of advanced techniques such as Grouped Query Attention (GQA) and Sliding Window Attention (SWA), which improve the speed of inference (when the model generates answers) and allow it to handle longer texts without significantly increasing the computational cost. 

For the experiment, we used a version of Mistral called **Mistral-7B-Instruct**, which is a tuned version of the **Mistral-7B** model specifically designed to perform instructional and chat tasks more efficiently. While Mistral-7B is a general model that can be applied to a wide variety of tasks, Mistral-7B-Instruct has been trained on datasets containing instructions, making it better suited for understanding and answering questions in conversation or following step-by-step instructions.

To maximize hardware efficiency, the model was quantized to 8 bits, a method that reduces the precision of computations and data storage. This approach greatly lowers the model's memory and computational demands without significantly affecting its performance or accuracy on its target tasks. By decreasing the bit width, quantization enhances storage, computation, and power efficiency, enabling the model to run on less powerful hardware or at a lower cost, while still delivering high-quality ontology generation results.


## Adaptation of OntoGenix prompts

We have adapted the OntoGenix prompts to the format of the official Llama 3 template. To achieve this, we used the AutoTokenizer class from the Transformers library, which allows the use of the conversation template defined by the model. These conversation templates are part of the tokenizer and dictate how interactions structured as lists of messages are converted into a tokenizable text string that follows the expected format of the model.

In a conversational context, instead of continuing a single string of text (as in typical language templates), the template handles a conversation consisting of one or more messages, each of which is assigned a specific role. These roles include

- **System**: Defines the purpose of the template and provides instructions on how the conversation should proceed.
- **User**: Represents the user's input or prompt, outlining the task to be performed or the question to be answered.
- **Assistant**: Represents the model-generated response that provides the information or solution requested by the user.

The official template follows this format:

```
text = "<s>[INST] What is your favourite condiment? [/INST]"
"Well, I'm quite partial to a good squeeze of fresh lemon juice. It adds just the right amount of zesty flavour to whatever I'm cooking up in the kitchen!</s> "
"[INST] Do you have mayonnaise recipes? [/INST]"
```

As shown in the example above, the prompt must be enclosed by [INST] and [/INST] tokens. The first statement must begin with a statement start tag. Subsequent statements do not. The generation of the wizard ends with the end-of-statement identifier.

## Results obtained

### Airlines Customer satisfaction

Link: https://github.com/tecnomod-um/OntoGenixOpenSourceLLM/tree/main/base-llm/mistral-7b/AirlinesCustomerSatisfaction

Description: Customers who have already flown with them, including the feedback of the customers on various contexts. 

Analysis: 

### Amazon Rating

Link: https://github.com/tecnomod-um/OntoGenixOpenSourceLLM/tree/main/base-llm/mistral-7b/AmazonRating

Description: Customer reviews and ratings of Beauty related products sold on their website.

Analysis: 

### BigBasket Products

Link: https://github.com/tecnomod-um/OntoGenixOpenSourceLLM/tree/main/base-llm/mistral-7b/BigBasketProducts

Description: Products listed on the website of online grocery store Big Basket.

Analysis: 

###  Brazilian e-commerce

Link: https://github.com/tecnomod-um/OntoGenixOpenSourceLLM/tree/main/base-llm/mistral-7b/BrazilianE-commerce

Description: Brazilian e-commerce public dataset of orders made at Olist Store.

Analysis: 

### Customer complaint

Link: https://github.com/tecnomod-um/OntoGenixOpenSourceLLM/tree/main/base-llm/mistral-7b/CustomerComplaint

Description: Collection of complaints about consumer financial products.

Analysis: 

### E-commerce

Link: https://github.com/tecnomod-um/OntoGenixOpenSourceLLM/tree/main/base-llm/mistral-7b/eCommerce

Description: Transactions for a UK-based and registered non-store online retail.

Analysis: 
