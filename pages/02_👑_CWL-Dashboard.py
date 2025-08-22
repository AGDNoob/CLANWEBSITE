import streamlit as st

st.set_page_config(page_title="CWL-Dashboard", layout="wide")
st.title("👑 CWL-Dashboard")

# Prüft, ob die CWL-Daten im Langzeitgedächtnis vorhanden sind.
if 'cwl_summary' not in st.session_state or not st.session_state.cwl_summary:
    st.warning("Bitte lade zuerst die Daten auf der Startseite.")
    st.info("Hinweis: Es werden nur Daten angezeigt, wenn eine CWL aktiv ist.")
    st.page_link("Startseite.py", label="Zurück zur Startseite", icon="🏠")
else:
    # Holt die verarbeiteten Daten aus dem Gedächtnis
    summary_data = st.session_state.cwl_summary
    
    st.success("CWL-Daten erfolgreich geladen! Die Liste kann jetzt sortiert werden.")
    st.subheader("CWL Gesamt-Statistik")

    # --- SORTIER-FUNKTION & KARTENANZEIGE ---
    sort_option = st.selectbox(
        "Sortiere Spieler nach:",
        ("Sterne (Meiste zuerst)", "Angriffe genutzt (Meiste zuerst)", "Sterne pro Angriff")
    )

    # Fügt temporäre Werte für die Sortierung hinzu
    for player in summary_data:
        # Stellt sicher, dass die Schlüssel für jeden Spieler existieren
        player['stars'] = player.get('stars', 0)
        player['attacks'] = player.get('attacks', 0)
        player['stars_per_attack'] = player['stars'] / player['attacks'] if player['attacks'] > 0 else 0

    # Sortier-Logik
    if sort_option == "Sterne (Meiste zuerst)":
        sorted_summary = sorted(summary_data, key=lambda p: p['stars'], reverse=True)
    elif sort_option == "Angriffe genutzt (Meiste zuerst)":
        sorted_summary = sorted(summary_data, key=lambda p: p['attacks'], reverse=True)
    elif sort_option == "Sterne pro Angriff":
        sorted_summary = sorted(summary_data, key=lambda p: p['stars_per_attack'], reverse=True)

    # Karten-Anzeige
    for player in sorted_summary:
        with st.container(border=True):
            col1, col2, col3, col4 = st.columns(4)
            
            col1.markdown(f"**{player.get('name', 'Unbekannt')}**")
            col2.metric("Gesamte Sterne ⭐", player['stars'])
            col3.metric("Genutzte Angriffe ⚔️", f"{player['attacks']} / 7")
            # Zeigt Sterne pro Angriff mit 2 Nachkommastellen an
            col4.metric("Sterne pro Angriff 🎯", f"{player['stars_per_attack']:.2f}")