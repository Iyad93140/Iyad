"""Résume un CSV de ventes en préservant les centimes avec Decimal."""
import argparse
import csv
from decimal import Decimal, InvalidOperation
import json
from pathlib import Path

COLUMNS = {'date', 'product', 'quantity', 'unit_price'}

def analyse(path):
    products = {}
    units = 0
    with Path(path).open(newline='', encoding='utf-8-sig') as stream:
        reader = csv.DictReader(stream)
        if not COLUMNS.issubset(reader.fieldnames or []):
            raise ValueError('Colonnes requises : date,product,quantity,unit_price')
        for line, row in enumerate(reader, start=2):
            product = (row.get('product') or '').strip()
            try:
                quantity = int(row.get('quantity') or '')
                price = Decimal(row.get('unit_price') or '')
            except (ValueError, InvalidOperation):
                raise ValueError(f'Ligne {line} : quantité ou prix invalide.')
            if (not product or quantity <= 0 or not price.is_finite() or
                    price < 0 or price != price.quantize(Decimal('0.01'))):
                raise ValueError(f'Ligne {line} : produit requis, quantité positive et prix positif ou nul à deux décimales maximum.')
            units += quantity
            products[product] = products.get(product, Decimal('0')) + quantity * price
    total = sum(products.values(), Decimal('0'))
    return {'units': units, 'revenue': f'{total:.2f}',
            'by_product': {k: f'{v:.2f}' for k, v in sorted(products.items(), key=lambda p: (-p[1], p[0]))}}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('csv_file')
    parser.add_argument('--output', help='Chemin facultatif du rapport JSON')
    args = parser.parse_args()
    try:
        result = analyse(args.csv_file)
        text = json.dumps(result, ensure_ascii=False, indent=2)
        if args.output:
            Path(args.output).write_text(text+'\n', encoding='utf-8')
        print(text)
    except (OSError, ValueError, InvalidOperation) as error:
        parser.exit(2, f'Erreur : {error}\n')

if __name__ == '__main__':main()
