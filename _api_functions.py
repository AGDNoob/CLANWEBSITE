# Dateiname: _api_functions.py

import streamlit as st
import requests

# Die URL deines neuen Vercel-Proxys
PROXY_URL = "https://clanwebsite-2.vercel.app/" # <-- HIER DEINE URL EINTRAGEN

# Wir brauchen nur noch eine Funktion, die den Proxy anspricht
@st.cache_data(ttl=600)
def get_data_from_proxy(path, key_placeholder='unused'): # key wird nicht mehr gebraucht
    """Fragt Daten über den sicheren Vercel-Proxy ab."""
    full_url = f"{PROXY_URL}/api/proxy?path={path}"
    try:
        response = requests.get(full_url, timeout=15) # Etwas längerer Timeout
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": True, "message": str(e)}

# Alle alten Funktionen rufen jetzt nur noch die neue Proxy-Funktion auf
def get_clan_data(tag, key):
    return get_data_from_proxy(f"/clans/{tag}")

def get_current_war_data(tag, key):
    return get_data_from_proxy(f"/clans/{tag}/currentwar")

def get_cwl_group_info(tag, key):
    return get_data_from_proxy(f"/clans/{tag}/currentwar/leaguegroup")

def get_capital_raid_data(tag, key, limit=10):
    return get_data_from_proxy(f"/clans/{tag}/capitalraidseasons?limit={limit}")
