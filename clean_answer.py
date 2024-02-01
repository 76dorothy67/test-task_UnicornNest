import pandas as pd

# Завантажте датафрейми
df_startups = pd.read_csv('startups_llama.csv')
df_industries = pd.read_csv('industries.csv')

masters_industries = df_industries['Master industry'].tolist()
sub_sectors_raw = df_industries['Sub-sectors (industries_formatted)'].tolist()

# Функція для перевірки на NaN
def is_nan(value):
    return value != value

# Перетворення sub_sectors_raw на список списків, ігноруючи NaN
sub_sectors = [item.split(', ') for item in sub_sectors_raw if not is_nan(item)]

# Основний цикл для обробки df_startups
for index, row in df_startups.iterrows():
    master_industries_found = []
    sub_sectors_found = []
    llm_response = str(row['lama_response'])  # Переконайтеся, що llm_response є рядком

    # Пошук Master Industries
    for master_industry in masters_industries:
        if master_industry in llm_response:
            master_industries_found.append(master_industry)

    # Пошук Sub-sectors
    for sub_sector_group in sub_sectors:
        for sub_sector in sub_sector_group:
            if sub_sector in llm_response:
                sub_sectors_found.append(sub_sector)

    # Оновлення DataFrame
    df_startups.at[index, 'Master industry'] = master_industries_found
    df_startups.at[index, 'Industry'] = sub_sectors_found

# Збереження оновленого DataFrame
df_startups.to_csv('startups_llama.csv', index=False)
