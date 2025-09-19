import streamlit as st
import requests, os, io
from PIL import Image
st.set_page_config(page_title='ExpoEye+ Demo (Groq Integrated)', layout='wide')
st.title("ExpoEye+ — Multi-Agent Demo (Groq Integrated)")

st.write("""Upload an image (badge/map/error) and optional note. Demo will call the local orchestrator which integrates Vision, Context agents and Groq LLM (mock if no key).""")

uploaded = st.file_uploader("Upload Image", type=["png","jpg","jpeg"])
note = st.text_input("Optional note (context for Groq)")

if st.button("Analyze"):
    if not uploaded:
        st.warning("Please upload an image first.")
    else:
        files = {"image": (uploaded.name, uploaded.getvalue(), uploaded.type)}
        orch_url = os.getenv('ORCH_URL','http://localhost:8200/submit')
        with st.spinner("Sending to orchestrator..."):
            try:
                resp = requests.post(orch_url, files=files, data={"note": note}, timeout=30)
                data = resp.json()
                if resp.status_code != 200:
                    st.error(f"Orchestrator error: {data}")
                else:
                    st.subheader("MCP Trace (Vision + Context)")
                    st.json(data.get('mcp_trace', {}))
                    st.subheader("Final Advice (from Groq)")
                    st.write(data.get('advice', 'No advice returned'))
            except Exception as e:
                st.error(f"Request failed: {e}")
