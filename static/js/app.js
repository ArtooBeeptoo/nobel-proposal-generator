/**
 * Nobel Biocare Proposal Tool v2 - Frontend JS
 */

// Quote State
let quote = {
    items: [],
    categoryDiscounts: {}
};

// Load quote from localStorage on init
document.addEventListener('DOMContentLoaded', () => {
    loadQuote();
    renderQuote();
});

// ── Quote Management ──

function loadQuote() {
    const saved = localStorage.getItem('nobelQuote');
    if (saved) {
        quote = JSON.parse(saved);
    }
}

function saveQuote() {
    localStorage.setItem('nobelQuote', JSON.stringify(quote));
    renderQuote();
}

function addToQuote(id, description, price, quantity, discount, category) {
    // Check if item already exists
    const existingIndex = quote.items.findIndex(item => item.id === id);
    
    if (existingIndex >= 0) {
        // Update existing item
        quote.items[existingIndex].quantity = quantity;
        quote.items[existingIndex].discount = discount;
    } else {
        // Add new item
        quote.items.push({
            id,
            description,
            price: parseFloat(price),
            quantity: parseInt(quantity) || 1,
            discount: parseFloat(discount) || 0,
            category
        });
    }
    
    saveQuote();
    showToast(`Added ${description.substring(0, 30)}...`);
}

function removeFromQuote(id) {
    quote.items = quote.items.filter(item => item.id !== id);
    saveQuote();
}

function updateQuoteItem(id, field, value) {
    const item = quote.items.find(item => item.id === id);
    if (item) {
        if (field === 'quantity') {
            item.quantity = parseInt(value) || 1;
        } else if (field === 'discount') {
            item.discount = parseFloat(value) || 0;
        }
        saveQuote();
    }
}

function clearQuote() {
    if (confirm('Clear all items from quote?')) {
        quote.items = [];
        quote.categoryDiscounts = {};
        saveQuote();
    }
}

function applyCategoryDiscount(category, discount) {
    quote.categoryDiscounts[category] = parseFloat(discount) || 0;
    
    // Apply to all items in category
    quote.items.forEach(item => {
        if (item.category === category) {
            item.discount = quote.categoryDiscounts[category];
        }
    });
    
    saveQuote();
    
    // Update UI inputs
    document.querySelectorAll(`.product-card[data-category="${category}"] .discount-input`).forEach(input => {
        input.value = discount;
    });
    
    showToast(`Applied ${discount}% to all ${category} items`);
}

// ── Rendering ──

function renderQuote() {
    const container = document.getElementById('quoteItems');
    const countBadge = document.getElementById('quoteCount');
    const listTotalEl = document.getElementById('quoteListTotal');
    const savingsEl = document.getElementById('quoteSavings');
    const totalEl = document.getElementById('quoteTotal');
    
    if (!container) return;
    
    // Update count badge
    if (countBadge) {
        countBadge.textContent = quote.items.length;
    }
    
    if (quote.items.length === 0) {
        container.innerHTML = '<div class="empty-quote">No items added yet</div>';
        if (listTotalEl) listTotalEl.textContent = '$0.00';
        if (savingsEl) savingsEl.textContent = '$0.00';
        if (totalEl) totalEl.textContent = '$0.00';
        return;
    }
    
    let listTotal = 0;
    let netTotal = 0;
    let html = '';
    
    quote.items.forEach(item => {
        const listPrice = item.price * item.quantity;
        const netPrice = item.price * (1 - item.discount / 100);
        const extended = netPrice * item.quantity;
        listTotal += listPrice;
        netTotal += extended;
        
        html += `
            <div class="quote-item">
                <div class="quote-item-header">
                    <span class="quote-item-id">#${item.id}</span>
                    <button class="quote-item-remove" onclick="removeFromQuote('${item.id}')">✕</button>
                </div>
                <div class="quote-item-desc">${item.description.substring(0, 50)}</div>
                <div class="quote-item-details">
                    <span>Qty: ${item.quantity} × $${netPrice.toFixed(2)}</span>
                    <span class="quote-item-extended">$${extended.toFixed(2)}</span>
                </div>
                ${item.discount > 0 ? `<div class="quote-item-discount" style="font-size: 0.75rem; color: #059669;">${item.discount.toFixed(2)}% off</div>` : ''}
            </div>
        `;
    });
    
    container.innerHTML = html;
    
    const savings = listTotal - netTotal;
    
    if (listTotalEl) listTotalEl.textContent = `$${listTotal.toFixed(2)}`;
    if (savingsEl) savingsEl.textContent = `$${savings.toFixed(2)}`;
    if (totalEl) totalEl.textContent = `$${netTotal.toFixed(2)}`;
}

// ── Quote Panel ──

function toggleQuotePanel() {
    const panel = document.getElementById('quotePanel');
    const main = document.querySelector('.main-content');
    
    if (panel) {
        panel.classList.toggle('open');
    }
    if (main) {
        main.classList.toggle('quote-open');
    }
}

// ── Product Actions ──

function addProduct(button) {
    const card = button.closest('.product-card');
    const id = card.dataset.id;
    const description = card.dataset.description;
    const price = card.dataset.price;
    const category = card.dataset.category;
    
    const qtyInput = card.querySelector('.qty-input');
    const discountInput = card.querySelector('.discount-input');
    
    const quantity = qtyInput ? parseInt(qtyInput.value) || 1 : 1;
    
    // Use category discount if set, otherwise use individual input
    let discount = 0;
    if (quote.categoryDiscounts && quote.categoryDiscounts[category]) {
        discount = quote.categoryDiscounts[category];
    } else {
        discount = discountInput ? parseFloat(discountInput.value) || 0 : 0;
    }
    
    addToQuote(id, description, price, quantity, discount, category);
}

// ── Kit Actions ──

function toggleKitComponents(button) {
    const card = button.closest('.kit-card');
    const components = card.querySelector('.kit-components');
    
    if (components) {
        components.classList.toggle('show');
        button.textContent = components.classList.contains('show') ? 'Hide Components' : 'Show Components';
    }
}

function addKit(kitId, kitName, kitPrice) {
    const card = document.querySelector(`.kit-card[data-id="${kitId}"]`);
    const qtyInput = card.querySelector('.qty-input');
    const discountInput = card.querySelector('.discount-input');
    
    const quantity = qtyInput ? parseInt(qtyInput.value) || 1 : 1;
    const discount = discountInput ? parseFloat(discountInput.value) || 0 : 0;
    
    addToQuote(kitId, kitName, kitPrice, quantity, discount, 'surgical_kits');
}

// ── Generate Documents ──

async function generatePDF() {
    if (quote.items.length === 0) {
        showToast('Add items to quote first', 'error');
        return;
    }
    
    const customerName = document.getElementById('customerName')?.value || '';
    const validThrough = document.getElementById('validThrough')?.value || '';
    const repName = document.getElementById('repName')?.value || '';
    const repTitle = document.getElementById('repTitle')?.value || '';
    const repPhone = document.getElementById('repPhone')?.value || '';
    const repEmail = document.getElementById('repEmail')?.value || '';
    const notes = document.getElementById('proposalNotes')?.value || '';
    
    try {
        const response = await fetch('/api/generate-pdf', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                items: quote.items,
                customerName: customerName,
                validThrough: validThrough,
                repName: repName,
                repTitle: repTitle,
                repPhone: repPhone,
                repEmail: repEmail,
                notes: notes
            })
        });
        
        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `Nobel_Proposal_${new Date().toISOString().slice(0,10)}.pdf`;
            document.body.appendChild(a);
            a.click();
            a.remove();
            window.URL.revokeObjectURL(url);
            showToast('PDF generated!');
        } else {
            showToast('Failed to generate PDF', 'error');
        }
    } catch (err) {
        console.error(err);
        showToast('Error generating PDF', 'error');
    }
}

async function generateDocx() {
    if (quote.items.length === 0) {
        showToast('Add items to quote first', 'error');
        return;
    }
    
    const customerName = document.getElementById('customerName')?.value || '';
    const validThrough = document.getElementById('validThrough')?.value || '';
    const repName = document.getElementById('repName')?.value || '';
    const repTitle = document.getElementById('repTitle')?.value || '';
    const repPhone = document.getElementById('repPhone')?.value || '';
    const repEmail = document.getElementById('repEmail')?.value || '';
    
    try {
        const response = await fetch('/api/generate-docx', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                items: quote.items,
                customerName: customerName,
                validThrough: validThrough,
                repName: repName,
                repTitle: repTitle,
                repPhone: repPhone,
                repEmail: repEmail
            })
        });
        
        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `Nobel_Proposal_${new Date().toISOString().slice(0,10)}.docx`;
            document.body.appendChild(a);
            a.click();
            a.remove();
            window.URL.revokeObjectURL(url);
            showToast('Word doc generated!');
        } else {
            showToast('Failed to generate Word doc', 'error');
        }
    } catch (err) {
        console.error(err);
        showToast('Error generating Word doc', 'error');
    }
}

// ── Toast Notifications ──

function showToast(message, type = 'success') {
    // Remove existing toast
    const existing = document.querySelector('.toast');
    if (existing) existing.remove();
    
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    toast.style.cssText = `
        position: fixed;
        bottom: 100px;
        right: 30px;
        padding: 12px 24px;
        background: ${type === 'error' ? '#dc2626' : '#059669'};
        color: white;
        border-radius: 6px;
        font-size: 14px;
        z-index: 1000;
        animation: slideIn 0.3s ease;
    `;
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.style.animation = 'fadeOut 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, 2500);
}

// Add CSS for animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    @keyframes fadeOut {
        from { opacity: 1; }
        to { opacity: 0; }
    }
`;
document.head.appendChild(style);
