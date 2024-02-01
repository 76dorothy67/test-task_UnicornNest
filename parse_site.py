import pandas as pd
import requests
from bs4 import BeautifulSoup

# Завантажте ваш CSV файл у DataFrame
csv_file_path = 'startups_llama.csv'
df = pd.read_csv(csv_file_path)

# Функція для отримання тексту першої сторінки сайту
def get_main_page_text(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Отримайте текст першої сторінки
            main_page_text = soup.get_text()
            return main_page_text
        else:
            return None
    except Exception as e:
        print(f"Помилка: {e}")
        return None

# Застосуйте функцію до стовпця 'Link' і створіть новий стовпець 'Main Page'
df['Main Page'] = df['Link'].apply(get_main_page_text)

# Збережіть оновлений DataFrame у той же CSV файл
df.to_csv(csv_file_path, index=False)

print("Розпарсено і збережено текст перших сторінок сайтів.")
