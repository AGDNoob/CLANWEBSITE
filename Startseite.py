# Dateiname: Startseite.py

import streamlit as st
import requests # Füge diesen Import hinzu
from _api_functions import get_clan_data, get_current_war_data, get_cwl_group_info, get_capital_raid_data, get_api_data

# --- DEINE DATEN (bleibt unverändert) ---
CLAN_TAG = "#2GJY8YPUP"
API_KEY = st.secrets["API_KEY"] 
# --------------------

st.set_page_config(page_title="CoC Werkzeuge", page_icon="⚔️", layout="centered")
st.title("Willkommen auf unserer offiziellen Clanwebsite! 👋")

# +++ NEUER CODE-BLOCK START +++
st.subheader("IP-Adressen-Finder 🕵️")
if st.button("Verrate mir deine Server-IP!"):
    with st.spinner("Frage IP-Adresse ab..."):
        try:
            response = requests.get("https://api.ipify.org")
            if response.status_code == 200:
                ip = response.text
                st.success(f"Die IP-Adresse deines Servers ist:")
                st.code(ip)
                st.info("Kopiere diese IP und füge sie im CoC Developer Portal zu deinem API-Key hinzu.")
            else:
                st.error("Konnte die IP-Adresse nicht abfragen. Versuche es erneut.")
        except Exception as e:
            st.error(f"Ein Fehler ist aufgetreten: {e}")
st.divider()
# +++ NEUER CODE-BLOCK ENDE +++


# Der Rest der Datei bleibt unverändert...
if st.button("Alle Live-Daten laden!", type="primary", use_container_width=True):
    # ... (deine bisherige Lade-Logik)
