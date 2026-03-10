"""
Nobel Biocare Proposal Generator v2
Complete overhaul with sidebar navigation, filters, and structured categories.
"""

import os
import json
from datetime import datetime
from io import BytesIO
from functools import wraps

from flask import Flask, render_template, request, redirect, url_for, session, send_file, flash, jsonify

# Use the custom proposal generator
from proposal_generator import generate_pdf as gen_pdf, generate_docx as gen_docx

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'nobel-proposal-v2-2026')
APP_PASSWORD = os.environ.get('APP_PASSWORD', 'nobel2026')

# ── Implant system filters ──
IMPLANT_FILTERS = [
    ('s_series', 'S Series (Active/Parallel/Replace)'),
    ('nobel_active', 'NobelActive'),
    ('nobel_parallel', 'NobelParallel'),
    ('nobel_replace', 'NobelReplace CC'),
    ('tcc', 'N1 (TCC)'),
    ('nobel_pearl', 'NobelPearl'),
    ('zygomatic', 'Zygomatic'),
    ('ext_hex', 'Brånemark (Ext Hex)'),
]

# ── Platform filters (for prosthetics) ──
PLATFORM_FILTERS = [
    ('cc', 'Conical Connection'),
    ('tcc', 'Trioval CC (N1)'),
    ('ext_hex', 'External Hex'),
    ('tri_channel', 'Tri-Channel'),
    ('nobel_pearl', 'NobelPearl'),
    ('zygomatic', 'Zygomatic'),
]

# ── Locator-specific filters ──
LOCATOR_FILTERS = [
    ('cc', 'Conical Connection'),
    ('ext_hex', 'External Hex'),
    ('tri_channel', 'Tri-Channel'),
]

# ── System filters (for tooling) ──
SYSTEM_FILTERS = [
    ('nobel_active', 'NobelActive'),
    ('nobel_parallel', 'NobelParallel'),
    ('nobel_replace', 'NobelReplace'),
    ('nobel_pearl', 'NobelPearl'),
    ('zygomatic', 'Zygomatic'),
    ('retrieval', 'Retrieval Tools'),
]

# ── Category Structure ──
CATEGORIES = {
    # Products with platform filters
    'implants': {'name': 'Implants', 'icon': '🦷', 'order': 1, 'filters': 'implant'},
    'healing_abutments': {'name': 'Healing Abutments', 'icon': '🩹', 'order': 2, 'filters': 'platform'},
    'cover_screws': {'name': 'Cover Screws', 'icon': '⚙️', 'order': 3, 'filters': 'platform'},
    'stock_abutments': {'name': 'Stock Abutments', 'icon': '🔧', 'order': 4, 'filters': 'platform'},
    'temp_abutments': {'name': 'Temp Abutments', 'icon': '⏱️', 'order': 5, 'filters': 'platform'},
    'multiunit_abutments': {'name': 'Multi-Unit Abutments', 'icon': '🔩', 'order': 6, 'filters': 'platform'},
    'locator_abutments': {'name': 'Locator Abutments', 'icon': '📍', 'order': 7, 'filters': 'locator'},
    'impression_taking': {'name': 'Impression Taking', 'icon': '📐', 'order': 8, 'filters': 'platform'},
    'procera_lab': {'name': 'Procera Lab', 'icon': '🏭', 'order': 9, 'filters': 'platform'},
    'screws': {'name': 'Screws', 'icon': '🔩', 'order': 10, 'filters': 'platform'},
    'replicas': {'name': 'Replicas', 'icon': '🔄', 'order': 11, 'filters': 'platform'},
    'prosthetic_drivers': {'name': 'Prosthetic Drivers', 'icon': '🔧', 'order': 12, 'filters': None},
    
    # Regeneratives and Sutures
    'regeneratives': {'name': 'Regeneratives', 'icon': '🧬', 'order': 13, 'filters': None},
    'sutures': {'name': 'Sutures', 'icon': '🧵', 'order': 14, 'filters': None},
    
    # Equipment
    'tooling': {'name': 'Tooling', 'icon': '🛠️', 'order': 15, 'filters': 'system'},
    'motors': {'name': 'Motors', 'icon': '⚡', 'order': 16, 'filters': None, 'hover': True},
    
    # Digital/Capital
    'scanners': {'name': 'Intraoral Scanners', 'icon': '📷', 'order': 17, 'filters': ['DEXIS', 'TRIOS'], 'filter_field': 'brand', 'hover': True},
    'sprintray': {'name': 'SprintRay', 'icon': '🖨️', 'order': 19, 'filters': None, 'hover': True},
    'icam': {'name': 'iCAM', 'icon': '🎥', 'order': 20, 'filters': None, 'hover': True},
    'xguide': {'name': 'X-Guide', 'icon': '🎯', 'order': 21, 'filters': None, 'hover': True},
    'dtx_studio': {'name': 'DTX Studio', 'icon': '💻', 'order': 22, 'filters': None},
}

# ── Load data files ──
def load_json(filename):
    filepath = os.path.join(os.path.dirname(__file__), 'data', filename)
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return json.load(f)
    return []  # Return empty list

def get_products():
    return load_json('products.json')

def get_kits():
    return load_json('kits.json')

def get_promos():
    return load_json('promos.json')

def get_components():
    return load_json('components.json')

# ── Auth ──
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('password') == APP_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('index'))
        flash('Invalid password', 'error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

# ── Main Routes ──
@app.route('/')
@login_required
def index():
    products = get_products()
    return render_template('index.html', 
                         categories=CATEGORIES,
                         products=products)

@app.route('/category/<cat_id>')
@login_required
def category(cat_id):
    if cat_id not in CATEGORIES:
        flash('Category not found', 'error')
        return redirect(url_for('index'))
    
    products = get_products()
    cat_products = products.get(cat_id, [])
    cat_info = CATEGORIES[cat_id]
    
    # Determine which filters to show
    filters = None
    filter_type = cat_info.get('filters')
    if filter_type == 'implant':
        filters = IMPLANT_FILTERS
    elif filter_type == 'platform':
        filters = PLATFORM_FILTERS
    elif filter_type == 'locator':
        filters = LOCATOR_FILTERS
    elif filter_type == 'system':
        filters = SYSTEM_FILTERS
    elif isinstance(filter_type, list):
        # Direct list of filters (e.g., for scanners: ['DEXIS', 'TRIOS'])
        filters = [(v, v) for v in filter_type]
    
    # Get components for hover if applicable
    components = get_components() if cat_info.get('hover') else {}
    
    return render_template('category.html',
                         categories=CATEGORIES,
                         current_category=cat_id,
                         category_info=cat_info,
                         products=cat_products,
                         filters=filters,
                         filter_type=filter_type,
                         components=components)

@app.route('/kits')
@login_required
def kits():
    return render_template('kits.html',
                         categories=CATEGORIES,
                         kits=get_kits(),
                         components=get_components())

@app.route('/promos')
@login_required
def promos():
    promo_data = get_promos()
    return render_template('promos.html',
                         categories=CATEGORIES,
                         promos=promo_data if isinstance(promo_data, list) else [])

@app.route('/new-starts')
@login_required
def new_starts():
    return render_template('new_starts.html',
                         categories=CATEGORIES)

@app.route('/exchange')
@login_required
def exchange():
    products = get_products()
    ref_lookup = {}
    if isinstance(products, dict):
        for cat_products in products.values():
            if not isinstance(cat_products, list):
                continue
            for product in cat_products:
                if not isinstance(product, dict):
                    continue
                ref = str(product.get('id', '')).strip()
                description = str(product.get('description', '')).strip()
                if ref and description and ref not in ref_lookup:
                    ref_lookup[ref] = description

    return render_template('exchange.html',
                         categories=CATEGORIES,
                         ref_lookup=ref_lookup)

# ── API Routes ──
@app.route('/api/products/<cat_id>')
@login_required
def api_products(cat_id):
    products = get_products()
    return jsonify(products.get(cat_id, []))

@app.route('/api/kit/<kit_id>')
@login_required
def api_kit(kit_id):
    kits = get_kits()
    for kit_type, kit_list in kits.items():
        for kit in kit_list:
            if kit.get('id') == kit_id:
                return jsonify(kit)
    return jsonify({'error': 'Kit not found'}), 404

@app.route('/api/promo/<promo_id>')
@login_required
def api_promo(promo_id):
    promos = get_promos()
    if isinstance(promos, list):
        for promo in promos:
            if promo.get('id') == promo_id:
                return jsonify(promo)
    return jsonify({'error': 'Promo not found'}), 404

@app.route('/api/components/<item_id>')
@login_required
def api_components(item_id):
    components = get_components()
    return jsonify(components.get(item_id, []))

@app.route('/api/generate-pdf', methods=['POST'])
@login_required
def generate_pdf():
    """Generate PDF proposal in Nobel Biocare format"""
    data = request.json
    items = data.get('items', [])
    customer_name = data.get('customerName', '')
    valid_through = data.get('validThrough', '')
    rep_name = data.get('repName', '')
    rep_title = data.get('repTitle', '')
    rep_phone = data.get('repPhone', '')
    rep_email = data.get('repEmail', '')
    notes = data.get('notes', '')
    
    if not items:
        return jsonify({'error': 'No items in quote'}), 400
    
    buffer = gen_pdf(items, customer_name, valid_through, rep_name, rep_title, rep_phone, rep_email, notes)
    
    return send_file(buffer, mimetype='application/pdf', as_attachment=True,
                    download_name=f"Nobel_Proposal_{datetime.now().strftime('%Y%m%d')}.pdf")

@app.route('/api/generate-docx', methods=['POST'])
@login_required
def generate_docx():
    """Generate Word proposal in Nobel Biocare format"""
    data = request.json
    items = data.get('items', [])
    customer_name = data.get('customerName', '')
    valid_through = data.get('validThrough', '')
    rep_name = data.get('repName', '')
    rep_title = data.get('repTitle', '')
    rep_phone = data.get('repPhone', '')
    rep_email = data.get('repEmail', '')
    
    if not items:
        return jsonify({'error': 'No items in quote'}), 400
    
    buffer = gen_docx(items, customer_name, valid_through, rep_name, rep_title, rep_phone, rep_email)
    
    return send_file(buffer, mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                    as_attachment=True, download_name=f"Nobel_Proposal_{datetime.now().strftime('%Y%m%d')}.docx")

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', debug=False, port=port)
