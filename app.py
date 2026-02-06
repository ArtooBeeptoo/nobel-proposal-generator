"""
Nobel Biocare Proposal Generator
A simple web app for generating custom sales proposals
"""

import os
import re
import json
from datetime import datetime
from io import BytesIO
from functools import wraps

from flask import Flask, render_template, request, redirect, url_for, session, send_file, flash
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'nobel-proposal-2026')

# Simple password - set via environment variable
APP_PASSWORD = os.environ.get('APP_PASSWORD', 'nobel2026')

# Discount groups - maps categories to discount group names
DISCOUNT_GROUPS = {
    'Implants': ['NobelActive TiUltra Implants', 'NobelActive Implants', 'Nobel Biocare N1 TiUltra Implants', 
                 'NobelParallel CC TiUltra Implants', 'NobelReplace CC TiUltra Implants', 'NobelPearl Ceramic Implants', 
                 'NobelZygoma Implants'],
    'Abutments': ['Esthetic Abutments', 'Multi-Unit Abutments', 'Locator Abutments', 'GoldAdapt Abutments'],
    'Kits': ['Surgical Kits'],
    '3Shape': ['Capital - 3Shape'],
    'SprintRay': ['Capital - SprintRay'],
    'DEXIS': ['Capital - DEXIS'],
    'X-Guide': ['Capital - X-Guide'],
    'iCAM': ['Capital - iCAM'],
    'DTX': ['Capital - DTX'],
}

def get_discount_group(category):
    """Get the discount group for a category"""
    for group, cats in DISCOUNT_GROUPS.items():
        if category in cats:
            return group
    return 'Other'

# Load product catalog
def load_products():
    """Load products from JSON file"""
    catalog_path = os.path.join(os.path.dirname(__file__), 'products.json')
    with open(catalog_path, 'r') as f:
        return json.load(f)

PRODUCTS = None

def get_products():
    global PRODUCTS
    if PRODUCTS is None:
        PRODUCTS = load_products()
    return PRODUCTS

# Auth decorator
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

@app.route('/')
@login_required
def index():
    products = get_products()
    categories = list(products.keys())
    discount_groups = list(DISCOUNT_GROUPS.keys()) + ['Other']
    return render_template('index.html', categories=categories, products=products, 
                         discount_groups=discount_groups, get_discount_group=get_discount_group)

@app.route('/generate', methods=['POST'])
@login_required
def generate():
    products = get_products()
    
    # Get form data
    account_name = request.form.get('account_name', 'Customer')
    output_format = request.form.get('output_format', 'docx')
    rep_name = request.form.get('rep_name', '')
    
    # Get per-group discounts
    group_discounts = {}
    for group in list(DISCOUNT_GROUPS.keys()) + ['Other']:
        discount_key = f'discount_{group.replace(" ", "_").replace("-", "_")}'
        group_discounts[group] = float(request.form.get(discount_key, 0))
    
    # Parse selected items
    items = []
    for key, value in request.form.items():
        if key.startswith('qty_') and value and int(value) > 0:
            item_id = key.replace('qty_', '')
            qty = int(value)
            
            # Find the product and its category
            for category, prods in products.items():
                for prod in prods:
                    if prod['id'] == item_id:
                        discount_group = get_discount_group(category)
                        discount_pct = group_discounts.get(discount_group, 0)
                        list_price = prod['price']
                        discounted_price = list_price * (1 - discount_pct / 100)
                        
                        items.append({
                            'id': item_id,
                            'description': prod['description'],
                            'list_price': list_price,
                            'discount_pct': discount_pct,
                            'discounted_price': discounted_price,
                            'quantity': qty,
                            'category': category
                        })
                        break
    
    if not items:
        flash('Please select at least one product', 'error')
        return redirect(url_for('index'))
    
    # Calculate totals
    list_total = sum(item['list_price'] * item['quantity'] for item in items)
    final_total = sum(item['discounted_price'] * item['quantity'] for item in items)
    discount_amount = list_total - final_total
    
    proposal_data = {
        'account_name': account_name,
        'rep_name': rep_name,
        'date': datetime.now().strftime('%B %d, %Y'),
        'items': items,
        'list_total': list_total,
        'discount_amount': discount_amount,
        'final_total': final_total
    }
    
    if output_format == 'pdf':
        return generate_pdf(proposal_data)
    else:
        return generate_docx(proposal_data)

def generate_docx(data):
    """Generate Word document"""
    doc = Document()
    
    # Title
    title = doc.add_heading('Nobel Biocare', 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    subtitle = doc.add_heading('Custom Sales Offer', level=1)
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # Account info
    doc.add_paragraph()
    doc.add_paragraph(f"Prepared for: {data['account_name']}")
    doc.add_paragraph(f"Date: {data['date']}")
    if data['rep_name']:
        doc.add_paragraph(f"Territory Manager: {data['rep_name']}")
    doc.add_paragraph()
    
    # Items table
    table = doc.add_table(rows=1, cols=4)
    table.style = 'Table Grid'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    # Header row
    header_cells = table.rows[0].cells
    header_cells[0].text = 'Description'
    header_cells[1].text = 'Qty'
    header_cells[2].text = 'Item #'
    header_cells[3].text = 'Discount'
    
    for cell in header_cells:
        cell.paragraphs[0].runs[0].bold = True
    
    # Add items
    for item in data['items']:
        row = table.add_row().cells
        row[0].text = item['description']
        row[1].text = str(item['quantity'])
        row[2].text = item['id']
        row[3].text = f"{item['discount_pct']:.0f}%"
    
    doc.add_paragraph()
    
    # Totals
    doc.add_paragraph(f"List Price Total: ${data['list_total']:,.2f}")
    doc.add_paragraph(f"Total Discount: -${data['discount_amount']:,.2f}")
    
    final_para = doc.add_paragraph()
    final_run = final_para.add_run(f"Your Price: ${data['final_total']:,.2f}")
    final_run.bold = True
    final_run.font.size = Pt(14)
    
    savings_para = doc.add_paragraph()
    savings_run = savings_para.add_run(f"You Save: ${data['discount_amount']:,.2f}")
    savings_run.bold = True
    
    # Footer
    doc.add_paragraph()
    doc.add_paragraph("Thank you for choosing Nobel Biocare!")
    doc.add_paragraph("Prices valid for 30 days from date of proposal.")
    
    # Save to BytesIO
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    
    filename = f"Nobel_Proposal_{data['account_name'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.docx"
    
    return send_file(
        buffer,
        as_attachment=True,
        download_name=filename,
        mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )

def generate_pdf(data):
    """Generate PDF document using ReportLab"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('Title', parent=styles['Heading1'], fontSize=24, textColor=colors.HexColor('#003366'), alignment=1)
    subtitle_style = ParagraphStyle('Subtitle', parent=styles['Heading2'], fontSize=16, textColor=colors.grey, alignment=1)
    normal_style = styles['Normal']
    
    elements = []
    
    # Title
    elements.append(Paragraph("Nobel Biocare", title_style))
    elements.append(Paragraph("Custom Sales Offer", subtitle_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # Info
    elements.append(Paragraph(f"<b>Prepared for:</b> {data['account_name']}", normal_style))
    elements.append(Paragraph(f"<b>Date:</b> {data['date']}", normal_style))
    if data['rep_name']:
        elements.append(Paragraph(f"<b>Territory Manager:</b> {data['rep_name']}", normal_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # Table
    table_data = [['Description', 'Qty', 'Item #', 'Disc.']]
    for item in data['items']:
        table_data.append([item['description'], str(item['quantity']), item['id'], f"{item['discount_pct']:.0f}%"])
    
    table = Table(table_data, colWidths=[3.5*inch, 0.5*inch, 1.2*inch, 0.6*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003366')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.lightgrey),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Totals
    elements.append(Paragraph(f"List Price Total: ${data['list_total']:,.2f}", normal_style))
    elements.append(Paragraph(f"Total Discount: -${data['discount_amount']:,.2f}", normal_style))
    elements.append(Spacer(1, 0.1*inch))
    
    final_style = ParagraphStyle('Final', parent=styles['Normal'], fontSize=14, fontName='Helvetica-Bold', textColor=colors.HexColor('#003366'))
    elements.append(Paragraph(f"Your Price: ${data['final_total']:,.2f}", final_style))
    
    savings_style = ParagraphStyle('Savings', parent=styles['Normal'], fontSize=12, fontName='Helvetica-Bold', textColor=colors.HexColor('#228B22'))
    elements.append(Paragraph(f"You Save: ${data['discount_amount']:,.2f}", savings_style))
    elements.append(Spacer(1, 0.4*inch))
    
    # Footer
    footer_style = ParagraphStyle('Footer', parent=styles['Normal'], fontSize=10, textColor=colors.grey)
    elements.append(Paragraph("Thank you for choosing Nobel Biocare!", footer_style))
    elements.append(Paragraph("Prices valid for 30 days from date of proposal.", footer_style))
    
    doc.build(elements)
    buffer.seek(0)
    
    filename = f"Nobel_Proposal_{data['account_name'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.pdf"
    
    return send_file(
        buffer,
        as_attachment=True,
        download_name=filename,
        mimetype='application/pdf'
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
