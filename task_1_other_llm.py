import pandas as pd
import microcore as mc
from articles import *
mc.configure(
    # DOT_ENV_FILE='.env.test.anyscale-7b'
    DOT_ENV_FILE='.env.test.deepinfra.airoboros.llama-70b'
)

df_articles = pd.read_csv('10__articles.csv')

df_articles['Answers_llama'] = ''


for i in range(len(df_articles)):

    mc.use_logging()
    json_response = mc.llm(f"""
    here is article {df_articles.loc[i, 'text']}.
    You need to extract the following data from this articles:

    Startup Name
    Funding Type (pre-seed, seed, series A, series B, etc.)
    Announced Date
    Industry 
    Money Raised (amount of money invested in the startup in this round)
    Valuation (if any)
    Revenue (if any)
    Investors
    Lead Investors (if any)
    Partner Investors (if any) (particular people who lead the round on behalf of the fund)

    Give me answer json object, respond only with JSON object, no additional text
    """)
    try:
        json_response = json_response.parse_json()
    except:
        # Обробка помилки, якщо відповідь не є коректним JSON
        print(f"Error parsing JSON for article {i}")
        json_response = {}  # Порожній словник у випадку помилки

    print(json_response)

    if not isinstance(json_response, str):
        json_response = str(json_response)

    df_articles.loc[i, 'Answers_llama'] = json_response


df_articles.head(10)
csv_file_path = '10__articles.csv'  # Вкажіть шлях до файлу
df_articles.to_csv(csv_file_path, index=False)