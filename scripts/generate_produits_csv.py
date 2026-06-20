#!/usr/bin/env python3
"""
Extrait le tableau de produits depuis index.html et régénère produits.csv.
Source: champ `produits` dans le bloc <script> de index.html.
"""
import csv
import re
import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
HTML_FILE = ROOT / "index.html"
CSV_FILE = ROOT / "produits.csv"

# Regex pour capturer les objets produit dans le tableau JS
PRODUCT_RE = re.compile(
    r'\{id:(\d+),nom:\'([^\']+)\',prix:(\d+),region:\'([^\']+)\'',
)

def extract_products(html: str) -> list[dict]:
    products = []
    for m in PRODUCT_RE.finditer(html):
        products.append({
            "id": int(m.group(1)),
            "nom": m.group(2),
            "emoji": "",
            "prix_vente_eur": int(m.group(3)),
            "region": m.group(4),
        })
    return products

def main():
    if not HTML_FILE.exists():
        print(f"Erreur : {HTML_FILE} introuvable", file=sys.stderr)
        sys.exit(1)

    html = HTML_FILE.read_text(encoding="utf-8")
    products = extract_products(html)

    if not products:
        print("Erreur : aucun produit trouvé dans index.html", file=sys.stderr)
        sys.exit(1)

    with CSV_FILE.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "nom", "emoji", "prix_vente_eur", "region"])
        writer.writeheader()
        writer.writerows(products)

    print(f"{len(products)} produits écrits dans {CSV_FILE}")

if __name__ == "__main__":
    main()
