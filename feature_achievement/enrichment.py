from feature_achievement.ingestion import convert_content_to_json, dump_data_to_json
import yaml
import spacy


nlp = spacy.load("en_core_web_sm")


def enrich_chapter_text(data: dict) -> dict:
    for chapter in data["chapters"]:
        sections = chapter.get("sections", [])
        signals = chapter.get("signals", {})
        bullets = signals.get("bullets", [])
        chapter["chapter_text"] = " ".join(bullets) if bullets else " ".join(sections)
    return data


def load_enriched_data(book_name, content_path):
    base_data = convert_content_to_json(book_name, content_path)
    # enriched_data_1 = enrich_signals_with_keyphrases(base_data)
    enriched_data = enrich_chapter_text(base_data)
    return enriched_data


def load_all_enriched_data(config_path):
    with open(config_path, "r") as f:
        book_configs = yaml.safe_load(f)
    enriched_books = []

    for cfg in book_configs:
        enriched = load_enriched_data(
            book_name=cfg["book_name"], content_path=cfg["content_path"]
        )
        dump_data_to_json(enriched)
        enriched_books.append(enriched)

    return enriched_books
