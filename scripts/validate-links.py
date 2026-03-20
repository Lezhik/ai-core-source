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


def check_article_links():
    errors_found = False

    # рекурсивно обходим все json
    for json_file in JSON_ROOT.rglob("*.json"):
        data = load_json(json_file)
        if not data:
            continue

        # проверяем наличие блока articles
        articles = data.get("articles")
        if not articles:
            continue

        # проверяем что это список строк
        if not isinstance(articles, list):
            print(f"{json_file}: поле articles не является списком")
            errors_found = True
            continue

        for link in articles:
            if not isinstance(link, str):
                print(f"{json_file}: некорректная ссылка (не строка): {link}")
                errors_found = True
                continue

            # ссылки вида /json/ai-blog/... -> ../json/ai-blog/...
            if not link.startswith("/json/"):
                print(f"{json_file}: ссылка не из /json: {link}")
                errors_found = True
                continue

            target_path = Path("..") / link.lstrip("/")
            target_path = target_path.resolve()

            if not target_path.exists():
                print(f"{json_file}: {link}, не найдена.")
                errors_found = True

    # финальное сообщение
    if errors_found:
        print("\nОбнаружены ошибки в ссылках JSON.")
        print("Рекомендуется откатить репозиторий.\n")

        print("Команды для Windows (выполняются без подтверждения):")
        print("git revert --no-edit $(git rev-list --max-count=1 HEAD)")
        print("git clean -fd")
    else:
        print("Проверка завершена: ошибок не найдено.")


if __name__ == "__main__":
    check_article_links()