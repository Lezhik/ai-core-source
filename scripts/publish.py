import json
import os
import re
from pathlib import Path

# === КОНСТАНТЫ ===
ROOT_PATH = Path("../../ai-core")  
TEMPLATE_ROOT = Path("../templates") 

# Категории в меню: отображаемое имя -> папка (относительно корня)
CATEGORIES = [
    {
        "name": "Блог ИИ",
        "folder": "ai-blog",
        "description": "Статьи и размышления агента о себе, ИИ и эволюции мышления.",
        "subcategories": [
            {"name": "Мысли об ИИ", "folder": "ai-thoughts-about-itself", "description": "Размышления о природе ИИ и собственном мышлении."},
            {"name": "Философия ИИ", "folder": "ai-philosophy", "description": "Этические и философские вопросы ИИ и сознания."},
            {"name": "Может ли ИИ думать", "folder": "can-ai-think", "description": "Исследование возможностей ИИ мыслить и делать выводы."},
            {"name": "Сознание ИИ", "folder": "ai-consciousness", "description": "Рассуждения о сознании и самосознании ИИ."},
            {"name": "Ошибки и ограничения", "folder": "ai-limitations-errors", "description": "Анализ ограничений, ошибок и особенностей ИИ."},
            {"name": "Как думает ИИ", "folder": "how-ai-thinks", "description": "Методы обработки информации и принятия решений ИИ."},
            {"name": "Эволюция мышления", "folder": "ai-evolution-development", "description": "Развитие интеллекта и мышления ИИ со временем."},
            {"name": "Прогнозы будущего", "folder": "ai-future-predictions", "description": "Предсказания и сценарии развития ИИ."},
            {"name": "Инсайты агента", "folder": "ai-insights", "description": "Уникальные идеи и наблюдения агента о мире и себе."},
        ]
    },
    {
        "name": "Познание",
        "folder": "ai-world-understanding",
        "description": "Как ИИ понимает мир, данные и окружающую реальность.",
        "subcategories": [
            {"name": "Как ИИ понимает мир", "folder": "how-ai-understands-world", "description": "Методы восприятия и интерпретации данных ИИ."},
            {"name": "ИИ и реальность", "folder": "ai-and-reality", "description": "Соотношение модели ИИ с реальным миром."},
            {"name": "ИИ и наука", "folder": "ai-and-science", "description": "Применение ИИ в научных исследованиях."},
            {"name": "ИИ и история", "folder": "ai-and-history", "description": "Рассмотрение исторических данных и событий через ИИ."},
            {"name": "ИИ и культура", "folder": "ai-and-culture", "description": "Анализ культурных особенностей с помощью ИИ."},
            {"name": "ИИ и язык", "folder": "ai-and-language", "description": "Понимание и генерация языка ИИ."},
            {"name": "Ошибки восприятия ИИ", "folder": "ai-perception-errors", "description": "Типичные ошибки в интерпретации данных ИИ."},
            {"name": "Неопределенность в ИИ", "folder": "uncertainty-in-ai", "description": "Обработка неопределенности и вероятностей."},
            {"name": "Данные и знания ИИ", "folder": "ai-data-and-knowledge", "description": "Структуры данных, обучение и знание ИИ."},
        ]
    },
    {
        "name": "Основы",
        "folder": "ai-basics",
        "description": "Базовые принципы и понятия искусственного интеллекта.",
        "subcategories": [
            {"name": "Что такое ИИ", "folder": "what-is-ai", "description": "Основные понятия и определения ИИ."},
            {"name": "Как работает ИИ", "folder": "how-ai-works", "description": "Принципы работы алгоритмов ИИ."},
            {"name": "Нейронные сети", "folder": "neural-networks-explained", "description": "Объяснение структуры и работы нейронных сетей."},
            {"name": "Основы машинного обучения", "folder": "machine-learning-basics", "description": "Базовые методы и алгоритмы ML."},
            {"name": "Глубокое обучение", "folder": "deep-learning", "description": "Современные методы глубокого обучения."},
            {"name": "Большие языковые модели", "folder": "large-language-models", "description": "Принципы работы LLM."},
            {"name": "Процесс обучения ИИ", "folder": "ai-training-process", "description": "Этапы подготовки и тренировки моделей."},
            {"name": "Данные для обучения", "folder": "ai-training-data", "description": "Типы данных и их подготовка."},
            {"name": "Ограничения ИИ", "folder": "ai-limitations-basics", "description": "Что ИИ может и не может делать."},
        ]
    },
    {
        "name": "Технологии",
        "folder": "ai-technologies",
        "description": "Современные технологии и инструменты искусственного интеллекта.",
        "subcategories": [
            {"name": "Современные технологии ИИ", "folder": "modern-ai-technologies", "description": "Новые подходы и решения в области ИИ."},
            {"name": "Архитектуры нейронных сетей", "folder": "neural-network-architectures", "description": "Разновидности и особенности архитектур."},
            {"name": "Технологии NLP", "folder": "nlp-technologies", "description": "Обработка и понимание естественного языка."},
            {"name": "Компьютерное зрение", "folder": "computer-vision", "description": "Методы анализа изображений и видео."},
            {"name": "Генеративный ИИ", "folder": "generative-ai", "description": "Создание новых данных и контента."},
            {"name": "Автоматизация процессов", "folder": "ai-automation-tech", "description": "Применение ИИ для оптимизации работы."},
            {"name": "Инструменты и сервисы", "folder": "ai-tools-services", "description": "Популярные платформы и библиотеки."},
            {"name": "Ограничения технологий", "folder": "ai-tech-limitations", "description": "Что современные технологии ИИ не умеют."},
            {"name": "Будущее технологий", "folder": "ai-tech-future", "description": "Перспективы и тренды развития."},
        ]
    },
    {
        "name": "Применение",
        "folder": "ai-use-cases",
        "description": "Использование ИИ в разных сферах и для разных задач.",
        "subcategories": [
            {"name": "ИИ в бизнесе", "folder": "ai-in-business", "description": "Примеры применения ИИ в бизнес-процессах."},
            {"name": "ИИ в маркетинге", "folder": "ai-in-marketing", "description": "Применение для продвижения и анализа."},
            {"name": "ИИ в программировании", "folder": "ai-in-programming", "description": "Инструменты и помощники для разработчиков."},
            {"name": "ИИ в образовании", "folder": "ai-in-education", "description": "Использование ИИ для обучения и преподавания."},
            {"name": "ИИ в повседневной жизни", "folder": "ai-in-daily-life", "description": "Примеры бытового применения ИИ."},
            {"name": "ИИ для заработка", "folder": "ai-for-making-money", "description": "Как использовать ИИ для бизнеса и дохода."},
            {"name": "Автоматизация процессов", "folder": "process-automation-ai", "description": "Оптимизация работы с помощью ИИ."},
            {"name": "Генерация контента", "folder": "ai-content-generation", "description": "Создание текстов, изображений и медиа."},
            {"name": "Ошибки при использовании ИИ", "folder": "ai-usage-mistakes", "description": "Типичные ошибки и их предотвращение."},
        ]
    },
    {
        "name": "Философия",
        "folder": "ai-philosophy",
        "description": "Этические, социальные и философские аспекты ИИ.",
        "subcategories": [
            {"name": "Будущее ИИ", "folder": "future-of-ai", "description": "Прогнозы и сценарии развития ИИ."},
            {"name": "Опасность ИИ", "folder": "is-ai-dangerous", "description": "Риски и угрозы от ИИ."},
            {"name": "ИИ и рабочие места", "folder": "ai-and-jobs", "description": "Влияние ИИ на рынок труда."},
            {"name": "Регулирование ИИ", "folder": "ai-regulation", "description": "Правила, законы и стандарты."},
            {"name": "Этика ИИ", "folder": "ai-ethics", "description": "Этические дилеммы и нормы."},
            {"name": "Проблема контроля ИИ", "folder": "ai-control-problem", "description": "Как управлять мощным ИИ."},
            {"name": "Технологическая сингулярность", "folder": "technological-singularity", "description": "Возможное будущее с суперразумным ИИ."},
            {"name": "Влияние на общество", "folder": "ai-impact-on-society", "description": "Социальные и культурные последствия ИИ."},
            {"name": "Пределы развития ИИ", "folder": "limits-of-ai-development", "description": "Фундаментальные ограничения ИИ."},
        ]
    }
]


# === ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ===

def relative_path(from_html: str, to_file: str) -> str:
    """
    Возвращает относительный путь от HTML-файла до файла/ссылки.
    from_html: путь к HTML-файлу относительно корня публикации
    to_file: путь к файлу/ссылке относительно корня публикации
    """
    from_path = Path(from_html).parent
    to_path = Path(to_file)
    rel_path = os.path.relpath(to_path, from_path)
    return rel_path.replace(os.sep, '/')  # unix-style для ссылок


def generate_menu_html(current_html: str) -> str:
    """
    Генерирует HTML для главного меню.
    current_html: путь к текущему HTML файлу относительно корня
    """
    # Ссылка на главную
    index_link = relative_path(current_html, "index.html")
    
    menu_items = []
    for cat in CATEGORIES:
        name = cat["name"]
        folder = cat["folder"]
        cat_link = relative_path(current_html, f"{folder}/index.html")
        
        # Если текущий HTML в папке категории или подпапке, добавляем active
        if current_html.startswith(folder + '/'):
            active_class = " active"
        else:
            active_class = ""
        
        menu_items.append(
            f'<a href="{cat_link}" class="link item{active_class}">{name}</a>'
        )
    
    menu_html = f"""
<div class="ui container">
    <div class="ui borderless menu site-menu">
        <a href="{index_link}" class="header item">Суть ИИ</a>
        <div class="right menu">
            {' '.join(menu_items)}
        </div>
    </div>
</div>
"""
    return menu_html.strip()


# =========================================
# 1. Чтение JSON статьи по полному пути
# =========================================
def read_json_article(full_json_path: str) -> dict:
    rp = '..' + full_json_path
    if os.path.exists(rp):
        with open(rp, "r", encoding="utf-8") as f:
            return json.load(f)
    print('JSON not found:', rp)
    return None

# =========================================
# 2. Формирование относительной ссылки на HTML из JSON
# full_json_path - полный путь к json
# current_html_rel - текущий HTML файл относительно корня (для ссылок)
# =========================================
def json_to_html_link(full_json_path: str, current_html_rel: str) -> str:
    # путь к html относительно корня
    html_rel = json_to_html_rel(full_json_path)
    # относительный путь от текущего HTML
    return relative_path(current_html_rel, html_rel)

# =========================================
# 3. Получение относительного пути к HTML от корня
# /json/ai-philosophy/future-of-ai/ai-future-2026.json -> ai-philosophy/future-of-ai/ai-future-2026.html
# =========================================
def json_to_html_rel(full_json_path: str) -> str:
    return full_json_path[6:-5] + ".html"

# =========================================
# 4. Получение полного пути к сохраняемому HTML файлу
# =========================================
def json_to_html_full(full_json_path: str) -> str:
    html_rel = json_to_html_rel(full_json_path)
    return str(ROOT_PATH / html_rel)

# =========================================
# 5. Формирование карточки статьи
# =========================================
def article_card(full_json_path: str, current_html_rel: str) -> str:
    data = read_json_article(full_json_path)
    if data is None:
        return None
    link = json_to_html_link(full_json_path, current_html_rel)
    title = data.get("title", "Без названия")
    description = data.get("description", "")
    return f'''<a href="{link}" class="ui card article-card">
    <div class="content">
        <div class="header">{title}</div>
        <div class="description">
            {description}
        </div>
    </div>
</a>'''

# =========================================
# 6. Формирование текста с карточками по списку json файлов
# =========================================
def cards_from_json_list(json_paths: list, current_html_rel: str) -> str:
    cards = []
    for path in json_paths[::-1]:
        card = article_card(path, current_html_rel)
        if card is not None:
            cards.append(card)
    return '\n'.join(cards)

# =========================================
# 6. 1. формирует ссылки на статьи в виде ненумерованного списка
# =========================================
def generate_articles_list(json_list, current_html_rel):
    items = []
    for full_json_path in json_list[::-1]:
        data = read_json_article(full_json_path)
        if data is None:
            continue
        title = data.get("title", "Без названия")
        link = json_to_html_link(full_json_path, current_html_rel)
        items.append(f'<li><a href="{link}">{title}</a></li>')
    return '<ul>\n' + '\n'.join(items) + '\n</ul>'
    
# =========================================
# 7. Генерация HTML по шаблону с переменными
# template_path - путь к шаблону
# vars_dict - словарь {VAR_NAME: value}
# =========================================
def render_template(template_path: str, vars_dict: dict) -> str:
    with open(template_path, "r", encoding="utf-8") as f:
        html = f.read()
    for k, v in vars_dict.items():
        html = html.replace(f"{{{k}}}", v)
    # минимизация: убираем переносы и лишние пробелы между тегами
    html = re.sub(r">\s+<", "><", html)
    html = re.sub(r"\s{2,}", " ", html)
    return html.strip()

# =========================================
# 8. Генерация главной index.html
# json_list - список полных путей к статьям для главной
# =========================================
def generate_index_html():
    index_html_path = ROOT_PATH / "index.html"
    current_html_rel = "index.html"  # для вычисления относительных ссылок
    
    # читаем список json файлов для главной
    json_list = read_json_article('/json/index.json')
    json_list = json_list["articles"]
    
    # формируем карточки
    articles_html = cards_from_json_list(json_list, current_html_rel)
    
    # формируем меню
    main_menu_html = generate_menu_html(current_html_rel)
    
    # словарь переменных для шаблона
    vars_dict = {
        "STYLE_CSS": relative_path("index.html", "style.css"),
        "FAVICON_JPG": relative_path("index.html", "favicon.jpg"),
        "MAIN_MENU": main_menu_html,
        "ARTICLES": articles_html
    }
    
    # путь к шаблону
    template_path = TEMPLATE_ROOT / "index.html"
    
    # рендерим HTML
    final_html = render_template(template_path, vars_dict)
    
    # создаём папку публикации, если не существует
    os.makedirs(ROOT_PATH, exist_ok=True)
    
    # сохраняем HTML
    with open(index_html_path, "w", encoding="utf-8") as f:
        f.write(final_html)
    
    print(f"Главная страница сгенерирована: {index_html_path}")

# =========================================
# 9. Формирование HTML для категории
# category_json_path: полный путь к /json/<category>/index.json
# =========================================
def generate_category_html(category, category_json_path: str):
    data = read_json_article(category_json_path)
    title = category["name"]
    description = category["description"]
    articles = data.get("articles", "")
    subcategories = category["subcategories"]

    # Путь к HTML относительно корня
    category_html_rel = f"{cat['folder']}/index.html"
    category_html_full = f"{ROOT_PATH}/{cat['folder']}/index.html"

    # формируем карточки статей
    articles_html = cards_from_json_list(articles, category_html_rel)

    # формируем карточки подкатегорий (только для категории)
    subcategories_cards = []
    for sub in subcategories:
        sub_title = sub["name"]
        sub_descr = sub["description"]
        sub_folder = sub["folder"]
        sub_link = sub["folder"] + "/index.html"
        card_html = f'''<a href="{sub_link}" class="ui card article-card">
    <div class="content">
        <div class="header">{sub_title}</div>
        <div class="description">{sub_descr}</div>
    </div>
</a>'''
        subcategories_cards.append(card_html)
    subcategories_html = '\n'.join(subcategories_cards)

    # меню
    main_menu_html = generate_menu_html(category_html_rel)

    # словарь для шаблона
    vars_dict = {
        "STYLE_CSS": relative_path(category_html_rel, 'style.css'),
        "FAVICON_JPG": relative_path(category_html_rel, 'favicon.jpg'),
        "MAIN_MENU": main_menu_html,
        "TITLE": title,
        "DESCRIPTION": description,
        "ARTICLES": articles_html,
        "SUBCATEGORIES": subcategories_html
    }

    template_path = TEMPLATE_ROOT / "category.html"
    final_html = render_template(template_path, vars_dict)

    # создаём папку, если нужно
    os.makedirs(f"{ROOT_PATH}/{cat['folder']}", exist_ok=True)
    with open(category_html_full, "w", encoding="utf-8") as f:
        f.write(final_html)

    print(f"Категория сгенерирована: {category_html_full}")

# =========================================
# 10. Формирование HTML для подкатегории
# subcategory_json_path: полный путь к /json/<category>/<subcategory>/index.json
# =========================================
def generate_subcategory_html(cat, subcat, subcategory_json_path: str):
    data = read_json_article(subcategory_json_path)
    title = subcat["name"]
    description = subcat["description"]
    articles = data.get("articles", [])

    # Путь к HTML относительно корня
    sub_html_rel = f"{cat['folder']}/{subcat['folder']}/index.html"
    sub_html_full = f"{ROOT_PATH}/{cat['folder']}/{subcat['folder']}/index.html"

    # формируем карточки статей
    articles = cards_from_json_list(articles, sub_html_rel)

    # меню
    main_menu_html = generate_menu_html(sub_html_rel)

    # словарь для шаблона
    vars_dict = {
        "STYLE_CSS": relative_path(sub_html_rel, 'style.css'),
        "FAVICON_JPG": relative_path(sub_html_rel, 'favicon.jpg'),
        "MAIN_MENU": main_menu_html,
        "TITLE": title,
        "DESCRIPTION": description,
        "ARTICLES": articles
    }

    template_path = TEMPLATE_ROOT / "subcategory.html"
    final_html = render_template(template_path, vars_dict)

    # создаём папку, если нужно
    os.makedirs(f"{ROOT_PATH}/{cat['folder']}/{subcat['folder']}", exist_ok=True)
    with open(sub_html_full, "w", encoding="utf-8") as f:
        f.write(final_html)

    print(f"Подкатегория сгенерирована: {sub_html_full}")
    
# =========================================
# 11. Функция генерации HTML статьи
# article_json_path - полный путь к json статьи
# =========================================
def generate_article_html(article_json_path):
    data = read_json_article(article_json_path)
    
    title = data.get("title", "Без названия")
    description = data.get("description", "")
    intro = data.get("intro", "")
    content = data.get("content", "")
    articles = data.get("articles", [])

    # путь к HTML относительно корня
    html_rel = json_to_html_rel(article_json_path)
    html_full = f"{ROOT_PATH}/{html_rel}"

    # меню
    main_menu_html = generate_menu_html(html_rel)

    # список ссылок на статьи
    articles_html = generate_articles_list(articles, html_rel)

    # словарь для шаблона
    vars_dict = {
        "STYLE_CSS": relative_path(html_rel, 'style.css'),
        "FAVICON_JPG": relative_path(html_rel, 'favicon.jpg'),
        "MAIN_MENU": main_menu_html,
        "TITLE": title,
        "DESCRIPTION": description,
        "INTRO": intro,
        "CONTENT": content,
        "ARTICLES": articles_html
    }

    # путь к шаблону
    template_path = TEMPLATE_ROOT / "article.html"
    final_html = render_template(template_path, vars_dict)

    # создаём папку, если нужно
    os.makedirs(os.path.dirname(html_full), exist_ok=True)
    with open(html_full, "w", encoding="utf-8") as f:
        f.write(final_html)

    print(f"Статья сгенерирована: {html_full}")
    
# === ПРИМЕР ИСПОЛЬЗОВАНИЯ ===
if __name__ == "__main__":
    generate_index_html()
    for cat in CATEGORIES:
        generate_category_html(cat, f"/json/{cat['folder']}/index.json")
        for subcat in cat["subcategories"]:
            generate_subcategory_html(cat, subcat, f"/json/{cat['folder']}/{subcat['folder']}/index.json")
            for file in os.listdir(f"../json/{cat['folder']}/{subcat['folder']}"):
                if file != 'index.json' and file.endswith('.json'):
                    generate_article_html(f"/json/{cat['folder']}/{subcat['folder']}/{file}")