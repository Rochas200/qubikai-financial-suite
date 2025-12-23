import streamlit as st
import google.generativeai as genai
from shared_brain.jurist import get_jurist_system_prompt

st.set_page_config(page_title="SchuldNavigator", page_icon="🧭")

# API Setup
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("⚠️ Check je API Key")
    st.stop()

st.title("SchuldNavigator 🧭")
st.markdown("### Praat met de Qubikai Jurist (Gemini Edition)")

# Chat Geschiedenis initialiseren
if "messages" not in st.session_state:
    st.session_state.messages = []
    # We voegen de systeem prompt toe als eerste instructie (onzichtbaar voor gebruiker)
    # Let op: Gemini chat werkt net anders, we sturen de system prompt gewoon mee in de context
    st.session_state.system_prompt = get_jurist_system_prompt(niveau="uitleg")

# Toon oude berichten
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat Input
if prompt := st.chat_input("Vraag bijv: 'Wat is de beslagvrije voet?'"):
    
    # 1. Toon user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Bouw de chat context voor Google
    # We maken een tijdelijke lijst voor Gemini
    history_for_google = []
    
    # Eerst de systeem instructie
    history_for_google.append({
        "role": "user", 
        "parts": [st.session_state.system_prompt + "\n\nDe gebruiker vraagt: " + prompt]
    })
    
    # 3. Vraag antwoord
    with st.chat_message("assistant"):
        try:
            # We gebruiken hier generate_content voor een enkele vraag-antwoord, 
            # voor een lange chat kun je start_chat gebruiken, maar dit is robuuster voor Streamlit.
            response = model.generate_content(history_for_google[0]['parts'][0])
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Foutje: {e}")