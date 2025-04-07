from openai import OpenAI #ChatGPT API
from dotenv import dotenv_values #environment control
import os #interact with the operating system
import sys #get the arguments for the script

def load_environment(): 
    """
    Load the API key of OpenAI from the environment.
    """
    config = dotenv_values(dotenv_path=".env")
    return config['OPENAI_API_KEY']

def prepare_data_ft(ft_data_path):
    """
    Upload the training and validation files to the OpenAI platform, indicating that the purpose is performing a fine-tuning job.

    Args:
        ft_data_path (str): Path to the folder containing the training and validation data.
    """
    api_key=load_environment()
    client = OpenAI(api_key=api_key)

    training_data = 'train_data.jsonl'
    validation_data = 'validation_data.jsonl'

    train_path = os.path.join(ft_data_path, training_data)
    validation_path = os.path.join(ft_data_path, validation_data)
    
    training_file_id = client.files.create(
    file=open(train_path, "rb"),
    purpose="fine-tune")

    validation_file_id = client.files.create(
    file=open(validation_path, "rb"),
    purpose="fine-tune")
    
    print(f"Training File ID: {training_file_id}")
    print(f"Validation File ID: {validation_file_id}")
    return client,training_file_id,validation_file_id

def create_job(ft_data_path, suffix):
  """
  Create the fine-tuning job with the selected model and the provided training and validation data.
  """
  client,training_file_id,validation_file_id = prepare_data_ft(ft_data_path)
  response = client.fine_tuning.jobs.create(
    training_file=training_file_id.id, 
    validation_file =validation_file_id.id,
    model= "gpt-3.5-turbo-0125", #model used for the fine-tuning job
    suffix= suffix, #suffix to identify the fine-tuned model
    hyperparameters={
    "n_epochs": 6,
    "batch_size": 3,
    "learning_rate_multiplier": 0.3
    }
  )
  job_id = response.id
  status = response.status
  print(f'Fine-tuning model with jobID: {job_id}.')
  print(f"Training Response: {response}")
  print(f"Training Status: {status}")
  return

def main(ft_data_path,suffix):
    create_job(ft_data_path,suffix) #launch the fine-tuning job

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage python ft_ontobuilder_creation.py input_folder suffix")
    else:
        ft_data_path = sys.argv[1]
        suffix = sys.argv[2]
        main(ft_data_path, suffix)





 