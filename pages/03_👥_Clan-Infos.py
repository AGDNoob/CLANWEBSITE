import streamlit as st

st.set_page_config(page_title="Clan-Infos", layout="wide")
st.title("👥 Allgemeine Clan-Informationen")

# Prüft, ob die Clan-Daten im Langzeitgedächtnis vorhanden sind.
if 'clan_data' not in st.session_state or not st.session_state.clan_data:
    st.warning("Bitte lade zuerst die Daten auf der Startseite.")
    st.page_link("Startseite.py", label="Zurück zur Startseite", icon="🏠")
else:
    # Holt die Daten aus dem Gedächtnis
    clan_data = st.session_state.clan_data

    # Prüft auf Fehler, die beim Laden aufgetreten sein könnten
    if clan_data.get("reason"):
        st.error(f"Fehler beim Laden der Clan-Daten: {clan_data.get('reason')}")
    else:
        # --- CLAN-ÜBERSICHT ---
        st.subheader(f"Statistiken für {clan_data.get('name')} ({clan_data.get('tag')})")
        st.info(f"Beschreibung: *{clan_data.get('description')}*")

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Clan-Level", clan_data.get('clanLevel', 0))
        col2.metric("Clan-Punkte", f"{clan_data.get('clanPoints', 0)} 🏆")
        col3.metric("Kriegs-Trophäen", f"{clan_data.get('clanWarTrophies', 0)} ⚔️")
        col4.metric("Mitglieder", f"{len(clan_data.get('memberList', []))} / 50")
        st.divider()

        # --- SORTIER-FUNKTION & KARTENANZEIGE ---
        st.subheader("Mitgliederliste")
        
        sort_option = st.selectbox(
            "Sortiere Mitglieder nach:",
            (
                "Clan-Rang", 
                "Rolle (Anführer zuerst)", 
                "Level (Höchstes zuerst)", 
                "Trophäen (Meiste zuerst)", 
                "Spenden (Meiste zuerst)", 
                "Erhalten (Meiste zuerst)"
            )
        )

        member_list = clan_data.get('memberList', [])
        
        # Sortierlogik
        if sort_option == "Clan-Rang":
            sorted_list = sorted(member_list, key=lambda m: m.get('clanRank', 99))
        elif sort_option == "Level (Höchstes zuerst)":
            sorted_list = sorted(member_list, key=lambda m: m.get('expLevel', 0), reverse=True)
        elif sort_option == "Trophäen (Meiste zuerst)":
            sorted_list = sorted(member_list, key=lambda m: m.get('trophies', 0), reverse=True)
        elif sort_option == "Spenden (Meiste zuerst)":
            sorted_list = sorted(member_list, key=lambda m: m.get('donations', 0), reverse=True)
        elif sort_option == "Erhalten (Meiste zuerst)":
            sorted_list = sorted(member_list, key=lambda m: m.get('donationsReceived', 0), reverse=True)
        elif sort_option == "Rolle (Anführer zuerst)":
            role_priority = {"leader": 0, "coLeader": 1, "admin": 2, "member": 3}
            sorted_list = sorted(member_list, key=lambda m: role_priority.get(m.get('role', 'member')))

        # Rollen übersetzen für eine schönere Anzeige
        role_map = {
            "leader": "Anführer",
            "coLeader": "Vize-Anführer",
            "admin": "Ältester",
            "member": "Mitglied"
        }

        # Kartenanzeige
        for member in sorted_list:
            with st.container(border=True):
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.markdown(f"##### {member.get('clanRank')}. {member.get('name')}")
                    st.caption(f"Level: {member.get('expLevel')} | Rolle: {role_map.get(member.get('role'))}")
                with col2:
                    sub_col1, sub_col2, sub_col3 = st.columns(3)
                    sub_col1.metric("Trophäen 🏆", member.get('trophies', 0))
                    sub_col2.metric("Spenden 👍", member.get('donations', 0))
                    sub_col3.metric("Erhalten 👇", member.get('donationsReceived', 0))