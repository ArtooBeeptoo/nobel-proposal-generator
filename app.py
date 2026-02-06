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
from weasyprint import HTML, CSS

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'nobel-proposal-2026')

# Simple password - set via environment variable
APP_PASSWORD = os.environ.get('APP_PASSWORD', 'nobel2026')

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
    return render_template('index.html', categories=categories, products=products)

@app.route('/generate', methods=['POST'])
@login_required
def generate():
    products = get_products()
    
    # Get form data
    account_name = request.form.get('account_name', 'Customer')
    discount_percent = float(request.form.get('discount', 0))
    output_format = request.form.get('output_format', 'docx')
    rep_name = request.form.get('rep_name', '')
    
    # Parse selected items
    items = []
    for key, value in request.form.items():
        if key.startswith('qty_') and value and int(value) > 0:
            item_id = key.replace('qty_', '')
            qty = int(value)
            
            # Find the product
            for category, prods in products.items():
                for prod in prods:
                    if prod['id'] == item_id:
                        items.append({
                            'id': item_id,
                            'description': prod['description'],
                            'list_price': prod['price'],
                            'quantity': qty
                        })
                        break
    
    if not items:
        flash('Please select at least one product', 'error')
        return redirect(url_for('index'))
    
    # Calculate totals
    list_total = sum(item['list_price'] * item['quantity'] for item in items)
    discount_amount = list_total * (discount_percent / 100)
    final_total = list_total - discount_amount
    
    proposal_data = {
        'account_name': account_name,
        'rep_name': rep_name,
        'date': datetime.now().strftime('%B %d, %Y'),
        'items': items,
        'discount_percent': discount_percent,
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
    table = doc.add_table(rows=1, cols=3)
    table.style = 'Table Grid'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    # Header row
    header_cells = table.rows[0].cells
    header_cells[0].text = 'Description'
    header_cells[1].text = 'Qty'
    header_cells[2].text = 'Item #'
    
    for cell in header_cells:
        cell.paragraphs[0].runs[0].bold = True
    
    # Add items
    for item in data['items']:
        row = table.add_row().cells
        row[0].text = item['description']
        row[1].text = str(item['quantity'])
        row[2].text = item['id']
    
    doc.add_paragraph()
    
    # Totals
    doc.add_paragraph(f"List Price Total: ${data['list_total']:,.2f}")
    doc.add_paragraph(f"Discount ({data['discount_percent']:.0f}%): -${data['discount_amount']:,.2f}")
    
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
    """Generate PDF document"""
    
    # Build HTML
    items_html = ""
    for item in data['items']:
        items_html += f"""
        <tr>
            <td>{item['description']}</td>
            <td style="text-align: center;">{item['quantity']}</td>
            <td>{item['id']}</td>
        </tr>
        """
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            h1 {{ color: #003366; text-align: center; margin-bottom: 5px; }}
            h2 {{ color: #666; text-align: center; margin-top: 5px; font-weight: normal; }}
            .info {{ margin: 30px 0; }}
            table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
            th, td {{ border: 1px solid #ddd; padding: 10px; text-align: left; }}
            th {{ background-color: #003366; color: white; }}
            .totals {{ margin-top: 30px; }}
            .totals p {{ margin: 5px 0; }}
            .final-price {{ font-size: 18px; font-weight: bold; color: #003366; }}
            .savings {{ font-size: 16px; font-weight: bold; color: #228B22; }}
            .footer {{ margin-top: 40px; color: #666; font-size: 12px; }}
        </style>
    </head>
    <body>
        <h1>Nobel Biocare</h1>
        <h2>Custom Sales Offer</h2>
        
        <div class="info">
            <p><strong>Prepared for:</strong> {data['account_name']}</p>
            <p><strong>Date:</strong> {data['date']}</p>
            {"<p><strong>Territory Manager:</strong> " + data['rep_name'] + "</p>" if data['rep_name'] else ""}
        </div>
        
        <table>
            <thead>
                <tr>
                    <th>Description</th>
                    <th style="width: 60px;">Qty</th>
                    <th style="width: 100px;">Item #</th>
                </tr>
            </thead>
            <tbody>
                {items_html}
            </tbody>
        </table>
        
        <div class="totals">
            <p>List Price Total: ${data['list_total']:,.2f}</p>
            <p>Discount ({data['discount_percent']:.0f}%): -${data['discount_amount']:,.2f}</p>
            <p class="final-price">Your Price: ${data['final_total']:,.2f}</p>
            <p class="savings">You Save: ${data['discount_amount']:,.2f}</p>
        </div>
        
        <div class="footer">
            <p>Thank you for choosing Nobel Biocare!</p>
            <p>Prices valid for 30 days from date of proposal.</p>
        </div>
    </body>
    </html>
    """
    
    # Generate PDF
    buffer = BytesIO()
    HTML(string=html_content).write_pdf(buffer)
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
