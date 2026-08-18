import os
import json
import requests
from datetime import datetime

# Сервер GitHub автоматически подставит сюда ваши ключи из настроек "Secrets"
API_KEY = os.environ.get("YANDEX_API_KEY")
FOLDER_ID = os.environ.get("YANDEX_FOLDER_ID")

# Ключевые фразы для вашего клубного дома Elysium
KEYWORDS = [
    "купить пентхаус тбилиси",
    "элитная недвижимость тбилиси",
    "премиум квартиры тбилиси",
    "клубный дом тбилиси",
    "инвестиции в недвижимость грузия премиум",
    "купить квартиру элиа тбилиси",
    "luxury real estate tbilisi"
]

# Гео-ID Яндекса: 225 означает регион «Вся Россия»
REGIONS = [225]

def fetch_wordstat_data():
    """Функция обращается к Yandex Search API и забирает свежую семантику"""
    url = "https://yandex.net"
    
    headers = {
        "Authorization": f"Api-Key {API_KEY}",
        "x-folder-id": FOLDER_ID,
        "Content-Type": "application/json"
    }
    
    payload = {
        "phrases": KEYWORDS,
        "geoIds": REGIONS,
        "withRelatedPhrases": True  # Просим Яндекс прислать также и похожие запросы (правую колонку)
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Ошибка Яндекса: {response.status_code}, {response.text}")
            return None
    except Exception as e:
        print(f"Не удалось связаться с API: {e}")
        return None

def build_web_page(data):
    """Функция берет полученные данные и упаковывает их в HTML-страницу"""
    phrases_html = ""
    
    # Проверяем, пришли ли корректные данные от Яндекса
    if data and "phrases" in data:
        for item in data["phrases"]:
            phrase = item.get("phrase", "Unknown request")
            count = item.get("count", 0)
            
            # Формируем красивую карточку для каждого ключевого слова
            phrases_html += f"""
            <div class="keyword-card">
                <span class="phrase">{phrase}</span>
                <span class="count">{count:,} <span class="unit">показов/мес</span></span>
            </div>
            """
    else:
        # Текст ошибки, если API ключ не сработал или на балансе Яндекса нет баллов
        phrases_html = "<div class='error'>Данные от Yandex API не получены. Проверьте баланс или корректность ключей в Secrets.</div>"

    # Премиальный шаблон страницы в темных тонах под стиль бренда Elysium
    html_template = f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Elysium Real Estate | Дашборд Семантики РФ</title>
        <style>
            body {{ font-family: 'Helvetica Neue', Arial, sans-serif; background-color: #0e0e0e; color: #f5f5f7; margin: 0; padding: 40px 20px; }}
            .wrapper {{ max-width: 900px; margin: 0 auto; background: #16161a; padding: 40px; border-radius: 16px; border: 1px solid #2a2a30; }}
            h1 {{ color: #d4af37; font-size: 28px; font-weight: 300; letter-spacing: 1px; margin-top: 0; }}
            .subtitle {{ color: #8e8e93; font-size: 14px; margin-bottom: 30px; text-transform: uppercase; letter-spacing: 2px; }}
            .grid {{ display: flex; flex-direction: column; gap: 12px; }}
            .keyword-card {{ display: flex; justify-content: space-between; align-items: center; background: #1f1f24; padding: 18px 24px; border-radius: 8px; border-left: 4px solid #d4af37; transition: 0.2s; }}
            .keyword-card:hover {{ background: #26262c; }}
            .phrase {{ font-size: 16px; font-weight: 500; color: #ffffff; }}
            .count {{ font-size: 18px; font-weight: bold; color: #d4af37; }}
            .unit {{ font-size: 11px; color: #8e8e93; font-weight: normal; }}
            .error {{ color: #ff453a; background: rgba(255, 69, 58, 0.1); padding: 20px; border-radius: 8px; border: 1px solid #ff453a; }}
        </style>
    </head>
    <body>
        <div class="wrapper">
            <h1>ELYSIUM PREMIUM RESIDENCES</h1>
            <div class="subtitle">Мониторинг семантического ядра (РФ) • Обновлено: {datetime.now().strftime('%d.%m.%Y %H:%M')}</div>
            <div class="grid">
                {phrases_html}
            </div>
        </div>
    </body>
    </html>
    """
    
    # Записываем готовый код в файл index.html для публикации на GitHub Pages
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_template)

if __name__ == "__main__":
    raw_data = fetch_wordstat_data()
    build_web_page(raw_data)
