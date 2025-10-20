import json, re, unicodedata, pathlib, sys
from typing import List, Dict, Any

def normalize_text(s: str) -> str:
    if s is None:
        return ""
    s = unicodedata.normalize("NFC", str(s))
    s = re.sub(r"\s+", " ", s).strip()
    return s

def normalize_menu(in_path: str, out_path: str) -> None:
    data = json.load(open(in_path, "r", encoding="utf-8"))
    docs = []
    items: List[Dict[str, Any]] = data.get("items", [])
    currency = data.get("currency", "IRR")
    for item in items:
        name = normalize_text(item.get("name", ""))
        desc = normalize_text(item.get("description", ""))
        ingredients = [normalize_text(x) for x in item.get("ingredients", [])]
        allergens = [normalize_text(x) for x in item.get("allergens", [])]
        price_val = item.get("price", 0)
        try:
            price = float(price_val)
        except Exception:
            price = 0.0
        diets = [normalize_text(x) for x in item.get("diets", [])]
        text = (
            f"نام: {name}\n"
            f"مواد: {', '.join(ingredients)}\n"
            f"آلرژن: {', '.join(allergens)}\n"
            f"رژیم: {', '.join(diets)}\n"
            f"توضیح: {desc}\n"
            f"قیمت: {price} {currency}"
        )
        docs.append({
            "id": name or f"item_{len(docs)+1}",
            "text": text,
            "meta": {
                "name": name,
                "ingredients": ingredients,
                "allergens": allergens,
                "price": price,
                "currency": currency,
                "diets": diets,
                "description": desc
            }
        })
    pathlib.Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    json.dump(docs, open(out_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"✅ Wrote {len(docs)} normalized docs to: {out_path}")

if __name__ == "__main__":
    in_path = sys.argv[1] if len(sys.argv) > 1 else "app/data/samples/menu_today.json"
    out_path = sys.argv[2] if len(sys.argv) > 2 else "app/data/processed/menu_docs.json"
    normalize_menu(in_path, out_path)
