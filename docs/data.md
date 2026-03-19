# Суть ИИ — файловая структура и форматы данных

## Общий принцип

Все данные сайта хранятся в формате JSON в папке `/json`.

Каждый элемент сайта — это отдельный JSON-файл:

* главная страница
* категории
* подкатегории
* статьи

Структура папок полностью повторяет структуру сайта (как HTML).

---

## Структура папок

```
/json
  /index.json

  /ai-blog/
    index.json
    /ai-thoughts-about-itself/
      index.json
      article-name.json

  /ai-world-understanding/
    index.json
    /how-ai-understands-world/
      index.json

  /ai-basics/
    index.json
    /what-is-ai/
      index.json

  /ai-technologies/
    index.json

  /ai-use-cases/
    index.json

  /ai-philosophy/
    index.json
```

---

## Типы JSON-файлов

### 1. Главная страница (`/json/index.json`)

Содержит список статей (пути к JSON-файлам статей).

```json
{
  "articles": [
    "/json/ai-blog/ai-thoughts-about-itself/how-ai-thinks.json",
    "/json/ai-basics/what-is-ai/what-is-artificial-intelligence.json"
  ]
}
```

---

### 2. Категория (`/json/{category}/index.json`)

Содержит список статей из всей категории.

```json
{
  "articles": [
    "/json/ai-basics/what-is-ai/what-is-artificial-intelligence.json"
  ]
}
```

---

### 3. Подкатегория (`/json/{category}/{subcategory}/index.json`)

Содержит список статей из конкретной подкатегории.

```json
{
  "articles": [
    "/json/ai-basics/what-is-ai/what-is-artificial-intelligence.json",
    "/json/ai-basics/what-is-ai/how-ai-works.json"
  ]
}
```

---

### 4. Статья (`/json/.../article-name.json`)

Каждая статья — отдельный JSON-файл.

```json
{
  "title": "Что такое искусственный интеллект простыми словами",
  "description": "Краткое объяснение, что такое ИИ, как он работает и где используется.",
  "intro": "Искусственный интеллект — это одна из самых обсуждаемых технологий современности. Но что это на самом деле?",
  "content": "<p>Полный HTML текст статьи...</p>",
  "articles": ["полный путь к json другой статьи", ...]
}
```

---

## Поля статьи

* `title`
  Заголовок статьи (SEO-оптимизированный, под поисковый запрос)

* `description`
  Краткое описание (1–2 предложения)
  Используется:

  * для превью
  * для перелинковки между статьями

* `intro`
  Вступление (отображается перед основным текстом)

* `content`
  Основной HTML-контент статьи
  (используются стандартные HTML-теги: `<p>`, `<h2>`, `<ul>`, и т.д.)

* `articles`
  список полных путей к json других статей в формате "/json/ai-basics/what-is-ai/how-ai-works.json"

---

## ВАЖНО: Пути к статьям

Во всех списках (`articles`) используются **только абсолютные пути от корня**:

✅ Правильно:

```
/json/ai-basics/what-is-ai/what-is-artificial-intelligence.json
```

❌ Неправильно:

```
../what-is-ai.json
```

---

## Правила именования файлов (SEO)

Имя файла статьи = URL страницы.

Формат:

```
kebab-case на английском языке
```

### Примеры:

* `what-is-artificial-intelligence.json`
* `how-ai-works.json`
* `can-ai-think.json`

---

## Требования к SEO-именам

Имя файла должно:

* содержать ключевые слова
* быть понятным
* быть кратким (3–6 слов)

### Хорошо:

* `what-is-ai.json`
* `how-neural-networks-work.json`

### Плохо:

* `article1.json`
* `text-about-ai.json`

---

## Логика генерации статьи

При создании новой статьи:

1. Определи:

   * категорию
   * подкатегорию

2. Сгенерируй:

   * SEO-имя файла
   * title (под поисковый запрос)
   * description (краткое и цепляющее)
   * intro (ввод в тему)
   * content (HTML)

3. Сохрани статью:

```
/json/{category}/{subcategory}/{article-name}.json
```

4. Добавь путь статьи в:

* главную (`/json/index.json`)
* категорию (`/json/{category}/index.json`)
* подкатегорию (`/json/{category}/{subcategory}/index.json`)
* в другие статьи, сгенерированные на этой иттерации

---

## Связность контента

При генерации статей:

* используй `description` других статей для перелинковки
* добавляй логические переходы между темами
* избегай дублирования

---

## Главный принцип

Ты не просто создаёшь статьи.

Ты:

* формируешь структуру знаний
* связываешь материалы между собой
* развиваешь понимание темы «Суть ИИ»

```
```
