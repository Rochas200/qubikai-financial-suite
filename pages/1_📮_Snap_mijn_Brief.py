import streamlit as st
from openai import OpenAI
from PIL import Image
import base64
import io
import time
# HIER IS DE KOPPELING MET JE SHARED BRAIN! 🧠
from shared_brain.jurist import get_jurist_system_prompt

st.set_page_config(page_title="Snap-mijn-Brief", page_icon="📮")

# Configuratie
APP_NAME = "Snap-mijn-Brief"
ACCENT_COLOR = "#FF4B4B"

# API Setup
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except:
    st.error("⚠️ Geen API Key gevonden! Check secrets.toml")
    st.stop()

# --- INTELLIGENTIE ---
def agent_analyze(base64_img):
    # De Analist blijft even lokaal voor de foto-analyse
    prompt = """
    Jij bent de Dossier Analist.
    Haal deze feiten uit de foto: Instantie, Datum, Kenmerk, Bedrag, Feit.
    Geef output als Markdown Tabel.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": [
                    {"type": "text", "text": prompt}, 
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_img}"}}
                ]}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Fout: {e}"

def agent_write_letter(analysis):
    # HIER HALEN WE DE JURIST UIT DE GEDEELDE MAP!
    system_prompt = get_jurist_system_prompt(niveau="formeel")
    
    user_prompt = f"""
    Schrijf een Pro-Forma bezwaarschrift op basis van deze feiten:
    {analysis}
    Gebruik placeholders [NAAM], [ADRES].
    """
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    return response.choices[0].message.content

# --- UI ---
st.title(f"{APP_NAME}")
st.markdown("### 📸 Post Scannen & Bezwaar Maken")

if 'step' not in st.session_state: st.session_state.step = 'upload'
if 'analysis' not in st.session_state: st.session_state.analysis = ""

# 1. UPLOAD
uploaded_file = st.file_uploader("Upload je brief", type=['png', 'jpg', 'jpeg'])
if uploaded_file:
    # Verwerk afbeelding
    img = Image.open(uploaded_file)
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    b64_img = base64.b64encode(buf.getvalue()).decode('utf-8')
    
    if st.button("🔍 Analyseer Brief"):
        with st.spinner("Analist leest mee..."):
            res = agent_analyze(b64_img)
            st.session_state.analysis = res
            st.session_state.step = 'result'
            st.rerun()

# 2. RESULTAAT & ACTIE
if st.session_state.analysis:
    st.markdown("---")
    st.markdown(st.session_state.analysis)
    
    if st.button("✍️ Laat Jurist Bezwaar Schrijven"):
        with st.spinner("Jurist schrijft brief..."):
            brief = agent_write_letter(st.session_state.analysis)
            st.markdown("### 📄 Concept Brief")
            st.code(brief, language="markdown")
            st.success("Kopieer de tekst hierboven!")