import json
import requests
from bs4 import BeautifulSoup

url = "https://quotes.toscrape.com/"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
results = []

# Словарь для хранения данных об авторах
authors_data = {}

# Поиск всех элементов с классом "quote"
quote_blocks = soup.find_all(class_="quote")

# Извлечение данных из каждого блока
for item in quote_blocks:
    quote_text = item.find("span", class_="text").get_text(strip=True)
    author_name = item.find("small", class_="author").get_text(strip=True)
    author_bio_url = item.find("a")["href"]
    tags = [tag.get_text(strip=True) for tag in item.find_all("a", class_="tag")]

    # Проверка, есть ли автор уже в authors_data
    if author_name not in authors_data:
        # Получаем биографию автора
        author_bio_response = requests.get(url + author_bio_url)
        author_soup = BeautifulSoup(author_bio_response.text, "html.parser")
        author_details = author_soup.find("div", class_="author-details")
        
        # Извлечение биографической информации
        born_date = author_details.find("span", class_="author-born-date").get_text(strip=True)
        born_location = author_details.find("span", class_="author-born-location").get_text(strip=True)
        bio = author_details.find("div", class_="author-description").get_text(strip=True)
        
        # Добавляем автора и его биографию в authors_data
        authors_data[author_name] = {
            "born": f"{born_date} {born_location}",
            "bio": bio,
            "quotes": []  # Инициализация списка цитат для данного автора
        }

    # Добавляем цитату в список цитат автора
    authors_data[author_name]["quotes"].append({
        "quote": quote_text,
        "tags": tags
    })

# Преобразование authors_data в список для результатов
for author, data in authors_data.items():
    results.append({
        "author": author,
        "born": data["born"],
        "bio": data["bio"],
        "quotes": data["quotes"]
    })

# Печать результатов в формате JSON
print(json.dumps(results, indent=4, ensure_ascii=False))
