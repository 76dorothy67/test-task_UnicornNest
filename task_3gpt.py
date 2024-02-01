import pandas as pd
import microcore as mc

df_startups = pd.read_csv('startups.csv')
df_industries = pd.read_csv('industries.csv')

masters_industries = df_industries['Master industry'].tolist()
sub_sectors = df_industries['Sub-sectors (industries_formatted)'].tolist()

for index, row in df_startups.iterrows():
    mc.use_logging()
    startup_name = row['Name']
    main_page_text = row['Main Page']

    mc.use_logging()
    json_response = mc.llm(f"""
        
        here is a name of startup: {startup_name}
        here is a main page of startup: {main_page_text}
        
        here is master industries: {masters_industries}
        here is Sub-sectors: {sub_sectors}
        
        You need to determine the Sub-sectors of startups (can be more than one) and match the industry with the one of master industries. 
        Give answer like:
        
        -Sub-sectors
        -Master industry
        
        Give me answer json object, respond only with JSON object, no additional text
        """).parse_json()
    master_industry = json_response.get("Master industry", "")
    industry = ", ".join(json_response.get("Sub-sectors", []))

    # Запишіть значення у відповідні колонки
    df_startups.at[index, 'Master industry'] = master_industry
    df_startups.at[index, 'Industry'] = industry

    print(json_response)

df_startups.to_csv('startups.csv', index=False)