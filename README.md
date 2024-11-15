# Анализ задачи по парсингу цитат

## Описание задачи

Целью задачи является сбор цитат с сайта [Quotes to Scrape](https://quotes.toscrape.com/) и сохранение полученных данных в формате JSON. Данные включают цитаты, имена авторов, их биографическую информацию (дату и место рождения), а также теги, связанные с цитатами.

## Что было сделано

1. **Парсинг данных с нескольких страниц**: Скрипт был разработан для парсинга цитат с нескольких страниц сайта. Он автоматически обходит все страницы с цитатами, начиная с первой и продолжая до последней странице с цитатами, пока не встретится страница, где цитаты отсутствуют.

2. **Сбор информации о цитатах**: Для каждой цитаты были извлечены следующие данные:
   - Текст цитаты
   - Имя автора
   - Биографическая информация об авторе (дата и место рождения, краткое описание)
   - Теги, связанные с цитатой

3. **Автоматическое добавление авторов**: Если автор еще не был добавлен в сбор данных, скрипт автоматически собирает его биографическую информацию (дату и место рождения, описание) и добавляет этого автора в структуру данных.

4. **Сохранение данных в JSON**: Все собранные данные о цитатах и авторах были сохранены в файл `quotes.json` в формате JSON. Файл включает в себя информацию о каждом авторе и его цитатах.

5. **Обработка ошибок**: Реализована обработка ошибок для страниц с кодами ответа 404 (страница не найдена) и 304 (не было изменений на странице), а также для случаев отсутствия цитат на страницах.

## Откуда были получены данные

Данные были получены с веб-сайта [Quotes to Scrape](https://quotes.toscrape.com/), который предоставляет публично доступные цитаты с именами авторов, их биографической информацией и тегами.

## Как осуществлялся сбор данных

1. **HTTP-запросы с использованием библиотеки `requests`**:
   Для получения HTML-кода страниц использовалась библиотека `requests`. Скрипт отправляет запросы к страницам с цитатами (например, https://quotes.toscrape.com/page/1/), последовательно увеличивая номер страницы. Каждый запрос получает HTML-код страницы.

2. **Парсинг HTML с использованием `BeautifulSoup`**:
   После получения HTML-кода, данные на странице извлекаются с помощью библиотеки `BeautifulSoup`. Мы ищем все элементы с классом `"quote"` для извлечения цитат. Для каждой цитаты также извлекаются имя автора, ссылка на его биографию и связанные с цитатой теги.

3. **Обработка ссылок на страницы авторов**:
   Для авторов, чьи биографии были необходимы, из ссылки на биографию извлекалась дополнительная информация (дата и место рождения, краткое описание). Если автор еще не был добавлен в структуру данных, скрипт автоматически собирает его биографию и добавляет его информацию в список авторов.

4. **Автоматическое добавление новых авторов**:
   Если автор встречается впервые, его биография и цитаты автоматически добавляются в структуру данных, создавая для него отдельную запись с информацией о дате и месте рождения, а также с его цитатами.

5. **Остановка при отсутствии цитат**:
   Скрипт проверяет, есть ли на странице цитаты. Если на странице нет цитат, сбор данных прекращается. Также скрипт завершает работу при получении кода ответа 404 (страница не найдена).

## Почему был выбран тот или иной метод/инструмент, а не другой

1. **Библиотека `requests`**:
   `requests` была выбрана для отправки HTTP-запросов, потому что она является одной из самых популярных и простых в использовании библиотек для работы с HTTP в Python. Она поддерживает все необходимые методы HTTP и имеет удобный интерфейс для получения и работы с ответами от сервера.

2. **Библиотека `BeautifulSoup`**:
   Для парсинга HTML использовалась библиотека `BeautifulSoup`, так как она эффективно извлекает данные из HTML-документов. `BeautifulSoup` предоставляет мощные функции для навигации по DOM-дереву и извлечения нужных данных с минимальными усилиями. Альтернативы, такие как `lxml`, были бы избыточными для данной задачи.

3. **Формат данных JSON**:
   Для сохранения данных был выбран формат JSON, потому что он является универсальным и легко читаемым форматом, который широко используется для обмена данными между различными приложениями. JSON также позволяет легко работать с данными в Python.

4. **Автоматическое добавление авторов**:
   Автоматическое добавление авторов было выбрано для упрощения работы с данными. Когда встречается новый автор, его информация сразу добавляется в базу данных, что делает процесс парсинга удобным и автоматизированным.

5. **Остановка при отсутствии цитат**:
   Решение прекратить сбор данных при отсутствии цитат на странице и при получении кода 404 основано на логике, что сайт не имеет бесконечного количества страниц с цитатами. Как только страницы с цитатами заканчиваются, сбор данных становится бесполезным.

## Как использовать

1. Убедитесь, что у вас установлен Python 3.x.
2. Установите необходимые библиотеки:
   ```bash
   pip install requests beautifulsoup4
