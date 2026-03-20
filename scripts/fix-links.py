import json
from pathlib import Path

# === КОНСТАНТЫ ===
JSON_ROOT = Path("../json")  # запуск из scripts

def load_json(path: Path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Ошибка чтения JSON {path}: {e}")
        return None


def save_json(path: Path, data: dict):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def clean_article_links():
    total_fixed_files = 0
    total_removed_links = 0

    # рекурсивно обходим все json
    for json_file in JSON_ROOT.rglob("*.json"):
        data = load_json(json_file)
        if not data:
            continue

        articles = data.get("articles")
        if not articles or not isinstance(articles, list):
            continue

        original_count = len(articles)
        valid_links = []

        for link in articles:
            if not isinstance(link, str):
                continue

            if not link.startswith("/json/"):
                continue

            # формируем путь
            target_path = Path("..") / link.lstrip("/")
            target_path = target_path.resolve()

            if target_path.exists():
                valid_links.append(link)
            else:
                print(f"Удалена битая ссылка: {json_file} -> {link}")
                total_removed_links += 1

        # если были изменения — сохраняем
        if len(valid_links) != original_count:
            data["articles"] = valid_links
            save_json(json_file, data)
            total_fixed_files += 1

    print("\n=== Результат ===")
    print(f"Файлов обновлено: {total_fixed_files}")
    print(f"Удалено ссылок: {total_removed_links}")

    if total_removed_links == 0:
        print("Битых ссылок не найдено.")
    else:
        print("Очистка завершена. Структура JSON приведена в порядок.")


if __name__ == "__main__":
    clean_article_links()