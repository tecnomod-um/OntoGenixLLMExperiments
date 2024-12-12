import os
import json

# For langchain and RAG
from langchain_community.document_loaders import DataFrameLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import pandas as pd
from langchain_community.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
persist_directory = "./chromedb"

def dataframe2prettyjson(dataframe: pd.DataFrame, file: str = None, save: bool = False) -> str:
    """
    Convert a Pandas DataFrame to pretty JSON and optionally save it to a file.

    Args:
        dataframe (pd.DataFrame): The input DataFrame.
        file (str): The file path to save the pretty JSON.
        save (bool): Whether to save the JSON to a file.

    Returns:
        str: The pretty JSON string representation.
    """
    try:
        json_data = dataframe.to_json(orient='index')
        parsed = json.loads(json_data)
        pretty_json = json.dumps(parsed, indent=4)

        if save and file:
            with open(file, 'w') as f:
                f.write(pretty_json)

        return pretty_json
    except json.JSONDecodeError as je:
        print(f"JSON Decode Error: {str(je)}")
    except ValueError as ve:
        print(f"Value Error: {str(ve)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        return ""
        

def read_txt_file_as_string (file_path): 
    with open(file_path, 'r') as file:
        file_content = file.read()
    
    return file_content


def rag_loader():  # Data preprocessing and split
    """
        Reads TTL ontology files from all text files in a specified directory and generates a DataFrame with a single column named 'output.'
        Each row of the DataFrame represents the content of an individual ontology file.
        The data is split.
    """
    # List to store the content of each ontology file
    ontologies = []
    directory_path = './ontologies_vs'

    # Iterate over all files in the directory
    for file in os.listdir(directory_path):
        if file.endswith(".txt"):  # Check if the file ends with .txt
            with open(os.path.join(directory_path, file), 'r', encoding='utf-8') as f:
                ontologies.append(f.read())

    # Create a DataFrame with the content
    df = pd.DataFrame({"output": ontologies})


    loader = DataFrameLoader(df, page_content_column="output")
    data = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    splits = text_splitter.split_documents(data)
    return splits
    
    
def save_chromedb(documents):
    """
        Include the embeddings into the target vector database, specifically Chroma DB in this case.
    """
    vectorstore = Chroma.from_documents(documents=documents, embedding=embeddings, persist_directory=persist_directory) # Use openAI embedding to get text vector 
    vectorstore.persist()
    print("Saved correctly")


def similarity_search_context(query):
    """
            A similarity search is performed based on the cosine similarity of the query performed and the top 4 results are returned.
    """
    vectordb = Chroma(persist_directory=persist_directory, embedding_function=embeddings) #Iniciate the chromadb with the directory of interest
    docs = vectordb.similarity_search(query, k=4)
    context = ""
    for document in docs:
        if document.page_content not in context:
            context = context + document.page_content + '\n'
    return context

