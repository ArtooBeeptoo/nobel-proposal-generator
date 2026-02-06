# Nobel Biocare Proposal Generator

A simple web app for generating custom Nobel Biocare sales proposals with discounts.

## Features

- 🔐 Password-protected access
- 📝 Search and select from Nobel Biocare product catalog
- 💰 Apply custom discount percentages
- 📄 Generate editable Word documents (.docx)
- 📕 Generate PDFs for sharing

## Deploy to Render

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/ArtooBeeptoo/nobel-proposal-generator)

After deploying, set your password in the Environment Variables:
- `APP_PASSWORD` - The password users will enter to access the app

## Local Development

```bash
pip install -r requirements.txt
export APP_PASSWORD=your-password
python app.py
```

Visit http://localhost:5000

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `APP_PASSWORD` | Login password | `nobel2026` |
| `SECRET_KEY` | Flask session key | Auto-generated |

## Products

The product catalog includes:
- NobelActive TiUltra Implants
- NobelActive Implants  
- Nobel Biocare N1 Implants
- NobelParallel CC TiUltra Implants
- NobelReplace CC TiUltra Implants
- NobelPearl Ceramic Implants
- NobelZygoma Implants
- Esthetic Abutments
- Multi-Unit Abutments
- Locator Abutments
- GoldAdapt Abutments
# v1.1 - Fri  6 Feb 10:37:11 CST 2026
# Redeploy trigger Fri  6 Feb 10:50:21 CST 2026
