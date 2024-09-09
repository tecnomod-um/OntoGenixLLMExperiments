# Fine-tuning and RAG experiments
## Ontology building
Study the ontology-building capabilities of:
* GPT base models from OpenAI through the **prompt** (Experiments realized by Juan Mulero).
* **Fine-tuning**, the model is trained on new, targeted data, allowing it to adapt effectively to a specific context, such as ontology building.
* **Retrival-Augmented Generation** (RAG), the model is provided with files to use as a reference for future queries. 
***
### Fine-tuning - GPT models
The **GPT-4o-mini model** is trained using 40 example pairs (CSV file and corresponding ontology) to learn how to translate a CSV file into an ontology. Of these 40 examples, 30 are used for training, while the remaining 10 are set aside for validation. Six datasets related to commercial activities will be used as test data to evaluate the ontology construction of the fine-tuned model.
### Fine-tuning - Open-source models (collaboration with Ronghao Pan)
The **Llama 3 (8B) model** is trained and tested using the same method as the GPT-4o model to compare the results of the fine-tuning process in both models. 

The Llama 3 (8B) model is quantized at both 4-bit and 8-bit levels, and the comparison of the fine-tuning process will be conducted to assess how quantization impacts the accuracy of the Llama 3 (8B) model.
### RAG
Due to the limitations of the API regarding file upload formats, the RAG process will be tested using the GPT-builder tool instead. This tool, available on the OpenAI website, supports the use of the Turtle format, which is necessary for uploading various ontology files. These ontology files will serve as references that the model will consult to accurately translate a given CSV file into an ontology.
### Results
* In both the RAG and fine-tuning processes, similar results are obtained. In both cases the ontologies are more concise than the base model using the prompt, that is, the redundacy observed with the base model is solved.
* The fine-tuning process addresses the issue where open-source tools failed to display the correct standardized format during ontology building.
* With the same training, the GPT-4o-mini model outperforms the Llama 3 model (8B) quantized at 4 bits, particularly in its ability to create classes that are related through object properties. However, given that the training dataset is small, increasing the dataset size could potentially enhance the performance of the Llama 3 model, allowing it to compete more effectively with the GPT-4o-mini model.
***
## Instruct the model to use a specific ontology of interest.
* **Through prompt**: The complete ontology is included in the prompt in turtle format, as the model is able to understand ontologies in RDF, RDFS and OWL. 
There is a considerable **token cost** in the system prompt, as the full ontology must be included for each piece of unstructured text at the user prompt.
* **Fine-tuning process**: Train the model with pairs unstructured text-KG where the KG conforms to the ontology of interest. It is like showing the model's use cases.
The system prompt can be very concise, so most of the token cost comes from the unstructured text to be transformed.
### Results 
* Instruct the model to use a specific ontology of interest through the prompt fits perfectly with the ontology of interest, not including new classes or properties. However, some of the information contained in the text is lost.
* Instruct the model to use a specific ontology of interest through a fine-tuning process, the fine-tuned model tends to create new properties that do not exist in the ontology of interest, gathering more information from the text. This could be useful for updating the ontology with new information.


