import streamlit as st
import requests
from _api_functions import get_clan_data, get_current_war_data, get_cwl_group_info, get_capital_raid_data, get_api_data

# --- ZENTRALE DATEN ---
CLAN_TAG = "#2GJY8YPUP"
API_KEY = st.secrets["API_KEY"]
# --------------------

st.set_page_config(page_title="CoC Werkzeuge", page_icon="⚔️", layout="centered")
st.title("Willkommen bei den CoC Werkzeugen! 👋")

# +++ IP-ADRESSEN-FINDER +++
st.subheader("IP-Adressen-Finder 🕵️")
st.warning("Nur benutzen, wenn die App einen IP-Fehler anzeigt!")
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
# +++ ENDE IP-FINDER +++


# --- ZENTRALER LADE-KNOPF ---
if st.button("Alle Live-Daten laden!", type="primary", use_container_width=True):
    st.session_state.clear()
    status = st.status("Lade alle Daten vom Server...", expanded=True)

    with status:
        st.session_state.clan_data = get_clan_data(CLAN_TAG, API_KEY)
        st.write("✅ Clan-Infos geladen.")
        
        st.session_state.war_data = get_current_war_data(CLAN_TAG, API_KEY)
        st.write("✅ Aktueller Krieg geladen.")
        
        st.session_state.raid_data = get_capital_raid_data(CLAN_TAG, API_KEY, limit=10)
        st.write("✅ Clan-Hauptstadt-Daten geladen.")

        st.write("Lade CWL-Daten (kann einen Moment dauern)...")
        group_data = get_cwl_group_info(CLAN_TAG, API_KEY)
        if group_data and not group_data.get("reason"):
            st.session_state.cwl_group_data = group_data
            cwl_wars_raw = []
            war_tags = [war['warTag'] for round_ in group_data.get('rounds', []) for war in round_ if war['warTag'] != '#0']
            for i, war_tag in enumerate(war_tags):
                war_url = f"https://api.clashofclans.com/v1/clanwarleagues/wars/{war_tag.replace('#', '%23')}"
                war_data = get_api_data(war_url, API_KEY)
                if war_data and not war_data.get("reason"):
                    cwl_wars_raw.append(war_data)
            st.session_state.cwl_wars_raw = cwl_wars_raw
            st.write(f"✅ {len(cwl_wars_raw)} / 7 CWL-Kriegstage geladen.")
        else:
            st.session_state.cwl_wars_raw = []
            st.write("ℹ️ Keine aktive CWL gefunden.")

    status.update(label="Alle Daten erfolgreich geladen!", state="complete", expanded=False)

st.sidebar.success("Wähle ein Werkzeug aus.")
st.markdown(
    """
    Diese Web-Anwendung befindet sich im Aufbau.
    **Drücke den Knopf oben, um die aktuellsten Daten zu laden.**
    
    **👈 Wähle dann links in der Seitenleiste eine Statistik aus!**
    """
)
