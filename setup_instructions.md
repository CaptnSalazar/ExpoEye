# ExpoEye Judge Setup Guide

## ✅ Requirements
- Python 3.8+
- pip
- Tesseract OCR installed on system
- Grok API key (optional, fallback mock mode available)

## ⚡ Setup
```bash
# Clone repo
git clone https://github.com/yourusername/ExpoEye.git
cd ExpoEye

# Create environment
python -m venv expoeye-env
source expoeye-env/bin/activate   # Windows: expoeye-env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Tesseract OCR (system)
# macOS: brew install tesseract
# Ubuntu: sudo apt-get install tesseract-ocr
# Windows: Download installer from: https://github.com/UB-Mannheim/tesseract/wiki

# Run app
streamlit run app.py
```

## 🚀 Usage
1. Upload a sample image from `demo_images/`
2. Select issue type (Networking, Navigation, Tech Glitch, Overwhelm)
3. ExpoEye will analyze with OCR + Scene Detection
4. Grok API (or fallback) generates witty solution

## 🔑 Environment
Create `.env` file from `.env.example` and add your Grok API key:
```
GROK_API_KEY=your_api_key_here
```
