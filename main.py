import json
import requests
from bs4 import BeautifulSoup

base_url = "https://quotes.toscrape.com/"
page_number = 1
results = []
authors_data = {}

while True:
    # Формируем URL для текущей страницы
    url = f"{base_url}page/{page_number}/"
    response = requests.get(url)

    print(f"We get the data from the link: {url}")
    
    # Проверка, если страница не найдена (404), то прерываем цикл
    if response.status_code == 404:
        print(f"Page {page_number} not found, stop parsing.")
        break
    
    # Парсим контент страницы
    soup = BeautifulSoup(response.text, "html.parser")

    # Поиск всех цитат на странице
    quote_blocks = soup.find_all(class_="quote")

    if not quote_blocks:
        print(f"There are no quotes on page {page_number}, stop parsing.")
        break


    # Извлечение данных из каждого блока цитат
    for item in quote_blocks:
        quote_text = item.find("span", class_="text").get_text(strip=True)
        author_name = item.find("small", class_="author").get_text(strip=True)
        author_bio_url = item.find("a")["href"]
        tags = [tag.get_text(strip=True) for tag in item.find_all("a", class_="tag")]

        # Проверка, если автор уже добавлен
        if author_name not in authors_data:
            author_bio_response = requests.get(base_url + author_bio_url)
            author_soup = BeautifulSoup(author_bio_response.text, "html.parser")
            author_details = author_soup.find("div", class_="author-details")
            
            born_date = author_details.find("span", class_="author-born-date").get_text(strip=True)
            born_location = author_details.find("span", class_="author-born-location").get_text(strip=True)
            bio = author_details.find("div", class_="author-description").get_text(strip=True)
            
            # Добавляем автора в authors_data с разделением на born_date и born_location
            authors_data[author_name] = {
                "born_date": born_date,
                "born_location": born_location,
                "bio": bio,
                "quotes": []
            }

        # Добавляем цитату к автору
        authors_data[author_name]["quotes"].append({
            "quote": quote_text,
            "tags": tags
        })

    # Переход к следующей странице
    page_number += 1

# Преобразование authors_data в список для результатов
for author, data in authors_data.items():
    results.append({
        "author": author,
        "born_date": data["born_date"],
        "born_location": data["born_location"],
        "bio": data["bio"],
        "quotes": data["quotes"]
    })


# Запись результатов в JSON-файл
with open("quotes.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=4, ensure_ascii=False)