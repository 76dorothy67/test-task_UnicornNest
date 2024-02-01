import pandas as pd
import microcore as mc

mc.configure(
    # DOT_ENV_FILE='.env.test.anyscale-7b'
    DOT_ENV_FILE='.env.test.deepinfra.airoboros.llama-70b'
)

df_startups = pd.read_csv('startups_llama.csv')
df_startups['short_text'] = ""
df_startups['lama_response'] = ""

for index, row in df_startups.iterrows():
    main_page_text = row['Main Page']
    if isinstance(main_page_text, str):
        # Розділіть текст на слова
        words = main_page_text.split()
        # Обмежте кількість слів до 720
        limited_words = words[:720]
        # Об'єднайте слова назад у текст
        limited_text = ' '.join(limited_words)
        df_startups.at[index, 'short_text'] = limited_text

df_startups.to_csv('startups_llama.csv', index=False)

df_industries = pd.read_csv('industries.csv')
masters_industries = df_industries['Master industry'].tolist()
sub_sectors = df_industries['Sub-sectors (industries_formatted)'].tolist()

for index, row in df_startups.iterrows():
    mc.use_logging()
    startup_name = row['Name']
    main_page_text = row['short_text']

    mc.use_logging()
    about_response = mc.llm(f"""

        here is a name of startup: {startup_name}
        here is words from a main page of startup: {main_page_text}

        Describe what this startup is about.
        """)
    print(about_response)
    json_response = mc.llm(f"""

            here is a name of startup: {startup_name}
            this is a startup description: {about_response}

            here is master industries: {masters_industries}
            here is Sub-sectors: {sub_sectors}

            You need to determine the Sub-sectors of startups (choose one) and match the industry with the one of master industries.
            Give answer like:

            -Sub-sectors
            -Master industry (CHOOSE ONE)

            Give me answer json object, respond only with JSON object, no additional text
            """)
    df_startups.at[index, 'lama_response'] = json_response
    print(json_response)

df_startups.to_csv('startups_llama.csv', index=False)