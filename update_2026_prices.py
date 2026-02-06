#!/usr/bin/env python3
"""Update all product prices to 2026 pricing"""

import json

# Read existing products
with open('products.json', 'r') as f:
    products = json.load(f)

# 2026 Pricing by category/type
IMPLANT_PRICES_2026 = {
    'NobelActive TiUltra': 615,
    'NobelActive': 590,  # Non-TiUltra
    'N1 TiUltra': 635,
    'NobelParallel CC TiUltra': 615,
    'NobelReplace CC TiUltra': 615,
    'NobelPearl': 685,  # Ceramic
    'NobelZygoma': 2235,  # Zygoma implants
    'Branemark': 545,  # Legacy
}

ABUTMENT_PRICES_2026 = {
    'Esthetic Abutment': 344,
    'Multi-unit Abutment': 290,
    'Locator Abutment': 395,
    'GoldAdapt': 125,
    'Angulated Screw Channel': 350,
    'Omnigrip': 115,
    'Healing Abutment': 52,
}

def update_implant_price(product):
    """Determine correct 2026 price for an implant"""
    desc = product['description']
    
    if 'Zygoma' in desc:
        return 2235
    elif 'NobelPearl' in desc:
        return 685
    elif 'N1' in desc and 'TiUltra' in desc:
        return 635
    elif 'TiUltra' in desc:
        return 615
    elif 'NobelActive' in desc:
        return 590
    elif 'NobelParallel' in desc:
        return 590
    elif 'NobelReplace' in desc:
        return 590
    elif 'Brånemark' in desc or 'Branemark' in desc:
        return 545
    else:
        return product['price']  # Keep existing if unknown

def update_abutment_price(product):
    """Determine correct 2026 price for an abutment"""
    desc = product['description']
    
    if 'Esthetic Abutment' in desc or 'Esthetic abutment' in desc:
        return 344
    elif 'Multi-unit' in desc or 'Multi-Unit' in desc:
        if 'Abutment' in desc:
            return 290
    elif 'Locator' in desc:
        return 395
    elif 'GoldAdapt' in desc:
        return 125
    elif 'Healing' in desc:
        return 52
    elif 'Omnigrip' in desc:
        return 115
    elif 'Angulated Screw Channel' in desc:
        return 350
    
    return product['price']  # Keep existing if unknown

# Update implant categories
implant_categories = [
    'NobelActive TiUltra Implants',
    'NobelActive Implants', 
    'Nobel Biocare N1 TiUltra Implants',
    'NobelParallel CC TiUltra Implants',
    'NobelReplace CC TiUltra Implants',
    'NobelPearl Ceramic Implants',
    'NobelZygoma Implants'
]

for cat in implant_categories:
    if cat in products:
        for prod in products[cat]:
            old_price = prod['price']
            prod['price'] = update_implant_price(prod)
            if old_price != prod['price']:
                print(f"  {cat}: {prod['id']} ${old_price} -> ${prod['price']}")

# Update abutment categories
abutment_categories = [
    'Esthetic Abutments',
    'Multi-Unit Abutments',
    'Locator Abutments',
    'GoldAdapt Abutments'
]

for cat in abutment_categories:
    if cat in products:
        for prod in products[cat]:
            old_price = prod['price']
            prod['price'] = update_abutment_price(prod)
            if old_price != prod['price']:
                print(f"  {cat}: {prod['id']} ${old_price} -> ${prod['price']}")

# Write updated products
with open('products.json', 'w') as f:
    json.dump(products, f, indent=2)

print("\n✅ All products updated to 2026 pricing")

# Summary
for cat in implant_categories + abutment_categories:
    if cat in products:
        sample = products[cat][0] if products[cat] else None
        if sample:
            print(f"  {cat}: ${sample['price']}")
