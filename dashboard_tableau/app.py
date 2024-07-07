import warnings
warnings.filterwarnings("ignore")

import streamlit as st
import streamlit.components.v1 as components
st.set_page_config(layout="wide",page_title="Tableau Dashboard",initial_sidebar_state="collapsed")

# Make sure container is centered
st.markdown("""
<style>
    [data-testid="stDecoration"] {display: none;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

</style>""",
unsafe_allow_html=True)

with open('tableau_embed.html', 'r') as f:
    tableau_html = f.read()

components.html(tableau_html, height=1140, scrolling=False)
