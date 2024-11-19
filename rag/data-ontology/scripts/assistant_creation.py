from openai import OpenAI #ChatGPT API
from dotenv import dotenv_values, set_key #environment control

def load_environment(var):
    """
    Get the environment variables.

    Args:
        var (str): Variable to be retrieved from the environment.
    """
    config = dotenv_values(dotenv_path=".env")
    if var == 'key':
        return config['OPENAI_API_KEY']

def assistant_creation():
    """
    Creation of an assistant with File Search enabled using the GPT-4o and store the assistant ID in the .env file.
    """
    api_key=load_environment('key')
    client = OpenAI(api_key=api_key)

    instructions = """
        You're an ontology expert with more than 12 years of experience in the field. 
        Your main purpose is to assist the user in assigning to each column of a CSV file an IRI corresponding to a class of the ontologies in TTL format contained in your vector store.
        For each column, try to identify which class of the ontologies included in your vector store, matches with the name of the column, following the next format:
        <column_name>: <insert IRI match class> <name of the match class> <ontology from which the class comes>
        If there is not a class that matches the name of the column, the format will be the next:
        <column_name>: No match available.
        Just use the ontologies contained in your vector store.
        Do not write notes at the end of your writing.
    """

    assistant = client.beta.assistants.create(
      name="Ontology Instantiation Assistant",
      instructions=instructions,
      model="gpt-4o",
      tools=[{"type": "file_search"}],
    )

    dotenv_path = ".env"
    set_key(dotenv_path, 'ASSISTANT_ID', assistant.id)

def main():
    assistant_creation()

if __name__ == "__main__":
    main()