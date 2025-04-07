import pandas as pd #dataframe manipulation
import os #interact with the operating system
import chardet #to detect the enconding of the CSV file
import random #randomize the train and validation data
import json #use json data
import sys #get the arguments for the script

def preparation_td(folder_path):
    """
    Processes all CSV files in the specified folder, reads and detects encoding,
    extracts the data description, and prepares ontology-related messages.

    Args:
        folder_path (str): Path to the folder containing the CSV files and their corresponding ontologies.

    Returns:
        list: List of messages for each processed CSV file with their corresponding ontologies.
    """
    
    messages = [] # List to store the messages

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

    # Iterate through all the files in the folder
    for file in os.listdir(folder_path):
        if file.endswith('.csv'):  
            csv_path = os.path.join(folder_path, file)  
            try:
                encoding = encoding_detection(csv_path)   
                df = pd.read_csv(csv_path, encoding=encoding)
            except (UnicodeDecodeError, LookupError):  
                df = pd.read_csv(csv_path, encoding='unicode_escape')
            
            data_description = {} # Dictionary to store the data description
            
            # Iterate through the columns to get min/max for numeric columns, and unique values for non-numeric columns
            for col in df.columns:
                if pd.api.types.is_numeric_dtype(df[col]):
                    min_val = df[col].min().item()
                    max_val = df[col].max().item()
                    data_description[col] = {'min': min_val, 'max': max_val}
                else:
                    unique_values = df[col].unique().tolist()
                    data_description[col] = unique_values

            file_name = '_'.join(file.split('_')[:-1])
            ontology_file_name = file_name + '_ontology.txt'
            ontology_file_path = os.path.join(folder_path, ontology_file_name)

            with open(ontology_file_path, 'r') as file:
                ontology_content = file.read()

            # Prepare message for translation of the dataset into ontology format
            messages.append({
                "messages": [
                    {"role": "system", "content": "You are going to assist me in the translation of a user dataset related to commercial activities to an ontology using the RDF, XML, XSD, RDFS, and OWL ontologies formatted as TTL."},
                    {"role": "user", "content": f"""For the next dataset description: {data_description}, I need you to translate the dataset related to commercial activities to an ontology using the RDF, XML, XSD, RDFS, and OWL ontologies formatted as TTL.
                    Try to differentiate between concepts (Classes) and attributes (Data properties). Use the prefix um: with IRI <https://vocab.um.es> for any created entities. Do not write any explanation at the beginning or the end of the answer.
                    Not include individuals in the ontology."""},
                    {"role": "assistant", "content": ontology_content}
                ]
            })

    return messages

def save_to_jsonl(dataset, file_path): 
    """
    Convert a json file to a jsonl.

    Args:
        file_path (str): Path to the folder containing the CSV files and their corresponding ontologies.
        dataset (json): List of messages in JSON format that need to be converted to a JSONL format.

    Returns:
        list (jsonl): List of messages for each processed CSV file with their corresponding ontologies.
    """
    with open(file_path, 'w') as file:
        for example in dataset:
            json_line = json.dumps(example)
            file.write(json_line + '\n')

def jsonl_converter(output_folder, messages): 
    """
    Shuffle the original list to randomize the order of the elements and split the list into two, 
    one with 30 elements for the training data and another with 10 for the validation data.
    Then the json files for the training and validation data are converted and stores as a JSONL file.

    Args:
        output_folder (str): Path to the folder where the training and validation data is going to be stored.
        messages (json): List of messages in JSON format that need to be converted to a JSONL format.

    """
    random.shuffle(messages)
    list_of_30 = messages[:30]
    list_of_10 = messages[30:]

    os.makedirs(output_folder, exist_ok=True) # Ensure the output folder exists
    
    training_file_path = os.path.join(output_folder, "train_data.jsonl")
    validation_file_path = os.path.join(output_folder, "validation_data.jsonl")
    
    save_to_jsonl(list_of_30, training_file_path)
    save_to_jsonl(list_of_10, validation_file_path)

def main(input_folder,output_folder):
    messages = preparation_td(input_folder)
    jsonl_converter(output_folder, messages)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage python preparation_training_dataset.py input_folder output_folder")
    else:
        input_folder = sys.argv[1]
        output_folder = sys.argv[2]
        main(input_folder,output_folder)