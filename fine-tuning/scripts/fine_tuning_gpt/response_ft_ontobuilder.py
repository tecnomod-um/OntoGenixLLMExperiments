import pandas as pd #dataframe manipulation 
from openai import OpenAI #ChatGPT API
from dotenv import dotenv_values #environment control
import os #interact with the operating system
import chardet #to detect the enconding of the CSV file
import sys

def load_environment(): 
    """
    Load the API key of OpenAI from the environment.
    """
    config = dotenv_values(dotenv_path=".env")
    return config['OPENAI_API_KEY']

def encoding_detection(archive):
    """
    Detects the encoding of a file.

    Args:
        archive (str): The path to the file.

    Returns:
        str: Detected encoding of the file.
    """
    with open(archive, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']

def get_openai_response(ft_model,folder_path):
    """
    Get the output from the fine-tuned model, creating the client to launch the query. 

    Args:
        ft_model (str): The name of the fine-tuned model.
        folder_path (str): Path where the CSV files, which need to be translated into an ontology, are located. 

    Returns:
        dicc (dict): Dictionary where the keys are the names of the CSV files, and the values are their corresponding ontologies.
    """
    api_key=load_environment()
    client = OpenAI(api_key=api_key) 

    dicc = {} #for each CSV file, we get its corresponding ontology

    for file in os.listdir(folder_path):
        if file.endswith('.csv'):
            csv_path = os.path.join(folder_path, file)   
            try:
                encoding = encoding_detection(csv_path)  
                df = pd.read_csv(csv_path, encoding=encoding) 
            except (UnicodeDecodeError, LookupError):
                df = pd.read_csv(csv_path, encoding='unicode_escape')  
            
            data_description = {} #get the data description of each column
            for col in df.columns:
                if pd.api.types.is_numeric_dtype(df[col]):
                    min_val = df[col].min().item()
                    max_val = df[col].max().item()
                    data_description[col] = {'min': min_val, 'max': max_val}
                else:
                    unique_values = df[col].unique().tolist()
                    data_description[col] = unique_values
            
        completion = client.chat.completions.create(
            model=ft_model, #fine-tune model
            messages=[
                {"role": "system", "content": "You are going to assist me in the translation of a user dataset related to commercial activities to an ontology using the RDF, XML, XSD, RDFS, and OWL ontologies formatted as TTL"},
                {"role": "user", "content": f"""For the next dataset description: {data_description}, I need you to translate the dataset related to commercial activities to an ontology using the RDF, XML, XSD, RDFS, and OWL ontologies formatted as TTL.
                    Try to differentiate between concepts (Classes) and attributes (Data properties). Use the prefix um: with IRI <https://vocab.um.es> for any created entities. Do not write any explanation at the beginning or the end of the answer.
                    Not include individuals in the ontology."""}
                ]
            )
        out = completion.choices[0].message.content
        dicc[file] = out
        print('The ontology for the file',file, 'has been created.')
    return dicc

def save_ontologies_to_separate_files(data, output_folder):
    """
    Function to save each ontology from a dictionary into a separate OWL file in a specified output folder.
    Args:
        data: Dictionary where the keys are CSV file names and the values are ontologies in Turtle format.
        output_folder: The folder where the OWL files will be saved.
    """
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    for csv_file, ontology in data.items():
        output_file = os.path.join(output_folder, csv_file.replace('.csv', '.owl'))

        # Write the ontology to a separate file
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(ontology)

        print(f"The owl file {output_file} has been successfully created.")


def main(ft_model,input_folder,output_folder):
    results = get_openai_response(ft_model,input_folder)
    save_ontologies_to_separate_files(results, output_folder)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage python response_ft_ontobuilder.py ft_model input_folder output_folder")
    else:
        ft_model = sys.argv[1]
        input_folder = sys.argv[2]
        output_folder = sys.argv[3]
        main(ft_model,input_folder,output_folder)