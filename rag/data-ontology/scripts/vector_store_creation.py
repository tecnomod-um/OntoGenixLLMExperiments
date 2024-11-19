from dotenv import dotenv_values, set_key #environment control
import os # to iterate over directories
from openai import OpenAI #ChatGPT API
import sys #get the arguments for the script

def load_environment(var):
    """
    Get the environment variables.

    Args:
        var (str): Variable to be retrieved from the environment.
    """
    config = dotenv_values(dotenv_path=".env")
    if var == 'key':
        return config['OPENAI_API_KEY']
    if var == 'assistant':
        return config['ASSISTANT_ID']

def get_file_streams_from_directory(directory):
    """
    Iterates over the directory and filter files ending with '.txt' and stores the file streams in a list.
    """
    # List to store the file paths
    file_paths = []

    # Iterate over the directory and filter files ending with '_ontology.txt'
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            file_paths.append(os.path.join(directory, filename))

    # Open the files in binary mode ('rb') and store the streams in a list
    file_streams = [open(path, "rb") for path in file_paths]

    return file_streams

def vector_store_creation(client,name,directory):
    """
    Creates a vector store with the file streams of the documents, which will serve as an additional knowledge-base.

    Args:
        name (str): Name of the vector store.
        directory (str): Path to the folder where the ontologies to use as a reference are stored in txt format.
    """

    vector_store = client.beta.vector_stores.create(name=name)
    file_streams = get_file_streams_from_directory(directory)

    file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
        vector_store_id=vector_store.id, files=file_streams
    )

    print("Status of the batch:", file_batch.status)
    print("File count of the batch:", file_batch.file_counts)
    return vector_store.id

def update_assistant_vectorstore(client, vector_store_id):
    """
    Updates the assistant with the new vector store.

    Args:
        vector_store_id (str): ID of the vector store.
    """
    assistant_id = load_environment('assistant')
    assistant = client.beta.assistants.update(
        assistant_id=assistant_id,
        tool_resources={"file_search": {"vector_store_ids": [vector_store_id]}},
    )
    print('Assistant Updated with vector store')

def thread_creation(client):
    """
    Creation of a new thread where all the messages are stored and which is associated with a thread.
    """
    thread = client.beta.threads.create()
    dotenv_path = '.env'
    set_key(dotenv_path, 'THREAD_ID', thread.id)
    print(f"THREAD_ID saved in .env: {thread.id}")


def main(vector_store_name, input_folder):
    api_key = load_environment('key')
    client = OpenAI(api_key=api_key)
    vector_store_id = vector_store_creation(client,vector_store_name,input_folder)
    update_assistant_vectorstore(client,vector_store_id)
    thread_creation(client)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage python vector_store_creation.py vector_store_name input_folder")
    else:
        vector_store_name = sys.argv[1]
        input_folder = sys.argv[2]
        main(vector_store_name,input_folder)