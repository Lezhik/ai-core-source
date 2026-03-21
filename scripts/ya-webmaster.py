import requests
import json
from datetime import datetime

# ==========================
# НАСТРОЙКИ
# ==========================

config = json.load(open("ya-stat-config.json", "r", encoding="utf-8"))
TOKEN = config["token"]
FILE_NAME = "../stats/webmaster.json"

BASE_URL = "https://api.webmaster.yandex.net/v4"

headers = {
    "Authorization": f"OAuth {TOKEN}"
}

# ==========================
# 1. Получаем user_id
# ==========================

user_resp = requests.get(f"{BASE_URL}/user", headers=headers)

if user_resp.status_code != 200:
    print("Ошибка получения user_id")
    print(user_resp.text)
    exit()

user_id = user_resp.json()["user_id"]
print("User ID:", user_id)

# ==========================
# 2. Получаем список сайтов
# ==========================

hosts_resp = requests.get(f"{BASE_URL}/user/{user_id}/hosts", headers=headers)

if hosts_resp.status_code != 200:
    print("Ошибка получения сайтов")
    print(hosts_resp.text)
    exit()

hosts = hosts_resp.json()["hosts"]

if not hosts:
    print("Нет добавленных сайтов")
    exit()

# берем первый сайт
host_id = hosts[0]["host_id"]
host_name = hosts[0]["ascii_host_url"]

print("Выбран сайт:", host_name)

# ==========================
# 3. Получаем поисковые запросы
# ==========================

search_url = f"{BASE_URL}/user/{user_id}/hosts/{host_id}/search-queries/popular"

params = {
    "date_from": "2026-03-01",
    "date_to": "2026-03-17",
    "order_by": "TOTAL_SHOWS",
    "query_indicator": "TOTAL_SHOWS",
    "limit": 100
}

search_resp = requests.get(search_url, headers=headers, params=params)

if search_resp.status_code != 200:
    print("Ошибка получения поисковых запросов")
    print(search_resp.text)
    exit()

data = search_resp.json()

# ==========================
# 4. Сохранение в файл
# ==========================

with open(FILE_NAME, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Данные сохранены в:", FILE_NAME)