# Exchange Template Generator — Feature Spec

**Created:** 2026-03-06  
**Status:** Approved for build  
**Delegate to:** Codex

## Overview
Add an exchange/return template generator to the proposal tool. Users upload implant box photos, system extracts REF + LOT via OCR, user adds account info, and generates a formatted exchange request.

## Requirements

### User Flow
1. User navigates to new "Exchange" page
2. User enters account info:
   - Account Name (text input)
   - SAP ID (text input)
3. User uploads 1+ implant box photos
4. System extracts REF + LOT via client-side OCR (Tesseract.js)
5. User reviews/edits extracted data in editable table
6. User can manually add rows for items OCR missed
7. User clicks "Generate Exchange Template"
8. System outputs formatted exchange request (copy to clipboard + download as .txt)

### Technical Approach

#### OCR
- Use **Tesseract.js** (client-side, zero API cost)
- Process images in browser
- Extract text, parse for patterns:
  - REF: typically 5-6 digit number
  - LOT: alphanumeric, often 8+ characters
- Show confidence indicator if possible

#### Manual Entry Fallback
- Editable table with columns: REF | Description | LOT | Qty
- "Add Row" button for manual entries
- Pre-populate description from REF lookup if we have product data

#### Template Output
Format (matches current exchange emails):
```
Exchange Request, SAP [SAP_ID], [ACCOUNT_NAME], [DATE]

Account: [ACCOUNT_NAME]
SAP: [SAP_ID]

Items to exchange:
1) REF: [REF] | [DESCRIPTION] | LOT: [LOT] | Qty: [QTY]
2) ...

Please provide a UPS return label.

Thank you,
[REP_NAME]
```

### UI/UX
- New nav item: "Exchange" (after Promos)
- Clean form layout similar to existing pages
- Drag-and-drop image upload zone
- Live preview of extracted items
- Copy button + Download button for final template

### Tech Stack
- Flask route: `/exchange`
- Template: `templates/exchange.html`
- JS: Include Tesseract.js from CDN
- No backend API calls for OCR

### Out of Scope (v1)
- Replacement item selection (user handles separately)
- Direct email sending
- Account lookup/autocomplete

## Success Criteria
- Users can generate exchange templates without API costs
- OCR works reasonably well on clear implant box photos
- Manual entry works as reliable fallback
- Template format matches current email structure

## Files to Create/Modify
- `templates/exchange.html` (new)
- `templates/base.html` (add nav link)
- `static/js/exchange.js` (new - OCR + form logic)
- `app.py` (add /exchange route)
