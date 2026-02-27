import ast
import re
import pandas as pd
from sqlalchemy.orm import Session
from database import engine, SessionLocal, Base
from models import Recipe


MEAT_KEYWORDS = ["chicken", "beef", "pork", "lamb", "turkey", "bacon", "sausage", "fish", "salmon", "shrimp", "tuna"]
GLUTEN_INGREDIENTS = ["flour", "bread", "pasta", "wheat", "barley", "rye", "couscous"]

def safe_parse(value):
    if pd.isna(value):
        return None
    try:
        return ast.literal_eval(str(value))
    except (ValueError, SyntaxError):
        return str(value)

def parse_nutrition(value):
    parsed = safe_parse(value)
    if isinstance(parsed, dict):
        result = {}
        for k, v in parsed.items():
            try:
                result[k] = float(re.sub(r"[^\d.]", "", str(v)))
            except ValueError:
                result[k] = 0.0
        return result
    return None

def derive_dietary_tags(ingredients_list):
    if not ingredients_list or not isinstance(ingredients_list, list):
        return []
    text = " ".join(ingredients_list).lower()
    tags = []

    has_meat = any(m in text for m in MEAT_KEYWORDS)
    has_gluten = any(g in text for g in GLUTEN_INGREDIENTS)

    if not has_meat:
        tags.append("vegetarian")
        dairy_words = ["milk", "cheese", "cream", "butter", "yogurt", "egg"]
        if not any(d in text for d in dairy_words):
            tags.append("vegan")
    if not has_gluten:
        tags.append("gluten_free")

    return tags

def estimate_cost(ingredients_list, cost_per_item=0.75):
    if not ingredients_list or not isinstance(ingredients_list, list):
        return None
    return round(len(ingredients_list) * cost_per_item, 2)

def ingest(csv_path: str = "data/raw/recipes.csv"):
    Base.metadata.create_all(bind=engine)
    df = pd.read_csv(csv_path)
    db: Session = SessionLocal()

    if db.query(Recipe).count() > 0:
        print("Recipes table already populated. Skipping ingestion.")
        db.close()
        return

    records = []
    for _, row in df.iterrows():
        ingredients = safe_parse(row.get("ingredients"))
        nutrition = parse_nutrition(row.get("nutrition"))

        recipe = Recipe(
            recipe_name=str(row.get("recipe_name", "Unknown")),
            prep_time=int(row["prep_time"]) if pd.notna(row.get("prep_time")) else None,
            cook_time=int(row["cook_time"]) if pd.notna(row.get("cook_time")) else None,
            total_time=int(row["total_time"]) if pd.notna(row.get("total_time")) else None,
            servings=int(row["servings"]) if pd.notna(row.get("servings")) else None,
            ingredients=ingredients if isinstance(ingredients, list) else None,
            directions=safe_parse(row.get("directions")),
            rating=float(row["rating"]) if pd.notna(row.get("rating")) else None,
            url=str(row.get("url", "")),
            cuisine_path=str(row.get("cuisine_path")) if pd.notna(row.get("cuisine_path")) else None,
            nutrition=nutrition,
            timing=safe_parse(row.get("timing")),
            dietary_tags=derive_dietary_tags(ingredients if isinstance(ingredients, list) else []),
            estimated_cost=estimate_cost(ingredients if isinstance(ingredients, list) else []),
        )

        records.append(recipe)

    db.bulk_save_objects(records)
    db.commit()
    db.close()
    print(f"Ingested {len(records)} recipes.")


if __name__ == "__main__":
    ingest()