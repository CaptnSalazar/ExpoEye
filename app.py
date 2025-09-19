import streamlit as st
import pytesseract
from PIL import Image

# Agents and Orchestrator Simulation (Streamlit demo front-end)
class VisionAgent:
    def process_image(self, image):
        text = pytesseract.image_to_string(image)
        return text.strip()

class ContextAgent:
    def enrich_context(self, text):
        # Simulate MCP integration by calling external API (mock)
        if "schedule" in text.lower():
            return "Found reference to event schedule. Fetching from MCP tool... (mock)"
        return "Context enriched with MCP tool (mock)."

class VoiceAgent:
    def process_voice(self, audio_bytes):
        # Mock voice transcription
        return "This is a mock transcription of your voice input."

class OrchestratorLocal:
    def __init__(self):
        self.vision = VisionAgent()
        self.context = ContextAgent()
        self.voice = VoiceAgent()

    def handle_request(self, image=None, audio=None):
        results = {}
        if image:
            vision_output = self.vision.process_image(image)
            results["ocr_text"] = vision_output
            results["context"] = self.context.enrich_context(vision_output)
        if audio:
            voice_text = self.voice.process_voice(audio)
            results["voice_text"] = voice_text
        return results

st.set_page_config(page_title='ExpoEye+ Multi-Agent Demo', layout='wide')
st.title("ExpoEye+ : Multi-Agent Expo Assistant (Demo UI)")

st.write("Upload an image (badge, map, booth) and/or a voice note to get insights. This demo runs a local orchestrator in-process (mock agents). For full multi-service deployment, run the docker-compose stack and use the orchestrator service.")

uploaded_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])
uploaded_audio = st.file_uploader("Upload Audio", type=["wav", "mp3", "m4a"])

orch = OrchestratorLocal()
results = None

if uploaded_file is not None or uploaded_audio is not None:
    image = None
    audio = None
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image', use_column_width=False)
    if uploaded_audio:
        audio = uploaded_audio.read()
    results = orch.handle_request(image=image, audio=audio)

if results:
    st.subheader("Results")
    if "ocr_text" in results:
        st.markdown("**Extracted Text (OCR):**")
        st.code(results["ocr_text"])
    if "context" in results:
        st.markdown("**Context Agent Response:**")
        st.write(results["context"])
    if "voice_text" in results:
        st.markdown("**Voice Agent Transcription:**")
        st.write(results["voice_text"])
