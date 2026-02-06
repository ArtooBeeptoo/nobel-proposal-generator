#!/usr/bin/env python3
"""Extract regenerative and suture products from price list and add to products.json"""

import json
import re

# Read existing products
with open('products.json', 'r') as f:
    products = json.load(f)

# Regenerative - Grafting products
grafting_products = [
    # creos allo.gain particulate - mineralized corticocancellous
    {"id": "N4510-B", "description": "creos allo.gain min corticocancellous bowl (0.25-1.00 mm) 0.25 cc", "price": 84},
    {"id": "N4520-B", "description": "creos allo.gain min corticocancellous bowl (0.25-1.00 mm) 0.5 cc", "price": 108},
    {"id": "N4530-B", "description": "creos allo.gain min corticocancellous bowl (0.25-1.00 mm) 1.0 cc", "price": 142},
    {"id": "N4540-B", "description": "creos allo.gain min corticocancellous bowl (0.25-1.00 mm) 2.0 cc", "price": 232},
    {"id": "N4510", "description": "creos allo.gain min corticocancellous vial (0.25-1.00 mm) 0.25 cc", "price": 78},
    {"id": "N4520", "description": "creos allo.gain min corticocancellous vial (0.25-1.00 mm) 0.5 cc", "price": 99},
    {"id": "N4530", "description": "creos allo.gain min corticocancellous vial (0.25-1.00 mm) 1.0 cc", "price": 130},
    {"id": "N4540", "description": "creos allo.gain min corticocancellous vial (0.25-1.00 mm) 2.0 cc", "price": 215},
    # creos allo.gain dbm putty
    {"id": "N6110", "description": "creos allo.gain dbm putty 0.5 cc", "price": 146},
    {"id": "N6120", "description": "creos allo.gain dbm putty 1.0 cc", "price": 247},
    {"id": "N6130", "description": "creos allo.gain dbm putty 2.5 cc", "price": 504},
    # creos xenogain - bovine bone mineral
    {"id": "N1110", "description": "creos xenogain vial cancellous (0.2-1.0 mm) 0.25 g", "price": 80},
    {"id": "N1120", "description": "creos xenogain vial cancellous (0.2-1.0 mm) 0.50 g", "price": 127},
    {"id": "N1130", "description": "creos xenogain vial cancellous (0.2-1.0 mm) 1.00 g", "price": 204},
    {"id": "N1140", "description": "creos xenogain vial cancellous (0.2-1.0 mm) 2.00 g", "price": 338},
    {"id": "N1111", "description": "creos xenogain vial cancellous (1.0-2.0 mm) 0.25 g", "price": 80},
    {"id": "N1121", "description": "creos xenogain vial cancellous (1.0-2.0 mm) 0.50 g", "price": 127},
    {"id": "N1131", "description": "creos xenogain vial cancellous (1.0-2.0 mm) 1.00 g", "price": 204},
    {"id": "N1141", "description": "creos xenogain vial cancellous (1.0-2.0 mm) 2.00 g", "price": 338},
    {"id": "N1110-B", "description": "creos xenogain bowl cancellous (0.2-1.0 mm) 0.25 g", "price": 80},
    {"id": "N1120-B", "description": "creos xenogain bowl cancellous (0.2-1.0 mm) 0.50 g", "price": 127},
    {"id": "N1130-B", "description": "creos xenogain bowl cancellous (0.2-1.0 mm) 1.00 g", "price": 204},
    {"id": "N1140-B", "description": "creos xenogain bowl cancellous (0.2-1.0 mm) 2.00 g", "price": 338},
    {"id": "N1210", "description": "creos xenogain syringe cancellous (0.2-1.0 mm) 0.25 g", "price": 80},
    {"id": "N1220", "description": "creos xenogain syringe cancellous (0.2-1.0 mm) 0.50 g", "price": 127},
    # creos xenogain collagen
    {"id": "N1320", "description": "creos xenogain collagen block 6 x 6 x 6 mm 100 mg", "price": 106},
    {"id": "N1330", "description": "creos xenogain collagen block 7 x 8 x 9 mm 250 mg", "price": 200},
    {"id": "N1340", "description": "creos xenogain collagen block 7 x 8 x 9 mm 250 mg (alt)", "price": 295},
    {"id": "N1410", "description": "creos xenogain collagen syringe 4.6x40 mm 250 mg", "price": 200},
    {"id": "N1420", "description": "creos xenogain collagen syringe 5.6x45 mm 500 mg", "price": 295},
    # creos xenocote/xenoplug/xenotape
    {"id": "WD62201", "description": "creos xenocote 1 cm x 2 cm 10x", "price": 159},
    {"id": "WD62202", "description": "creos xenoplug 1 cm x 2 cm 10x", "price": 149},
    {"id": "WD62200", "description": "creos xenotape 2.5 cm x 7.5 cm 10x", "price": 225},
]

# Regenerative - Membranes
membrane_products = [
    # creos allo.protect pericardium
    {"id": "N7110", "description": "creos allo.protect pericardium membrane 10 x 10 mm", "price": 112},
    {"id": "N7120", "description": "creos allo.protect pericardium membrane 15 x 20 mm", "price": 190},
    {"id": "N7140", "description": "creos allo.protect pericardium membrane 20 x 30 mm", "price": 254},
    # creos xenoprotect collagen membrane
    {"id": "N1520", "description": "creos xenoprotect collagen membrane 15 x 20 mm", "price": 170},
    {"id": "N2530", "description": "creos xenoprotect collagen membrane 25 x 30 mm", "price": 205},
    {"id": "N3040", "description": "creos xenoprotect collagen membrane 30 x 40 mm", "price": 330},
    # Cytoplast RTM collagen
    {"id": "CLMRTM1520", "description": "Cytoplast RTM Collagen 15 x 20 mm, 2/pkg", "price": 220},
    {"id": "CLMRTM2030", "description": "Cytoplast RTM Collagen 20 x 30 mm, 2/pkg", "price": 270},
    {"id": "CLMRTM3040", "description": "Cytoplast RTM Collagen 30 x 40 mm, 2/pkg", "price": 390},
    # Cytoplast Ti-150 titanium-reinforced (selected sizes)
    {"id": "TI150PS-N-1", "description": "Cytoplast Ti-150 PS 20 mm x 25 mm, 1/pkg", "price": 205},
    {"id": "TI150PS-N-2", "description": "Cytoplast Ti-150 PS 20 mm x 25 mm, 2/pkg", "price": 350},
    {"id": "TI150PL-N-1", "description": "Cytoplast Ti-150 PL 25 mm x 30 mm, 1/pkg", "price": 225},
    {"id": "TI150PL-N-2", "description": "Cytoplast Ti-150 PL 25 mm x 30 mm, 2/pkg", "price": 385},
    {"id": "TI150XL-N-1", "description": "Cytoplast Ti-150 XL 30 mm x 40 mm, 1/pkg", "price": 280},
    {"id": "TI150XL-N-2", "description": "Cytoplast Ti-150 XL 30 mm x 40 mm, 2/pkg", "price": 475},
    {"id": "TI150BL-N-1", "description": "Cytoplast Ti-150 BL 17 mm x 25 mm, 1/pkg", "price": 170},
    {"id": "TI150BL-N-2", "description": "Cytoplast Ti-150 BL 17 mm x 25 mm, 2/pkg", "price": 290},
    {"id": "TI150K2-N-1", "description": "Cytoplast Ti-150 K2 40 mm x 50 mm, 1/pkg", "price": 395},
    {"id": "TI150K2-N-2", "description": "Cytoplast Ti-150 K2 40 mm x 50 mm, 2/pkg", "price": 675},
    # TXT-200
    {"id": "TXT1224", "description": "Cytoplast TXT-200 12 mm x 24 mm 10/pkg", "price": 450},
    {"id": "TXT1224-1", "description": "Cytoplast TXT-200 12 mm x 24 mm 1/pkg", "price": 55},
    {"id": "TXT2530", "description": "Cytoplast TXT-200 25 mm x 30 mm 4/pkg", "price": 300},
    {"id": "TXT2530-1", "description": "Cytoplast TXT-200 25 mm x 30 mm 1/pkg", "price": 90},
    # RTM Plug/Foam/Tape
    {"id": "CLMRTMPLUG10", "description": "Cytoplast RTMPlug 10/pkg", "price": 128},
    {"id": "CLMRTMFOAM10", "description": "Cytoplast RTMFoam 10/pkg", "price": 144},
    {"id": "CLMRTMTAPE10", "description": "Cytoplast RTMTape 10/pkg", "price": 199},
]

# Sutures
suture_products = [
    # Cytoplast PTFE sutures
    {"id": "CS0418", "description": "Cytoplast PTFE 18\" 2-0 USP, 3/8 circle 19 mm needle, 12/pkg", "price": 105},
    {"id": "CS0428", "description": "Cytoplast PTFE 28\" 2-0 USP, 3/8 circle 19 mm needle, 12/pkg", "price": 115},
    {"id": "CS0518", "description": "Cytoplast PTFE 18\" 3-0 USP, 3/8 circle 16 mm needle, 12/pkg", "price": 105},
    {"id": "CS0518BK", "description": "Cytoplast PTFE 18\" 3-0 USP, 3/8 circle black 16 mm needle, 12/pkg", "price": 115},
    {"id": "CS051819", "description": "Cytoplast PTFE 18\" 3-0 USP, 3/8 circle 19 mm needle, 12/pkg", "price": 105},
    {"id": "CS051819BK", "description": "Cytoplast PTFE 18\" 3-0 USP, 3/8 circle black 19 mm needle, 12/pkg", "price": 115},
    {"id": "CS0528", "description": "Cytoplast PTFE 28\" 3-0 USP, 3/8 circle 16 mm needle, 12/pkg", "price": 115},
    {"id": "CS0528BK", "description": "Cytoplast PTFE 28\" 3-0 USP, 3/8 circle black 16 mm needle, 12/pkg", "price": 125},
    {"id": "CS0618PERIO", "description": "Cytoplast PTFE 18\" 4-0 USP, 1/2 circle 13 mm needle, 12/pkg", "price": 115},
    {"id": "CS0618PREM", "description": "Cytoplast PTFE 18\" 4-0 USP, 3/8 circle 13 mm needle, 12/pkg", "price": 115},
    {"id": "CS0618RC", "description": "Cytoplast PTFE 18\" 4-0 USP, 3/8 circle 16 mm needle, 12/pkg", "price": 115},
    {"id": "CS071813", "description": "Cytoplast PTFE 18\" 5-0 USP, 3/8 circle 13 mm needle, 12/pkg", "price": 115},
    {"id": "CS071816", "description": "Cytoplast PTFE 18\" 5-0 USP, 3/8 circle 16 mm needle, 12/pkg", "price": 115},
    {"id": "CS072813", "description": "Cytoplast PTFE 28\" 5-0 USP, 3/8 circle 13 mm needle, 12/pkg", "price": 125},
    {"id": "CS072816", "description": "Cytoplast PTFE 28\" 5-0 USP, 3/8 circle 16 mm needle, 12/pkg", "price": 125},
    # RESORBA GLYCOLON sutures
    {"id": "RMGOD01100", "description": "GLYCOLON 45 cm violet, 5-0 USP, 1/2 circle 16 mm needle, 12/pkg", "price": 79},
    {"id": "RMGOD01101", "description": "GLYCOLON 45 cm violet, 4-0 USP, 1/2 circle 18 mm needle, 12/pkg", "price": 79},
    {"id": "RMGOD01102", "description": "GLYCOLON 45 cm violet, 6-0 USP, 1/2 circle 10 mm needle, 12/pkg", "price": 100},
    {"id": "RMGOD01200", "description": "GLYCOLON 45 cm undyed, 6-0 USP, 3/8 circle 13 mm needle, 12/pkg", "price": 79},
    {"id": "RMGOD01201", "description": "GLYCOLON 45 cm violet, 4-0 USP, 3/8 circle 16 mm needle, 12/pkg", "price": 79},
    {"id": "RMGOD01202", "description": "GLYCOLON 45 cm undyed, 5-0 USP, 3/8 circle 18 mm needle, 12/pkg", "price": 79},
    {"id": "RMGOD01204", "description": "GLYCOLON 45 cm violet, 3-0 USP, 3/8 circle 16 mm needle, 12/pkg", "price": 79},
    {"id": "RMGOD01205", "description": "GLYCOLON 45 cm violet, 3-0 USP, 3/8 circle 18 mm needle, 12/pkg", "price": 79},
    {"id": "RMGOD01210", "description": "GLYCOLON 45 cm violet, 5-0 USP, 3/8 circle black 13 mm needle, 12/pkg", "price": 95},
    {"id": "RMGOD01211", "description": "GLYCOLON 45 cm violet, 5-0 USP, 3/8 circle black 16 mm needle, 12/pkg", "price": 95},
    {"id": "RMGOD01212", "description": "GLYCOLON 45 cm violet, 5-0 USP, 3/8 circle black 18 mm needle, 12/pkg", "price": 95},
]

# Add new categories
products['Regenerative - Grafting'] = grafting_products
products['Regenerative - Membranes'] = membrane_products
products['Sutures'] = suture_products

# Write updated products
with open('products.json', 'w') as f:
    json.dump(products, f, indent=2)

print(f"Added {len(grafting_products)} grafting products")
print(f"Added {len(membrane_products)} membrane products")
print(f"Added {len(suture_products)} suture products")
print(f"Total categories: {len(products)}")
