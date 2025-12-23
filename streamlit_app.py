import streamlit as st

# 1. CONFIGURATIE (Geldt voor het hele platform)
st.set_page_config(
    page_title="Qubikai Financial Suite",
    page_icon="🛡️",
    layout="wide"
)

# 2. STYLING (Corporate Identity)
st.markdown("""
<style>
    /* Algemene stijl voor donkere modus */
    .stApp {background-color: #0E1117; color: white;}
    
    /* De kaarten op het dashboard */
    .nav-card {
        background-color: #1F2937;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #FF4B4B;
        text-align: center;
        transition: transform 0.2s;
        margin-bottom: 20px;
        cursor: pointer;
    }
    .nav-card:hover {
        transform: scale(1.02);
        background-color: #2D3748;
    }
    h3 { margin-bottom: 10px; }
</style>
""", unsafe_allow_html=True)

# 3. HET DASHBOARD
st.title("Welkom in de Qubikai Hub 🛡️")
st.write("Jouw centrale plek voor financiële rust en overzicht.")

st.markdown("---")

# Navigatie Kolommen
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="nav-card">', unsafe_allow_html=True)
    st.markdown("### 📮 Snap-mijn-Brief")
    st.write("Post ontvangen? Ik analyseer het en schrijf een bezwaar.")
    if st.button("Open Brieven App"):
        st.switch_page("pages/1_📮_Snap_mijn_Brief.py")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="nav-card" style="border-left-color: #00C853;">', unsafe_allow_html=True)
    st.markdown("### 💰 SmartBudget")
    st.write("Krijg grip op je uitgaven en bonnetjes.")
    if st.button("Open Budget App"):
        st.switch_page("pages/2_💰_SmartBudget.py")
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="nav-card" style="border-left-color: #0078D7;">', unsafe_allow_html=True)
    st.markdown("### 🧭 SchuldNavigator")
    st.write("De routekaart naar een schuldenvrij leven.")
    if st.button("Open Navigator"):
        st.switch_page("pages/3_🧭_SchuldNavigator.py")
    st.markdown('</div>', unsafe_allow_html=True)