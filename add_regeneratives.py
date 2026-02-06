#!/usr/bin/env python3
"""Extract regenerative and suture products from 2026 price list and add to products.json"""

import json

# Read existing products
with open('products.json', 'r') as f:
    products = json.load(f)

# Remove old regenerative/suture categories if they exist
for cat in ['Regenerative - Grafting', 'Regenerative - Membranes', 'Sutures']:
    if cat in products:
        del products[cat]

# 2026 Regenerative - Grafting products
grafting_products = [
    # creos allo.gain (allogenic) - mineralized corticocancellous
    {"id": "N4510BA", "description": "creos allo.gain corticocancellous bowl (0.25-1.00 mm) 0.25 cc", "price": 84},
    {"id": "N4511BA", "description": "creos allo.gain corticocancellous bowl (0.5-1.0 mm) 0.25 cc", "price": 84},
    {"id": "N4520BA", "description": "creos allo.gain corticocancellous bowl (0.25-1.00 mm) 0.5 cc", "price": 108},
    {"id": "N4521BA", "description": "creos allo.gain corticocancellous bowl (0.5-1.0 mm) 0.5 cc", "price": 108},
    {"id": "N4530BA", "description": "creos allo.gain corticocancellous bowl (0.25-1.00 mm) 1.0 cc", "price": 142},
    {"id": "N4531BA", "description": "creos allo.gain corticocancellous bowl (0.5-1.0 mm) 1.0 cc", "price": 142},
    {"id": "N4540BA", "description": "creos allo.gain corticocancellous bowl (0.25-1.00 mm) 2.0 cc", "price": 232},
    {"id": "N4541BA", "description": "creos allo.gain corticocancellous bowl (0.5-1.0 mm) 2.0 cc", "price": 232},
    # creos allo.gain - demineralized cortical
    {"id": "N4310BA", "description": "creos allo.gain demineralized cortical bowl (0.125-0.850 mm) 0.25 cc", "price": 55},
    {"id": "N4311BA", "description": "creos allo.gain demineralized cortical bowl (0.5-1.0 mm) 0.25 cc", "price": 55},
    {"id": "N4320BA", "description": "creos allo.gain demineralized cortical bowl (0.125-0.850 mm) 0.5 cc", "price": 77},
    {"id": "N4321BA", "description": "creos allo.gain demineralized cortical bowl (0.5-1.0 mm) 0.5 cc", "price": 77},
    {"id": "N4330BA", "description": "creos allo.gain demineralized cortical bowl (0.125-0.850 mm) 1.0 cc", "price": 105},
    {"id": "N4331BA", "description": "creos allo.gain demineralized cortical bowl (0.5-1.0 mm) 1.0 cc", "price": 105},
    {"id": "N4340BA", "description": "creos allo.gain demineralized cortical bowl (0.125-0.850 mm) 2.0 cc", "price": 164},
    {"id": "N4341BA", "description": "creos allo.gain demineralized cortical bowl (0.5-1.0 mm) 2.0 cc", "price": 164},
    # creos allo.gain - mineralized cancellous
    {"id": "N4210BA", "description": "creos allo.gain mineralized cancellous bowl (0.25-1.00 mm) 0.25 cc", "price": 81},
    {"id": "N4211BA", "description": "creos allo.gain mineralized cancellous bowl (0.5-1.0 mm) 0.25 cc", "price": 81},
    {"id": "N4220BA", "description": "creos allo.gain mineralized cancellous bowl (0.25-1.00 mm) 0.5 cc", "price": 108},
    {"id": "N4221BA", "description": "creos allo.gain mineralized cancellous bowl (0.5-1.0 mm) 0.5 cc", "price": 108},
    {"id": "N4230BA", "description": "creos allo.gain mineralized cancellous bowl (0.25-1.00 mm) 1.0 cc", "price": 142},
    {"id": "N4231BA", "description": "creos allo.gain mineralized cancellous bowl (0.5-1.0 mm) 1.0 cc", "price": 142},
    {"id": "N4240BA", "description": "creos allo.gain mineralized cancellous bowl (0.25-1.00 mm) 2.0 cc", "price": 217},
    {"id": "N4241BA", "description": "creos allo.gain mineralized cancellous bowl (0.5-1.0 mm) 2.0 cc", "price": 217},
    # creos allo.gain dbm putty
    {"id": "N6110", "description": "creos allo.gain dbm putty 0.5 cc", "price": 155},
    {"id": "N6120", "description": "creos allo.gain dbm putty 1.0 cc", "price": 263},
    {"id": "N6130", "description": "creos allo.gain dbm putty 2.5 cc", "price": 537},
    # enCore allogenic bone substitute
    {"id": "CM55050", "description": "enCore 50/50 cortical & cancellous allograft (0.5-1.25 mm) 0.5 cc", "price": 95},
    {"id": "CM55100", "description": "enCore 50/50 cortical & cancellous allograft (0.5-1.25 mm) 1.0 cc", "price": 137},
    {"id": "CM55150", "description": "enCore 50/50 cortical & cancellous allograft (0.5-1.25 mm) 1.5 cc", "price": 169},
    {"id": "CM55250", "description": "enCore 50/50 cortical & cancellous allograft (0.5-1.25 mm) 2.5 cc", "price": 218},
    {"id": "NAT025", "description": "enCore natural blend allograft (0.25-1.00 mm) 0.25 cc", "price": 62},
    {"id": "NAT050", "description": "enCore natural blend allograft (0.25-1.00 mm) 0.5 cc", "price": 78},
    {"id": "NAT100", "description": "enCore natural blend allograft (0.25-1.00 mm) 1.0 cc", "price": 105},
    {"id": "NAT150", "description": "enCore natural blend allograft (0.25-1.00 mm) 1.5 cc", "price": 147},
    {"id": "NAT250", "description": "enCore natural blend allograft (0.25-1.00 mm) 2.5 cc", "price": 211},
    # creos xenogain bovine mineral matrix - bowl
    {"id": "N1110-B", "description": "creos xenogain bowl cancellous (0.2-1.0 mm) 0.25 g", "price": 85},
    {"id": "N1120-B", "description": "creos xenogain bowl cancellous (0.2-1.0 mm) 0.50 g", "price": 135},
    {"id": "N1130-B", "description": "creos xenogain bowl cancellous (0.2-1.0 mm) 1.00 g", "price": 217},
    {"id": "N1140-B", "description": "creos xenogain bowl cancellous (0.2-1.0 mm) 2.00 g", "price": 360},
    {"id": "N1111-B", "description": "creos xenogain bowl cancellous (1.0-2.0 mm) 0.25 g", "price": 85},
    {"id": "N1121-B", "description": "creos xenogain bowl cancellous (1.0-2.0 mm) 0.50 g", "price": 135},
    {"id": "N1131-B", "description": "creos xenogain bowl cancellous (1.0-2.0 mm) 1.00 g", "price": 217},
    {"id": "N1141-B", "description": "creos xenogain bowl cancellous (1.0-2.0 mm) 2.00 g", "price": 360},
    # creos xenogain - syringe
    {"id": "N1210", "description": "creos xenogain syringe cancellous (0.2-1.0 mm) 0.25 g", "price": 85},
    {"id": "N1220", "description": "creos xenogain syringe cancellous (0.2-1.0 mm) 0.50 g", "price": 135},
    {"id": "N1211", "description": "creos xenogain syringe cancellous (1.0-2.0 mm) 0.25 g", "price": 85},
    {"id": "N1221", "description": "creos xenogain syringe cancellous (1.0-2.0 mm) 0.50 g", "price": 135},
    # creos xenogain collagen
    {"id": "N1320", "description": "creos xenogain collagen block 6 x 6 x 6 mm, 100 mg", "price": 113},
    {"id": "N1330", "description": "creos xenogain collagen block 7 x 8 x 9 mm, 250 mg", "price": 213},
    {"id": "N1340", "description": "creos xenogain collagen block 9 x 10 x 11 mm, 500 mg", "price": 314},
    {"id": "N1410", "description": "creos xenogain collagen syringe 4.6 x 40 mm, 250 mg", "price": 213},
    {"id": "N1420", "description": "creos xenogain collagen syringe 5.6 x 45 mm, 500 mg", "price": 314},
    # NovaBone Dental Putty
    {"id": "NVANA1610", "description": "NovaBone Dental putty syringe 0.5 cc", "price": 108},
    {"id": "NVANA1611", "description": "NovaBone Dental putty syringe 1.0 cc", "price": 191},
    {"id": "NVANA1612", "description": "NovaBone Dental putty syringe 2.0 cc", "price": 338},
    {"id": "NVANA3620", "description": "NovaBone Dental putty cartridges 0.5 cc, 2/pk", "price": 211},
    {"id": "NVANA3660", "description": "NovaBone Dental putty cartridges 0.5 cc, 6/pk", "price": 521},
    # Zcore Expand Socket
    {"id": "CLMZXSOCKET-1", "description": "Zcore Expand Socket 1/pkg", "price": 79},
    {"id": "CLMZXSOCKET-5", "description": "Zcore Expand Socket 5/pkg", "price": 318},
    {"id": "CLMZXSOCKET-10", "description": "Zcore Expand Socket 10/pkg", "price": 582},
]

# 2026 Regenerative - Membranes
membrane_products = [
    # creos xenoprotect collagen membrane
    {"id": "N1520", "description": "creos xenoprotect collagen membrane 15 x 20 mm", "price": 170},
    {"id": "N2530", "description": "creos xenoprotect collagen membrane 25 x 30 mm", "price": 218},
    {"id": "N3040", "description": "creos xenoprotect collagen membrane 30 x 40 mm", "price": 351},
    # Cytoplast RTM collagen membrane
    {"id": "CLMRTM1520", "description": "Cytoplast RTM Collagen 15 x 20 mm, 2/pkg", "price": 239},
    {"id": "CLMRTM2030", "description": "Cytoplast RTM Collagen 20 x 30 mm, 2/pkg", "price": 294},
    {"id": "CLMRTM3040", "description": "Cytoplast RTM Collagen 30 x 40 mm, 2/pkg", "price": 423},
    # creos allo.protect pericardium membrane
    {"id": "N7110", "description": "creos allo.protect pericardium membrane 10 x 10 mm", "price": 119},
    {"id": "N7120", "description": "creos allo.protect pericardium membrane 15 x 20 mm", "price": 202},
    {"id": "N7140", "description": "creos allo.protect pericardium membrane 20 x 30 mm", "price": 271},
    # Cytoplast TXT-200 PTFE membranes
    {"id": "TXT1224", "description": "Cytoplast TXT-200 12 mm x 24 mm, 10/pkg", "price": 477},
    {"id": "TXT1224-1", "description": "Cytoplast TXT-200 12 mm x 24 mm, 1/pkg", "price": 58},
    {"id": "TXT1230", "description": "Cytoplast TXT-200 12 mm x 30 mm, 10/pkg", "price": 582},
    {"id": "TXT2530", "description": "Cytoplast TXT-200 25 mm x 30 mm, 4/pkg", "price": 318},
    {"id": "TXT2530-1", "description": "Cytoplast TXT-200 25 mm x 30 mm, 1/pkg", "price": 95},
    # Cytoplast Ti-150 titanium-reinforced
    {"id": "TI150ANL-N-1", "description": "Cytoplast Ti-150 ANL 12 mm x 24 mm, 1/pkg", "price": 132},
    {"id": "TI150ANL-N-2", "description": "Cytoplast Ti-150 ANL 12 mm x 24 mm, 2/pkg", "price": 228},
    {"id": "TI150AS-N-1", "description": "Cytoplast Ti-150 AS 14 mm x 24 mm, 1/pkg", "price": 169},
    {"id": "TI150AS-N-2", "description": "Cytoplast Ti-150 AS 14 mm x 24 mm, 2/pkg", "price": 291},
    {"id": "TI150BL-N-1", "description": "Cytoplast Ti-150 BL 17 mm x 25 mm, 1/pkg", "price": 180},
    {"id": "TI150BL-N-2", "description": "Cytoplast Ti-150 BL 17 mm x 25 mm, 2/pkg", "price": 307},
    {"id": "TI150BLL-N-1", "description": "Cytoplast Ti-150 BL Long 17 mm x 30 mm, 1/pkg", "price": 201},
    {"id": "TI150BLL-N-2", "description": "Cytoplast Ti-150 BL Long 17 mm x 30 mm, 2/pkg", "price": 349},
    {"id": "TI150K2-N-1", "description": "Cytoplast Ti-150 K2 40 mm x 50 mm, 1/pkg", "price": 418},
    {"id": "TI150K2-N-2", "description": "Cytoplast Ti-150 K2 40 mm x 50 mm, 2/pkg", "price": 715},
    {"id": "TI150PL-N-1", "description": "Cytoplast Ti-150 PL 25 mm x 30 mm, 1/pkg", "price": 238},
    {"id": "TI150PL-N-2", "description": "Cytoplast Ti-150 PL 25 mm x 30 mm, 2/pkg", "price": 408},
    {"id": "TI150PLT-N-1", "description": "Cytoplast Ti-150 PLT 41 mm x 50 mm, 1/pkg", "price": 286},
    {"id": "TI150PLT-N-2", "description": "Cytoplast Ti-150 PLT 41 mm x 50 mm, 2/pkg", "price": 487},
    {"id": "TI150PS-N-1", "description": "Cytoplast Ti-150 PS 20 mm x 25 mm, 1/pkg", "price": 217},
    {"id": "TI150PS-N-2", "description": "Cytoplast Ti-150 PS 20 mm x 25 mm, 2/pkg", "price": 371},
    # RTM Plug/Foam/Tape
    {"id": "CLMRTMPLUG10", "description": "Cytoplast RTMPlug 10/pkg", "price": 139},
    {"id": "CLMRTMFOAM10", "description": "Cytoplast RTMFoam 10/pkg", "price": 157},
    {"id": "CLMRTMTAPE10", "description": "Cytoplast RTMTape 2.5 cm x 7.5 cm, 10/pkg", "price": 217},
]

# 2026 Sutures
suture_products = [
    # Cytoplast PTFE sutures
    {"id": "CS0418", "description": "Cytoplast PTFE 18\" 2-0 USP, 3/8 circle 19 mm needle, 12/pkg", "price": 111},
    {"id": "CS0428", "description": "Cytoplast PTFE 28\" 2-0 USP, 3/8 circle 19 mm needle, 12/pkg", "price": 122},
    {"id": "CS0518", "description": "Cytoplast PTFE 18\" 3-0 USP, 3/8 circle 16 mm needle, 12/pkg", "price": 111},
    {"id": "CS0518BK", "description": "Cytoplast PTFE 18\" 3-0 USP, 3/8 circle black 16 mm needle, 12/pkg", "price": 122},
    {"id": "CS051819", "description": "Cytoplast PTFE 18\" 3-0 USP, 3/8 circle 19 mm needle, 12/pkg", "price": 111},
    {"id": "CS051819BK", "description": "Cytoplast PTFE 18\" 3-0 USP, 3/8 circle black 19 mm needle, 12/pkg", "price": 122},
    {"id": "CS0528", "description": "Cytoplast PTFE 28\" 3-0 USP, 3/8 circle 16 mm needle, 12/pkg", "price": 122},
    {"id": "CS0528BK", "description": "Cytoplast PTFE 28\" 3-0 USP, 3/8 circle black 16 mm needle, 12/pkg", "price": 132},
    {"id": "CS052819", "description": "Cytoplast PTFE 28\" 3-0 USP, 3/8 circle 19 mm needle, 12/pkg", "price": 122},
    {"id": "CS052819BK", "description": "Cytoplast PTFE 28\" 3-0 USP, 3/8 circle black 19 mm needle, 12/pkg", "price": 132},
    {"id": "CS0618PERIO", "description": "Cytoplast PTFE 18\" 4-0 USP, 1/2 circle 13 mm needle, 12/pkg", "price": 122},
    {"id": "CS0618PREM", "description": "Cytoplast PTFE 18\" 4-0 USP, 3/8 circle 13 mm needle, 12/pkg", "price": 122},
    {"id": "CS0618RC", "description": "Cytoplast PTFE 18\" 4-0 USP, 3/8 circle 16 mm needle, 12/pkg", "price": 122},
    {"id": "CS0628PERIO", "description": "Cytoplast PTFE 28\" 4-0 USP, 1/2 circle 13 mm needle, 12/pkg", "price": 132},
    {"id": "CS0628PREM", "description": "Cytoplast PTFE 28\" 4-0 USP, 3/8 circle 13 mm needle, 12/pkg", "price": 132},
    {"id": "CS0628RC", "description": "Cytoplast PTFE 28\" 4-0 USP, 3/8 circle 16 mm needle, 12/pkg", "price": 132},
    {"id": "CS071813", "description": "Cytoplast PTFE 18\" 5-0 USP, 3/8 circle 13 mm needle, 12/pkg", "price": 122},
    {"id": "CS071816", "description": "Cytoplast PTFE 18\" 5-0 USP, 3/8 circle 16 mm needle, 12/pkg", "price": 122},
    {"id": "CS072813", "description": "Cytoplast PTFE 28\" 5-0 USP, 3/8 circle 13 mm needle, 12/pkg", "price": 132},
    {"id": "CS072816", "description": "Cytoplast PTFE 28\" 5-0 USP, 3/8 circle 16 mm needle, 12/pkg", "price": 132},
    # Resorba Glycolon sutures
    {"id": "RMGOD01100", "description": "Glycolon 45 cm violet, 5-0 USP, 1/2 circle 16 mm needle, 12/pkg", "price": 86},
    {"id": "RMGOD01101", "description": "Glycolon 45 cm violet, 4-0 USP, 1/2 circle 18 mm needle, 12/pkg", "price": 86},
    {"id": "RMGOD01102", "description": "Glycolon 45 cm violet, 6-0 USP, 1/2 circle 10 mm needle, 12/pkg", "price": 109},
    {"id": "RMGOD01200", "description": "Glycolon 45 cm undyed, 6-0 USP, 3/8 circle 13 mm needle, 12/pkg", "price": 86},
    {"id": "RMGOD01201", "description": "Glycolon 45 cm violet, 4-0 USP, 3/8 circle 16 mm needle, 12/pkg", "price": 86},
    {"id": "RMGOD01202", "description": "Glycolon 45 cm undyed, 5-0 USP, 3/8 circle 18 mm needle, 12/pkg", "price": 86},
    {"id": "RMGOD01204", "description": "Glycolon 45 cm violet, 3-0 USP, 3/8 circle 16 mm needle, 12/pkg", "price": 86},
    {"id": "RMGOD01205", "description": "Glycolon 45 cm violet, 3-0 USP, 3/8 circle 18 mm needle, 12/pkg", "price": 86},
    {"id": "RMGOD01203", "description": "Glycolon 45 cm violet, 4-0 USP, 3/8 circle 18 mm needle, 12/pkg", "price": 86},
    {"id": "RMGOD01210", "description": "Glycolon 45 cm violet, 5-0 USP, 3/8 circle black 13 mm needle, 12/pkg", "price": 104},
    {"id": "RMGOD01211", "description": "Glycolon 45 cm violet, 5-0 USP, 3/8 circle black 16 mm needle, 12/pkg", "price": 104},
    {"id": "RMGOD01212", "description": "Glycolon 45 cm violet, 5-0 USP, 3/8 circle black 18 mm needle, 12/pkg", "price": 104},
    {"id": "RMGOD01214", "description": "Glycolon 45 cm violet, 5-0 USP, 3/8 circle 16 mm needle, 12/pkg", "price": 86},
    {"id": "RMGOD01213", "description": "Glycolon 45 cm violet, 6-0 USP, 3/8 circle 13 mm needle, 12/pkg", "price": 86},
    # X-Gut Chromic gut sutures
    {"id": "GC3019P45", "description": "Chromic gut 45 cm 3-0 USP, 3/8 circle 19 mm needle, 12/box", "price": 85},
    {"id": "GC3019P75", "description": "Chromic gut 75 cm 3-0 USP, 3/8 circle 19 mm needle, 12/box", "price": 83},
    {"id": "GC301945", "description": "Chromic gut 45 cm 3-0 USP, 3/8 circle 19 mm needle, 12/box", "price": 45},
    {"id": "GC301975", "description": "Chromic gut 75 cm 3-0 USP, 3/8 circle 19 mm needle, 12/box", "price": 43},
    {"id": "GC4013P45", "description": "Chromic gut 45 cm 4-0 USP, 3/8 circle 13 mm needle, 12/box", "price": 45},
    {"id": "GC4019P45", "description": "Chromic gut 45 cm 4-0 USP, 3/8 circle 19 mm needle, 12/box", "price": 83},
    {"id": "GC5013P45", "description": "Chromic gut 45 cm 5-0 USP, 3/8 circle 13 mm needle, 12/box", "price": 83},
    {"id": "GC5016P45", "description": "Chromic gut 45 cm 5-0 USP, 3/8 circle 16 mm needle, 12/box", "price": 43},
]

# Add new categories
products['Regenerative - Grafting'] = grafting_products
products['Regenerative - Membranes'] = membrane_products
products['Sutures'] = suture_products

# Write updated products
with open('products.json', 'w') as f:
    json.dump(products, f, indent=2)

print(f"Added {len(grafting_products)} grafting products (2026 pricing)")
print(f"Added {len(membrane_products)} membrane products (2026 pricing)")
print(f"Added {len(suture_products)} suture products (2026 pricing)")
print(f"Total categories: {len(products)}")
