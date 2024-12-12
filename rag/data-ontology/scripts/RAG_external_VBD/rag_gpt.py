import argparse
from utils_data_ont import dataframe2prettyjson, read_txt_file_as_string, rag_loader, save_chromedb, similarity_search_context
import pandas as pd
import LlmBase
import json


class LlmIRIGpt(LlmBase.GptLLM):
    name = 'ontology'

    def __init__(self, model_name, json_data, description, temperature=0.5 ):
        super().__init__(model_name, temperature)
        self.prompt_path = "./IRI_search_prompt.txt"
        self.system_input = """As an expert ontology mapper, I need your help in searching for suitable identifiers from the column names of a CSV file."""
        self.json_data = json_data
        self.description = description
        self.prompt = ""

    def set_prompt(self, json_data, description, ontologies_examples):
        initial_prompt = read_txt_file_as_string(self.prompt_path)
        initial_prompt = initial_prompt.format(json_data=json_data, description=description, ontologies_examples=ontologies_examples)
        conversation = []
        conversation.append({"role": "system", "content": self.system_input})
        conversation.append({"role": "user", "content": initial_prompt}) 
        self.prompt = conversation     

    def get_prompt(self): 
        return self.prompt

def main(args):
    output_folder = args.output_folder
    dataset_path = args.dataset_path
    dataset_description = args.dataset_description
    model_name = args.model_name

    ### if new database ###
    #documents = rag_loader()
    #save_chromedb(documents)
    #######################

    dataframe = pd.read_csv(dataset_path) #csv file loaded
    sample_dataframe = dataframe.head(10)
    json_data = dataframe2prettyjson(sample_dataframe) #csv2json
    json_data_json = json.loads(json_data)

    with open(dataset_description, 'r', encoding='utf-8') as file:
        description = file.read()

    print('---------------------------------------------------')
    llm_ontology = LlmIRIGpt(model_name, json_data, description) #Main task: Search identifiers from the synthesized JSON data

    #ontologies_examples = similarity_search_context(json_data) #get the ontologies similar to the JSON data
    result_strings = []
    for column, value in json_data_json["0"].items():
        result = similarity_search_context(column)  # Apply the function
        print('###############')
        print(column,result)
        print('###############')
        result_strings.append(result)
    # Combine all results into a single string with newlines
    ontologies_examples = "\n".join(result_strings)
    print(f"RAG-identifiers extrated:\n{ontologies_examples}")
    llm_ontology.set_prompt(llm_ontology.json_data, llm_ontology.description, ontologies_examples) #Prompt generation for the main task (based few-shot)
    print("--------------")
    llm_ontology.run_inference(llm_ontology.prompt) #Get the ontology
    llm_ontology.save_responses_to_json(output_folder, llm_ontology.responses[0]["response"])

if __name__ == "__main__": 
    parser = argparse.ArgumentParser()
    parser.add_argument("--output_folder",  type=str)
    parser.add_argument("--dataset_path", type=str)
    parser.add_argument("--dataset_description", type=str)
    parser.add_argument("--model_name", type=str)
    
    args = parser.parse_args()
    main(args)
