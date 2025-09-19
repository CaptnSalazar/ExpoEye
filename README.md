# ExpoEye: AI-Powered Expo Companion 🎭✨

ExpoEye is your witty, scene-aware guide for navigating chaotic expos.  
Upload snapshots (badge, map, networking chaos, or tech glitches), and ExpoEye uses OCR + Scene Classification + Grok LLM to provide playful, context-aware suggestions.

---

## 🚀 Features
- 📸 Upload expo photos (badges, maps, error screens)
- 🔍 OCR text extraction via Tesseract
- 🧠 Scene classification (Networking, Navigation, Tech Glitch, Overwhelm)
- 🤖 Grok-powered witty suggestions (mock mode available)
- 🎨 Streamlit interactive interface

---

## 📂 Project Structure
```
ExpoEye/
├── README.md
├── app.py
├── requirements.txt
├── .gitignore
├── .streamlit/
│   └── config.toml
├── demo_images/
│   ├── badge_sample.jpg
│   ├── map_sample.jpg
│   └── error_screen_sample.jpg
├── setup_instructions.md
├── LICENSE
└── .env.example
```

---

## 🛠️ Setup Instructions
See [setup_instructions.md](./setup_instructions.md)

---

## 📸 Demo Usage
- Upload a photo of a badge → ExpoEye extracts text + suggests witty networking icebreaker
- Upload an expo map → ExpoEye helps with navigation humor
- Upload an error screen → ExpoEye provides “tech glitch survival tips”

---

## 🔑 Environment Variables
Create `.env` file from `.env.example` and configure:
```
GROK_API_KEY=your_api_key_here
```

If left as `demo`, ExpoEye runs in mock mode.

---

## 📜 License
MIT License (see LICENSE file)
