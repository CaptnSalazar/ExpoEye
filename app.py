import streamlit as st
import pytesseract
from PIL import Image
import numpy as np
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Mock Grok API call
def call_grok_api(prompt, image=None):
    api_key = os.getenv("GROK_API_KEY", "demo")
    if api_key == "demo":
        return f"[MOCK RESPONSE] ExpoEye suggests: {prompt}"
    # Example of real API (placeholder, replace with actual Grok endpoint)
    try:
        response = requests.post(
            "https://api.grok.ai/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}"},
            json={"messages": [{"role": "user", "content": prompt}]},
            timeout=30
        )
        if response.status_code == 200:
            return response.json().get("choices", [{}])[0].get("message", {}).get("content", "[Empty response]")
        return f"[ERROR] Grok API returned {response.status_code}: {response.text}"
    except Exception as e:
        return f"[ERROR] Grok API call failed: {str(e)}"

# Simple scene classification (mocked based on brightness)
def classify_scene(image: Image.Image) -> str:
    arr = np.array(image.convert("L"))  # grayscale
    mean_val = arr.mean()
    if mean_val < 85:
        return "Networking Chaos"
    elif mean_val < 170:
        return "Navigation Puzzle"
    else:
        return "Tech Glitch or Overwhelm"

def extract_text(image: Image.Image) -> str:
    try:
        return pytesseract.image_to_string(image)
    except Exception as e:
        return f"[OCR ERROR] {str(e)}"

def main():
    st.title("ExpoEye 🎭✨ - Your Expo Companion")
    st.write("Upload expo snapshots (badge, map, glitch, etc.) and let ExpoEye analyze.")

    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        # OCR
        text = extract_text(image)
        st.subheader("Extracted Text")
        st.code(text if text.strip() else "[No text detected]")

        # Scene classification
        scene = classify_scene(image)
        st.subheader("Scene Classification")
        st.success(scene)

        # Suggestion via Grok/mock
        prompt = f"Scene: {scene}\nExtracted Text: {text}"
        response = call_grok_api(prompt)
        st.subheader("ExpoEye Suggestion")
        st.info(response)

if __name__ == "__main__":
    main()
