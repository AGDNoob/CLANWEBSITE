## Dateiname: _api_functions.py

import streamlit as st
import requests

# Die @st.cache_data Zeile ist das einzige, was wir hier hinzufügen
@st.cache_data(ttl=600)
def get_api_data(url, key):
    """Eine generische Funktion, um Daten von einer beliebigen CoC API URL abzufragen."""
    headers = {"Authorization": f"Bearer {key}"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": True, "message": str(e)}

def get_clan_data(tag, key):
    """Fragt die allgemeinen Clan-Daten ab."""
    url = f"https://api.clashofclans.com/v1/clans/{tag.replace('#', '%23')}"
    return get_api_data(url, key)

def get_current_war_data(tag, key):
    """Fragt die Daten des aktuellen Clan-Kriegs ab."""
    url = f"https://api.clashofclans.com/v1/clans/{tag.replace('#', '%23')}/currentwar"
    return get_api_data(url, key)

def get_cwl_group_info(tag, key):
    """Fragt die Informationen der aktuellen CWL-Gruppe ab."""
    url = f"https://api.clashofclans.com/v1/clans/{tag.replace('#', '%23')}/currentwar/leaguegroup"
    return get_api_data(url, key)

# Wir passen diese Funktion an, um eine variable Anzahl an Raids zu holen
def get_capital_raid_data(tag, key, limit=1):
    """Fragt die Daten der letzten Raid-Wochenenden ab."""
    url = f"https://api.clashofclans.com/v1/clans/{tag.replace('#', '%23')}/capitalraidseasons?limit={limit}"
    return get_api_data(url, key)
