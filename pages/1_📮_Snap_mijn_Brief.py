import streamlit as st
import google.generativeai as genai
from PIL import Image
import time
from shared_brain.jurist import get_jurist_system_prompt

st.set_page_config(page_title="Snap-mijn-Brief", page_icon="📮")

# API Setup (Google Versie) 🔵
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # We gebruiken Flash: Snel, slim & goedkoop
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"⚠️ API Error: {e}")
    st.stop()

# --- INTELLIGENTIE ---
def agent_analyze(image):
    # Google snapt direct PIL Images, we hoeven niet moeilijk te doen met base64!
    prompt = """
    Jij bent de Dossier Analist.
    Haal deze feiten uit de foto: Instantie, Datum, Kenmerk, Bedrag, Feit.
    Geef output als Markdown Tabel.
    """
    try:
        # Hier sturen we de foto + tekst direct naar Gemini
        response = model.generate_content([prompt, image])
        return response.text
    except Exception as e:
        return f"Fout: {e}"

def agent_write_letter(analysis):
    system_prompt = get_jurist_system_prompt(niveau="formeel")
    
    user_prompt = f"""
    Schrijf een Pro-Forma bezwaarschrift op basis van deze feiten:
    {analysis}
    
    GEBRUIK DEZE PERSONA INSTRUCTIES:
    {system_prompt}
    
    Gebruik placeholders [NAAM], [ADRES].
    """
    
    response = model.generate_content(user_prompt)
    return response.text

# --- UI (Blijft hetzelfde) ---
st.title("Snap-mijn-Brief 📮")
st.markdown("### 📸 Post Scannen & Bezwaar Maken (Powered by Gemini)")

if 'step' not in st.session_state: st.session_state.step = 'upload'
if 'analysis' not in st.session_state: st.session_state.analysis = ""

# 1. UPLOAD
uploaded_file = st.file_uploader("Upload je brief", type=['png', 'jpg', 'jpeg'])
if uploaded_file:
    image = Image.open(uploaded_file)
    # We tonen de foto even klein
    st.image(image, caption="Jouw brief", width=200)
    
    if st.button("🔍 Analyseer Brief"):
        with st.spinner("Gemini leest mee..."):
            res = agent_analyze(image)
            st.session_state.analysis = res
            st.session_state.step = 'result'
            st.rerun()

# 2. RESULTAAT
if st.session_state.analysis:
    st.markdown("---")
    st.markdown(st.session_state.analysis)
    
    if st.button("✍️ Laat Jurist Bezwaar Schrijven"):
        with st.spinner("Jurist schrijft brief..."):
            brief = agent_write_letter(st.session_state.analysis)
            st.markdown("### 📄 Concept Brief")
            st.code(brief, language="markdown")
            st.success("Klaar!")