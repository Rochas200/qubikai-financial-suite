import streamlit as st
# Ook deze kan straks bij het shared brain!
from shared_brain.jurist import get_jurist_system_prompt 

st.set_page_config(page_title="SchuldNavigator", page_icon="🧭")

st.title("SchuldNavigator 🧭")
st.write("Soms zie je door de bomen het bos niet meer. Wij helpen je.")

# Test of het brein werkt
prompt = get_jurist_system_prompt(niveau="uitleg")
st.caption(f"Brein Status: Gekoppeld ✅")

st.info("🚧 Module in ontwikkeling.")