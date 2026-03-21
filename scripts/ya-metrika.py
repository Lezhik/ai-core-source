import requests
import json

## получение токена
## - Открыть ссылку: https://oauth.yandex.ru/authorize?response_type=token&client_id=f85e39d58a9841648a842f88e861ffb6
## - Разрешить доступ
## - Получить токен: AQAAAABCD123456...

# ===== настройки =====
config = json.load(open("ya-stat-config.json", "r", encoding="utf-8"))
TOKEN = config["token"]
COUNTER_ID = config["counterId"]

API_URL  = "https://api-metrika.yandex.net/stat/v1/data"
FILE_NAME = "../stats/metrika.json"


# ==========================
# ПАРАМЕТРЫ СТАТИСТИКИ
# ==========================

params = {
    "ids": COUNTER_ID,

    "metrics": ",".join([
        "ym:s:visits",
        "ym:s:users",
        "ym:s:pageviews",
        "ym:s:bounceRate",
        "ym:s:avgVisitDurationSeconds"
    ]),

    "dimensions": ",".join([
        "ym:s:date",
        "ym:s:trafficSource",
        "ym:s:deviceCategory",
        "ym:s:browser"
    ]),

    "date1": "7daysAgo",
    "date2": "today",
    "limit": 10000,
    "accuracy": "full"
}

headers = {
    "Authorization": f"OAuth {TOKEN}"
}

# ==========================
# ЗАПРОС
# ==========================

response = requests.get(API_URL, headers=headers, params=params)

if response.status_code != 200:
    print("Ошибка API:", response.status_code)
    print(response.text)
    exit()

data = response.json()

# ==========================
# СОХРАНЕНИЕ В ФАЙЛ
# ==========================

with open(FILE_NAME, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Статистика сохранена в файл:", FILE_NAME)