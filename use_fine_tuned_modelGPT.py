from openai import OpenAI
import pandas as pd
from dotenv import load_dotenv
import os

# Завантажуємо змінні середовища
load_dotenv()

client = OpenAI(
  api_key=os.environ['LLM_API_KEY'],
)

def response(fine_tuned_name, messages):
    response = client.chat.completions.create(
        model=fine_tuned_name,
        messages=messages
    )
    return response


def get_data(fine_tuned_name):
    df_articles = pd.read_csv('10__articles.csv')
    df_articles['Fine_Tuned_GPT'] = ''
    for i in range(len(df_articles)):

        messages = []
        first_line = {"role": "system", "content": "You are a chat bot that analyze text and extract some information from text."}
        question = {"role": "user", "content": df_articles.loc[i, 'text']}

        messages.append(first_line)
        messages.append(question)
        ai_response = response(fine_tuned_name, messages)
        ai_text_response = ai_response.choices[0].message.content  # Отримання текстового вмісту відповіді
        df_articles.loc[i, 'Fine_Tuned_GPT'] = ai_text_response

        print(ai_text_response)
    df_articles.to_csv('10__articles.csv', index=False)

if __name__ == "__main__":
    fine_tuned_model="name_model"
    get_data(fine_tuned_model)