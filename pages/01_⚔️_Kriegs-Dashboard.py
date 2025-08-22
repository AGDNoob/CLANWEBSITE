import streamlit as st

st.set_page_config(page_title="Kriegs-Dashboard", layout="wide")
st.title("Live Kriegs-Dashboard ⚔️")

# Prüft, ob die Kriegsdaten im Langzeitgedächtnis vorhanden sind.
if 'war_data' not in st.session_state or not st.session_state.war_data:
    st.warning("Bitte lade zuerst die Daten auf der Startseite.")
    st.page_link("Startseite.py", label="Zurück zur Startseite", icon="🏠")
else:
    # Holt die Daten aus dem Gedächtnis
    war_data = st.session_state.war_data

    # Prüft den Status des Krieges (z.B. "notInWar")
    if war_data.get("state") == "notInWar":
        st.info("Euer Clan befindet sich aktuell in keinem Krieg.")
    elif war_data.get("reason"):
        st.error(f"Fehler beim Laden der Kriegsdaten: {war_data.get('reason')}")
    else:
        # Wenn alles gut ist, wird die Seite normal angezeigt
        clan = war_data.get('clan', {})
        opponent = war_data.get('opponent', {})

        # --- KRIEGS-ÜBERSICHT ---
        st.subheader(f"{clan.get('name', 'Dein Clan')} vs. {opponent.get('name', 'Gegner')}")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Sterne ⭐", f"{clan.get('stars', 0)} - {opponent.get('stars', 0)}")
        col2.metric("Zerstörung %", f"{clan.get('destructionPercentage', 0):.2f}% - {opponent.get('destructionPercentage', 0):.2f}%")
        col3.metric("Angriffe ⚔️", f"{clan.get('attacks', 0)} / {len(clan.get('members', []))*2}")
        col4.metric("Status", war_data.get('state').replace('inWar', 'Läuft').replace('preparation', 'Vorbereitung'))
        st.divider()

        # --- SORTIER-FUNKTION & KARTENANZEIGE ---
        st.subheader("Spieler-Leistung")

        sort_option = st.selectbox(
            "Sortiere Spieler nach:",
            ("Karten-Position (Standard)", "Bester Angriff (Sterne)", "Durchschnittliche Zerstörung", "Rathaus-Level (Höchstes zuerst)")
        )

        members = war_data.get('clan', {}).get('members', [])

        # Fügt temporäre Werte für die Sortierung hinzu
        for member in members:
            if 'attacks' in member and member['attacks']:
                member['bestAttackStars'] = max(a['stars'] for a in member['attacks'])
                member['avgDestruction'] = sum(a['destructionPercentage'] for a in member['attacks']) / len(member['attacks'])
            else:
                member['bestAttackStars'] = -1
                member['avgDestruction'] = 0.0
        
        # Sortier-Logik
        if sort_option == "Karten-Position (Standard)":
            sorted_members = sorted(members, key=lambda m: m.get('mapPosition', 99))
        elif sort_option == "Rathaus-Level (Höchstes zuerst)":
            sorted_members = sorted(members, key=lambda m: m.get('townhallLevel', 0), reverse=True)
        elif sort_option == "Bester Angriff (Sterne)":
            sorted_members = sorted(members, key=lambda m: m['bestAttackStars'], reverse=True)
        elif sort_option == "Durchschnittliche Zerstörung":
            sorted_members = sorted(members, key=lambda m: m['avgDestruction'], reverse=True)

        # Karten-Anzeige
        for member in sorted_members:
            with st.container(border=True):
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    st.markdown(f"##### {member.get('mapPosition')}. {member.get('name')}")
                    st.caption(f"Rathaus-Level: {member.get('townhallLevel')}")
                
                # Zeigt die Angriffe an, falls vorhanden
                if 'attacks' in member:
                    for i, attack in enumerate(member['attacks']):
                        stars = "⭐" * attack['stars'] if attack['stars'] > 0 else "❌"
                        (col2 if i == 0 else col3).metric(f"Angriff {i+1}", f"{stars} {attack['destructionPercentage']}%")
                else:
                    col2.metric("Angriff 1", "Nicht angegriffen")