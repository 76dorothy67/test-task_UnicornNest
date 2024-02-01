import pandas as pd
import microcore as mc

df_articles = pd.read_csv('10__articles.csv')

df_articles['Answers_GPT'] = ''


for i in range(len(df_articles)):

    mc.use_logging()
    json_response = mc.llm(f"""
    here is an article {df_articles.loc[i, 'text']}.
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
    """).parse_json()

    print(json_response)
    if not isinstance(json_response, str):
        json_response = str(json_response)

    df_articles.loc[i, 'Answers_GPT'] = json_response


df_articles.head(10)
csv_file_path = '10__articles.csv'  # Вкажіть шлях до файлу
df_articles.to_csv(csv_file_path, index=False)