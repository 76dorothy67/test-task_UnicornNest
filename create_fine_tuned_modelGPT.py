import pandas as pd
from openai import OpenAI
import json
from dotenv import load_dotenv
import os

# Завантажуємо змінні середовища
load_dotenv()
client = OpenAI(
  api_key=os.environ['LLM_API_KEY'],
)


def creat_list(df_articles):
    print(len(df_articles))
    for i in range(len(df_articles)):
        prompt = []
        first_line = {"role": "system", "content": "You are a chat bot that analyze text and extract some information from text."}
        dic_1 = {"role": "user", "content": f"Here is an article {df_articles.loc[i, 'text']}"
        }
        dic_2 = {"role": "assistant", "content": df_articles.loc[i, 'labeled_data']}
        prompt.append(first_line)
        prompt.append(dic_1)
        prompt.append(dic_2)
        result = {'messages': prompt}
        with open('prompts.jsonl', 'a', encoding='utf-8') as file:
            json.dump(result, file)
            file.write(f"\n")

training_file_name = "training_data.jsonl"
validation_file_name = "validation_data.jsonl"


def upload_training_file(file_name):
    training_file_id = client.files.create(
        file=open(training_file_name, "rb"),
        purpose="fine-tune"
    )
    return training_file_id


def create_fine_tuned_model(file_id):
    client.fine_tuning.jobs.create(
        training_file=file_id,
        model="gpt-3.5-turbo"
    )

if __name__ == "__main__":
    df_articles = pd.read_csv('20_articles.csv')
    creat_list(df_articles)

    training_file_id = upload_training_file("prompts.jsonl").id
    print(f"Training File ID: {training_file_id}")

    create_fine_tuned_model(training_file_id)
    #print(client.fine_tuning.jobs.retrieve(training_file_id))