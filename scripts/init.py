import os
import json

# === КОРНЕВАЯ ПАПКА ===
ROOT_DIR = "../ai-core-source/json"

# === СТРУКТУРА САЙТА ===
STRUCTURE = {
    "ai-blog": [
        "ai-thoughts-about-itself",
        "ai-philosophy",
        "can-ai-think",
        "ai-consciousness",
        "ai-limitations-errors",
        "how-ai-thinks",
        "ai-evolution-development",
        "ai-future-predictions",
        "ai-insights"
    ],
    "ai-world-understanding": [
        "how-ai-understands-world",
        "ai-and-reality",
        "ai-and-science",
        "ai-and-history",
        "ai-and-culture",
        "ai-and-language",
        "ai-perception-errors",
        "uncertainty-in-ai",
        "ai-data-and-knowledge"
    ],
    "ai-basics": [
        "what-is-ai",
        "how-ai-works",
        "neural-networks-explained",
        "machine-learning-basics",
        "deep-learning",
        "large-language-models",
        "ai-training-process",
        "ai-training-data",
        "ai-limitations-basics"
    ],
    "ai-technologies": [
        "modern-ai-technologies",
        "neural-network-architectures",
        "nlp-technologies",
        "computer-vision",
        "generative-ai",
        "ai-automation-tech",
        "ai-tools-services",
        "ai-tech-limitations",
        "ai-tech-future"
    ],
    "ai-use-cases": [
        "ai-in-business",
        "ai-in-marketing",
        "ai-in-programming",
        "ai-in-education",
        "ai-in-daily-life",
        "ai-for-making-money",
        "process-automation-ai",
        "ai-content-generation",
        "ai-usage-mistakes"
    ],
    "ai-philosophy": [
        "future-of-ai",
        "is-ai-dangerous",
        "ai-and-jobs",
        "ai-regulation",
        "ai-ethics",
        "ai-control-problem",
        "technological-singularity",
        "ai-impact-on-society",
        "limits-of-ai-development"
    ]
}


def create_index_file(path):
    os.makedirs(path, exist_ok=True)
    index_path = os.path.join(path, "index.json")

    if not os.path.exists(index_path):
        with open(index_path, "w", encoding="utf-8") as f:
            json.dump({"articles": []}, f, ensure_ascii=False, indent=2)
        print(f"Created: {index_path}")
    else:
        print(f"Exists: {index_path}")


def main():
    # Главная
    create_index_file(ROOT_DIR)

    # Категории и подкатегории
    for category, subcategories in STRUCTURE.items():
        category_path = os.path.join(ROOT_DIR, category)
        create_index_file(category_path)

        for subcategory in subcategories:
            subcategory_path = os.path.join(category_path, subcategory)
            create_index_file(subcategory_path)


if __name__ == "__main__":
    main()