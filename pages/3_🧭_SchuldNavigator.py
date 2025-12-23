import streamlit as st
from openai import OpenAI
# HIER IS HET BEWIJS: We lenen de jurist van de buren! 🧠
from shared_brain.jurist import get_jurist_system_prompt

st.set_page_config(page_title="SchuldNavigator", page_icon="🧭")

# API Setup (Ook hier hebben we de sleutel nodig)
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except:
    st.error("⚠️ API Key error")
    st.stop()

st.title("SchuldNavigator 🧭")
st.markdown("### Praat met de Qubikai Jurist")
st.write("Stel een vraag over schulden, boetes of beslaglegging. Ik geef rustig en juridisch correct antwoord.")

# Chat geheugen
if "messages" not in st.session_state:
    st.session_state.messages = []

# Toon eerdere berichten
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat Input
if prompt := st.chat_input("Vraag bijv: 'Mag de deurwaarder mijn TV meenemen?'"):
    # 1. Toon gebruikersbericht
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Haal de slimme 'Shared Brain' prompt op (Niveau: Uitleg)
    # Dit is DEZELFDE expert als in de Brief-app, maar nu in 'chat-modus'.
    system_instruction = get_jurist_system_prompt(niveau="uitleg")

    # 3. Genereer antwoord
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_instruction},
                *st.session_state.messages # Stuur chatgeschiedenis mee
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    
    st.session_state.messages.append({"role": "assistant", "content": response})