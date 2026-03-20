import json
from pathlib import Path

# === КОНСТАНТЫ ===
JSON_ROOT = Path("../json")
MAX_ARTICLES = 18


def load_json(path: Path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Ошибка чтения {path}: {e}")
        return None


def save_json(path: Path, data: dict):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def trim_articles(json_file: Path):
    data = load_json(json_file)
    if not data:
        return False

    articles = data.get("articles")
    if not articles or not isinstance(articles, list):
        return False

    if len(articles) <= MAX_ARTICLES:
        return False

    original_len = len(articles)

    # удаляем первые (самые старые)
    trimmed_articles = articles[-MAX_ARTICLES:]

    data["articles"] = trimmed_articles
    save_json(json_file, data)

    print(f"{json_file}: {original_len} -> {len(trimmed_articles)} (обрезано {original_len - len(trimmed_articles)})")
    return True


def main():
    updated_files = 0

    # 1. Главная
    main_index = JSON_ROOT / "index.json"
    if trim_articles(main_index):
        updated_files += 1

    # 2. Только категории (../json/*/index.json)
    for category_dir in JSON_ROOT.iterdir():
        if not category_dir.is_dir():
            continue

        category_index = category_dir / "index.json"
        if category_index.exists():
            if trim_articles(category_index):
                updated_files += 1

    print("\n=== Результат ===")
    print(f"Обновлено файлов: {updated_files}")


if __name__ == "__main__":
    main()