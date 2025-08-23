# Dateiname: Startseite.py

import streamlit as st
from _api_functions import get_clan_data, get_current_war_data, get_cwl_group_info, get_capital_raid_data, get_api_data

# --- ZENTRALE DATEN ---
CLAN_TAG = "#2GJY8YPUP"
API_KEY = "DEIN_API_SCHLÜSSEL"
# --------------------

st.set_page_config(page_title="CoC Werkzeuge", page_icon="⚔️", layout="centered")
st.title("Willkommen auf unserer offiziellen CLanwebsite! 👋")

if st.button("Alle Live-Daten laden!", type="primary", use_container_width=True):
    st.session_state.clear()
    status = st.status("Lade alle Daten vom Server...", expanded=True)

    with status:
        st.session_state.clan_data = get_clan_data(CLAN_TAG, API_KEY)
        st.write("✅ Clan-Infos geladen.")
        
        st.session_state.war_data = get_current_war_data(CLAN_TAG, API_KEY)
        st.write("✅ Aktueller Krieg geladen.")
        
        st.session_state.raid_data = get_capital_raid_data(CLAN_TAG, API_KEY)
        st.write("✅ Clan-Hauptstadt-Daten geladen.")

        # --- NEUE CWL-LADELOGIK ---
        st.write("Lade CWL-Rohdaten für den Rechner...")
        group_data = get_cwl_group_info(CLAN_TAG, API_KEY)
        if group_data and not group_data.get("reason"):
            st.session_state.cwl_group_data = group_data # Speichern auch die Gruppen-Info
            cwl_wars_raw = []
            war_tags = [war['warTag'] for round_ in group_data.get('rounds', []) for war in round_ if war['warTag'] != '#0']
            for i, war_tag in enumerate(war_tags):
                war_url = f"https://api.clashofclans.com/v1/clanwarleagues/wars/{war_tag.replace('#', '%23')}"
                war_data = get_api_data(war_url, API_KEY)
                if war_data and not war_data.get("reason"):
                    cwl_wars_raw.append(war_data)
            st.session_state.cwl_wars_raw = cwl_wars_raw # Speichere die Liste der rohen Kriegsdaten
            st.write(f"✅ {len(cwl_wars_raw)} / 7 CWL-Kriegstage geladen.")
        else:
            st.session_state.cwl_wars_raw = []
            st.write("ℹ️ Keine aktive CWL gefunden.")

    status.update(label="Alle Daten erfolgreich geladen!", state="complete", expanded=False)

st.sidebar.success("Wähle ein Werkzeug aus.")
st.markdown("Drücke den Knopf oben, um die aktuellsten Daten zu laden. Wähle dann links eine Statistik aus!")
