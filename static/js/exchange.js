/**
 * Exchange Template Generator
 * Client-side OCR with Tesseract.js and template output helpers.
 */

document.addEventListener('DOMContentLoaded', () => {
    const refLookup = window.exchangeRefLookup || {};
    const selectedImages = [];
    const items = [];

    const dropZone = document.getElementById('dropZone');
    const imageInput = document.getElementById('imageInput');
    const uploadList = document.getElementById('uploadList');
    const runOcrBtn = document.getElementById('runOcrBtn');
    const clearImagesBtn = document.getElementById('clearImagesBtn');
    const addRowBtn = document.getElementById('addRowBtn');
    const generateTemplateBtn = document.getElementById('generateTemplateBtn');
    const copyTemplateBtn = document.getElementById('copyTemplateBtn');
    const downloadTemplateBtn = document.getElementById('downloadTemplateBtn');
    const ocrStatus = document.getElementById('ocrStatus');
    const tableBody = document.getElementById('exchangeItemsBody');
    const templateOutput = document.getElementById('templateOutput');

    function showStatus(message, isError = false) {
        ocrStatus.textContent = message;
        ocrStatus.style.color = isError ? '#991b1b' : 'var(--text-secondary)';
    }

    function addImages(fileList) {
        Array.from(fileList).forEach((file) => {
            if (!file.type.startsWith('image/')) {
                return;
            }
            selectedImages.push(file);
        });
        renderUploadList();
    }

    function renderUploadList() {
        if (selectedImages.length === 0) {
            uploadList.innerHTML = '';
            return;
        }

        uploadList.innerHTML = selectedImages
            .map((file, index) => `<div class="upload-pill">${index + 1}. ${escapeHtml(file.name)}</div>`)
            .join('');
    }

    function createItemRow(data = {}) {
        items.push({
            ref: data.ref || '',
            description: data.description || '',
            lot: data.lot || '',
            qty: data.qty || 1,
            confidence: data.confidence || ''
        });
        renderItems();
    }

    function renderItems() {
        if (items.length === 0) {
            tableBody.innerHTML = `
                <tr>
                    <td colspan="6" style="text-align: center; color: #666;">No items yet. Add a row or run OCR.</td>
                </tr>
            `;
            return;
        }

        tableBody.innerHTML = items.map((item, index) => {
            return `
                <tr data-index="${index}">
                    <td class="editable-cell"><input class="row-ref" type="text" value="${escapeHtml(item.ref)}" placeholder="REF"></td>
                    <td class="editable-cell"><input class="row-description" type="text" value="${escapeHtml(item.description)}" placeholder="Description"></td>
                    <td class="editable-cell"><input class="row-lot" type="text" value="${escapeHtml(item.lot)}" placeholder="LOT"></td>
                    <td class="editable-cell"><input class="row-qty" type="number" min="1" step="1" value="${escapeHtml(String(item.qty || 1))}"></td>
                    <td class="confidence-cell">${item.confidence ? `${item.confidence}%` : '-'}</td>
                    <td><button class="btn btn-sm btn-secondary row-remove" type="button">Remove</button></td>
                </tr>
            `;
        }).join('');
    }

    function syncItemsFromTable() {
        const rows = tableBody.querySelectorAll('tr[data-index]');
        rows.forEach((row) => {
            const index = Number(row.dataset.index);
            if (Number.isNaN(index) || !items[index]) {
                return;
            }
            const ref = row.querySelector('.row-ref')?.value.trim() || '';
            const descriptionInput = row.querySelector('.row-description');
            const lot = row.querySelector('.row-lot')?.value.trim() || '';
            const qtyRaw = row.querySelector('.row-qty')?.value || '1';

            const qty = Math.max(1, parseInt(qtyRaw, 10) || 1);
            const suggested = refLookup[ref] || '';
            const description = (descriptionInput?.value || '').trim() || suggested;
            if (descriptionInput && !descriptionInput.value.trim() && suggested) {
                descriptionInput.value = suggested;
            }

            items[index].ref = ref;
            items[index].description = description;
            items[index].lot = lot;
            items[index].qty = qty;
        });
    }

    function extractRef(text) {
        const withLabel = text.match(/(?:^|\s)REF[^A-Z0-9]{0,8}([0-9]{5,6})(?:\s|$)/i);
        if (withLabel) {
            return withLabel[1];
        }
        const refs = text.match(/\b[0-9]{5,6}\b/g) || [];
        return refs[0] || '';
    }

    function extractLot(text) {
        const withLabel = text.match(/(?:^|\s)LOT[^A-Z0-9]{0,8}([A-Z0-9-]{6,})(?:\s|$)/i);
        if (withLabel) {
            return withLabel[1];
        }
        const candidates = text.match(/\b(?=[A-Z0-9-]{8,}\b)(?=.*[A-Z])(?=.*[0-9])[A-Z0-9-]+\b/g) || [];
        return candidates[0] || '';
    }

    function normalizeOcrText(text) {
        return text
            .replace(/\r/g, '\n')
            .replace(/[|]/g, 'I')
            .replace(/[^\S\n]+/g, ' ')
            .toUpperCase();
    }

    async function runOcr() {
        if (!window.Tesseract) {
            showStatus('Tesseract.js failed to load. Refresh and try again.', true);
            return;
        }
        if (selectedImages.length === 0) {
            showStatus('Add at least one image before running OCR.', true);
            return;
        }

        runOcrBtn.disabled = true;
        let addedCount = 0;

        for (let i = 0; i < selectedImages.length; i += 1) {
            const file = selectedImages[i];
            showStatus(`Processing ${i + 1}/${selectedImages.length}: ${file.name}`);

            try {
                const result = await window.Tesseract.recognize(file, 'eng');
                const cleanText = normalizeOcrText(result.data?.text || '');
                const ref = extractRef(cleanText);
                const lot = extractLot(cleanText);
                const confidence = result.data?.confidence ? Math.round(result.data.confidence) : '';

                if (ref || lot) {
                    createItemRow({
                        ref,
                        lot,
                        description: refLookup[ref] || '',
                        qty: 1,
                        confidence
                    });
                    addedCount += 1;
                }
            } catch (error) {
                console.error(error);
            }
        }

        runOcrBtn.disabled = false;
        showStatus(`OCR complete. ${addedCount} item(s) added from ${selectedImages.length} image(s).`);
    }

    function generateTemplate() {
        syncItemsFromTable();

        const accountName = document.getElementById('accountName')?.value.trim() || '';
        const sapId = document.getElementById('sapId')?.value.trim() || '';
        const repName = document.getElementById('repName')?.value.trim() || '';
        const dateText = new Date().toLocaleDateString();

        const filledItems = items.filter((item) => item.ref || item.description || item.lot);
        const lines = filledItems.map((item, idx) => {
            const ref = item.ref || '[REF]';
            const description = item.description || '[DESCRIPTION]';
            const lot = item.lot || '[LOT]';
            const qty = item.qty || 1;
            return `${idx + 1}) REF: ${ref} | ${description} | LOT: ${lot} | Qty: ${qty}`;
        });

        const template = [
            `Exchange Request, SAP ${sapId || '[SAP_ID]'}, ${accountName || '[ACCOUNT_NAME]'}, ${dateText}`,
            '',
            `Account: ${accountName || '[ACCOUNT_NAME]'}`,
            `SAP: ${sapId || '[SAP_ID]'}`,
            '',
            'Items to exchange:',
            lines.length ? lines.join('\n') : '1) REF: [REF] | [DESCRIPTION] | LOT: [LOT] | Qty: [QTY]',
            '',
            'Please provide a UPS return label.',
            '',
            'Thank you,',
            repName || '[REP_NAME]'
        ].join('\n');

        templateOutput.value = template;
    }

    async function copyTemplate() {
        const text = templateOutput.value.trim();
        if (!text) {
            showStatus('Generate a template first.', true);
            return;
        }
        try {
            await navigator.clipboard.writeText(text);
            showStatus('Template copied to clipboard.');
        } catch (_err) {
            templateOutput.focus();
            templateOutput.select();
            document.execCommand('copy');
            showStatus('Template copied to clipboard.');
        }
    }

    function downloadTemplate() {
        const text = templateOutput.value.trim();
        if (!text) {
            showStatus('Generate a template first.', true);
            return;
        }
        const sapId = document.getElementById('sapId')?.value.trim() || 'SAP';
        const datePart = new Date().toISOString().slice(0, 10);
        const safeSap = sapId.replace(/[^A-Za-z0-9_-]/g, '_');
        const filename = `Exchange_Template_${safeSap}_${datePart}.txt`;
        const blob = new Blob([text], { type: 'text/plain;charset=utf-8' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        link.remove();
        URL.revokeObjectURL(url);
        showStatus('Template downloaded.');
    }

    function clearImages() {
        selectedImages.splice(0, selectedImages.length);
        imageInput.value = '';
        renderUploadList();
        showStatus('Image queue cleared.');
    }

    function escapeHtml(value) {
        return String(value)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
    }

    dropZone.addEventListener('click', () => imageInput.click());
    imageInput.addEventListener('change', (event) => addImages(event.target.files || []));

    dropZone.addEventListener('dragover', (event) => {
        event.preventDefault();
        dropZone.classList.add('drag-active');
    });
    dropZone.addEventListener('dragleave', () => dropZone.classList.remove('drag-active'));
    dropZone.addEventListener('drop', (event) => {
        event.preventDefault();
        dropZone.classList.remove('drag-active');
        addImages(event.dataTransfer?.files || []);
    });

    runOcrBtn.addEventListener('click', runOcr);
    clearImagesBtn.addEventListener('click', clearImages);
    addRowBtn.addEventListener('click', () => createItemRow({ qty: 1 }));
    generateTemplateBtn.addEventListener('click', generateTemplate);
    copyTemplateBtn.addEventListener('click', copyTemplate);
    downloadTemplateBtn.addEventListener('click', downloadTemplate);

    tableBody.addEventListener('click', (event) => {
        const button = event.target.closest('.row-remove');
        if (!button) {
            return;
        }
        const row = button.closest('tr[data-index]');
        if (!row) {
            return;
        }
        const index = Number(row.dataset.index);
        if (Number.isNaN(index)) {
            return;
        }
        items.splice(index, 1);
        renderItems();
    });

    tableBody.addEventListener('input', (event) => {
        const row = event.target.closest('tr[data-index]');
        if (!row) {
            return;
        }
        syncItemsFromTable();
    });

    renderItems();
});
