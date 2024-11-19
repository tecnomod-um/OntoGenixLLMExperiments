from dotenv import dotenv_values #environment control
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
    if var == 'thread':
        return config['THREAD_ID']

def assistant_run(client, thread_id, assistant_id, file_path):
    """
    Use the assistant to launch a query using the vector store previously created with the files of interest.

    Args:
        file_path (str): File path to a specified prompt.
    """
    def read_prompt_file(file_path):
        """
        Function to read the prompt from the specified file path.
        """
        with open(file_path, 'r') as file:
            return file.read()

    prompt = read_prompt_file(file_path)

    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=prompt
    )

    # Create and poll the assistant run
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread_id, assistant_id=assistant_id
    )
    if run.status == "failed":
        print(f"Run failed with error: {run.last_error}")
    else:
        print("Run completed.")

    # Retrieve the list of messages from the run
    messages = list(client.beta.threads.messages.list(thread_id=thread_id, run_id=run.id))

    # Access and return the content of the first message
    message_content = messages[0].content[0].text
    return message_content.value

def save_ontology_as_owl(file_name, assistant_content):
    """
    Save the ontology content in Turtle format to an .owl file.

    Parameters:
        file_name (str): The name of the file to save the ontology. Defaults to 'ConsumerComplaintOntology.owl'.
        ontology_content (str):
    """

    # Open the file with write permissions
    with open(file_name, 'w', encoding="utf-8") as file:
        # Write the ontology content to the file
        file.write(assistant_content)

    print(f"The ontology has been saved as '{file_name}'")

def main(prompt_path,file_name):
    api_key = load_environment('key')
    client = OpenAI(api_key=api_key)
    assistant_id = load_environment('assistant')
    thread_id = load_environment('thread')
    ontology_content = assistant_run(client, thread_id, assistant_id, prompt_path)
    save_ontology_as_owl(file_name, ontology_content)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage python assistant_run.py prompt_path file_name")
    else:
        prompt_path = sys.argv[1]
        file_name = sys.argv[2]
        main(prompt_path,file_name)