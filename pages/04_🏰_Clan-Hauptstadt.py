import streamlit as st
import pandas as pd

st.set_page_config(page_title="Clan-Hauptstadt", layout="wide")
st.title("🏰 Clan-Hauptstadt & Raid-Wochenende")

if 'raid_data' not in st.session_state or not st.session_state.raid_data:
    st.warning("Bitte lade zuerst die Daten auf der Startseite.")
    st.page_link("Startseite.py", label="Zurück zur Startseite", icon="🏠")
else:
    raid_data = st.session_state.raid_data

    if raid_data.get("error"):
        st.error(f"Fehler beim Laden der Raid-Daten: {raid_data.get('message')}")
    elif not raid_data.get('items'):
        st.info("Für diesen Clan wurden keine Raid-Daten gefunden.")
    else:
        raid_history = raid_data['items']

        st.subheader("🔍 Detail-Analyse eines Wochenendes")
        
        # Erstelle eine Liste von Daten für das Dropdown-Menü
        date_options = [pd.to_datetime(raid.get('startTime')).strftime('%d.%m.%Y') for raid in raid_history]
        selected_date_str = st.selectbox("Wähle ein Wochenende aus der Historie aus:", options=date_options)

        # Finde den ausgewählten Raid in der Liste
        selected_raid = next((raid for raid in raid_history if pd.to_datetime(raid.get('startTime')).strftime('%d.%m.%Y') == selected_date_str), None)

        if selected_raid:
            # --- RAID-ÜBERSICHT FÜR DAS AUSGEWÄHLTE WOCHENENDE ---
            # Diese Daten sind immer verfügbar
            start_time = pd.to_datetime(selected_raid.get('startTime')).strftime('%d.%m.%Y')
            end_time = pd.to_datetime(selected_raid.get('endTime')).strftime('%d.%m.%Y')
            st.info(f"Angezeigtes Wochenende: {start_time} - {end_time}")
            
            # Die Gesamtbeute muss jetzt auch hier berechnet werden, falls Mitgliederdaten da sind
            total_loot = sum(member.get('capitalResourcesLooted', 0) for member in selected_raid.get('members', []))

            col1, col2, col3 = st.columns(3)
            col1.metric("Gesamt-Beute 💰", f"{total_loot:,}".replace(',', '.'))
            col2.metric("Genutzte Angriffe ⚔️", selected_raid.get('totalAttacks', 0))
            col3.metric("Teilnehmer 👥", len(selected_raid.get('members', [])) if 'members' in selected_raid else "N/A")
            st.divider()

            # --- KARTENANZEIGE NUR, WENN MITGLIEDERDATEN VORHANDEN SIND ---
            st.subheader("Leistung der Mitglieder")
            
            members = selected_raid.get('members', [])
            
            if not members:
                st.warning("Detaillierte Mitglieder-Statistiken sind laut API nur für das jeweils letzte Raid-Wochenende verfügbar.")
            else:
                # Der Code für Sortierung und Kartenanzeige wird nur hier ausgeführt
                sort_option = st.selectbox(
                    "Sortiere Mitglieder nach:",
                    ("Beute (Meiste zuerst)", "Angriffe (Meiste zuerst)", "Effizienz (Beute pro Angriff)")
                )
                
                for m in members:
                    attacks = m.get('attacks', 0)
                    loot = m.get('capitalResourcesLooted', 0)
                    m['efficiency'] = loot / attacks if attacks > 0 else 0

                if sort_option == "Beute (Meiste zuerst)":
                    sorted_members = sorted(members, key=lambda m: m.get('capitalResourcesLooted', 0), reverse=True)
                elif sort_option == "Angriffe (Meiste zuerst)":
                    sorted_members = sorted(members, key=lambda m: m.get('attacks', 0), reverse=True)
                else: # Effizienz
                    sorted_members = sorted(members, key=lambda m: m.get('efficiency', 0), reverse=True)

                for member in sorted_members:
                    if 'name' not in member: continue
                    with st.container(border=True):
                        col1, col2, col3, col4 = st.columns(4)
                        col1.markdown(f"**{member['name']}**")
                        col2.metric("Erbeutetes Kapitalgold 💰", f"{member.get('capitalResourcesLooted', 0):,}".replace(',', '.'))
                        col3.metric("Genutzte Angriffe ⚔️", f"{member.get('attacks', 0)} / {selected_raid.get('capitalTotalAttacks', 6)}")
                        col4.metric("Beute pro Angriff 🎯", f"{member.get('efficiency', 0):,.0f}".replace(',', '.'))