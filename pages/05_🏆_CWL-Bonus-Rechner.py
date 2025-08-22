# Dateiname: pages/05_🏆_CWL-Bonus-Rechner.py

import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="CWL Bonus Rechner", layout="wide")
st.title("🏆 Interaktiver CWL Bonus Rechner")

# --- ANPASSBARES PUNKTESYSTEM ---
with st.expander("⚙️ Punktesystem anpassen", expanded=True):
    points = {}
    
    st.subheader("PUNKTE FÜR RATHAUS-LEVEL DIFFERENZ (ELL)")
    c1, c2, c3, c4, c5 = st.columns(5)
    points['ell_rh_p2'] = c1.number_input("RH+2", value=3)
    points['ell_rh_p1'] = c2.number_input("RH+1", value=2)
    points['ell_rh_0'] = c3.number_input("RH=0", value=1)
    points['ell_rh_m1'] = c4.number_input("RH-1", value=0)
    points['ell_rh_m2'] = c5.number_input("RH-2", value=-1)
    
    st.subheader("PUNKTE FÜR ANGRIFFE")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("**3 Sterne**")
        points['atk_3s_vs_rh_p2'] = st.number_input("3⭐ vs RH+2", value=6)
        points['atk_3s_vs_rh_0'] = st.number_input("3⭐ vs RH=0", value=4)
        points['atk_3s_vs_rh_m2'] = st.number_input("3⭐ vs RH-2", value=2)
    with c2:
        st.markdown("**2 Sterne**")
        points['atk_2s_90'] = st.number_input("2⭐ (90%+)", value=4)
        points['atk_2s_80_89'] = st.number_input("2⭐ (80-89%)", value=3)
        points['atk_2s_50_79'] = st.number_input("2⭐ (50-79%)", value=2)
    with c3:
        st.markdown("**1 Stern**")
        points['atk_1s_90_99'] = st.number_input("1⭐ (90-99%)", value=2)
        points['atk_1s_50_89'] = st.number_input("1⭐ (50-89%)", value=1)

    st.subheader("BONUSPUNKTE")
    c1, c2, c3, c4, c5 = st.columns(5)
    points['bonus_aktiv'] = c1.number_input("Aktivität", value=1)
    points['bonus_100'] = c2.number_input("100% Bonus", value=1)
    points['bonus_mut'] = c3.number_input("Mutbonus (RH+3)", value=1)
    points['bonus_mut_extra'] = c4.number_input("Extra Mut (30-49%)", value=2)
    points['bonus_alle_7'] = c5.number_input("Alle 7 Angriffe", value=2)


# --- DATEN PRÜFEN ---
if 'cwl_wars_raw' not in st.session_state or not st.session_state.cwl_wars_raw:
    st.warning("Bitte lade zuerst die Daten auf der Startseite.")
    st.info("Dieser Rechner funktioniert nur, wenn eine CWL aktiv ist und die Daten geladen wurden. Außerdem befindet sich diese Seite in der Testphase.")
    st.page_link("Startseite.py", label="Zurück zur Startseite", icon="🏠")
else:
    # --- DATENAUFBEREITUNG & EDITIERBARE TABELLEN ---
    cwl_wars_data = st.session_state.cwl_wars_raw
    tab_list = st.tabs([f"Tag {i+1}" for i in range(len(cwl_wars_data))])
    edited_dfs = []

    for i, tab in enumerate(tab_list):
        with tab:
            st.subheader(f"Angriffe am {i+1}. Kriegstag")
            war_day_data = cwl_wars_data[i]
            opponent_th_levels = {m['tag']: m['townhallLevel'] for m in war_day_data.get('opponent', {}).get('members', [])}
            attacks_today = []
            for member in war_day_data.get('clan', {}).get('members', []):
                if 'attacks' in member:
                    attack = member['attacks'][0]
                    opponent_tag = attack['defenderTag']
                    attacks_today.append({
                        "Spieler": member['name'],
                        "Eigenes RH": member['townhallLevel'],
                        "Gegner RH (API)": opponent_th_levels.get(opponent_tag),
                        "Gegner RH (Korrektur)": opponent_th_levels.get(opponent_tag),
                        "Sterne": attack['stars'],
                        "Prozent": attack['destructionPercentage'],
                    })
            if not attacks_today:
                st.info("Für diesen Tag liegen noch keine Angriffsdaten vor.")
                continue
            df_today = pd.DataFrame(attacks_today)
            edited_df = st.data_editor(df_today, column_config={"Spieler": st.column_config.TextColumn(disabled=True), "Eigenes RH": st.column_config.NumberColumn(disabled=True), "Gegner RH (API)": st.column_config.NumberColumn(disabled=True), "Sterne": st.column_config.NumberColumn(disabled=True), "Prozent": st.column_config.NumberColumn(disabled=True), "Gegner RH (Korrektur)": st.column_config.NumberColumn("RH Korrektur", min_value=1, max_value=16, step=1, required=True)}, hide_index=True, use_container_width=True, key=f"editor_tag_{i+1}")
            edited_dfs.append(edited_df)
    st.divider()

    # --- BERECHNUNG & ERGEBNIS ---
    if st.button("Punkte berechnen!", type="primary", use_container_width=True):
        if not edited_dfs:
            st.error("Keine Angriffsdaten zum Berechnen vorhanden.")
        else:
            final_df = pd.concat(edited_dfs, ignore_index=True)
            rh_diff = final_df['Gegner RH (Korrektur)'] - final_df['Eigenes RH']
            
            ell_cond = [rh_diff >= 2, rh_diff == 1, rh_diff == 0, rh_diff == -1, rh_diff <= -2]
            ell_choices = [points['ell_rh_p2'], points['ell_rh_p1'], points['ell_rh_0'], points['ell_rh_m1'], points['ell_rh_m2']]
            ell_pts = np.select(ell_cond, ell_choices, default=0)

            atk_cond = [(final_df['Sterne'] == 3) & (rh_diff >= 2), (final_df['Sterne'] == 3) & (rh_diff.between(-1, 1)), (final_df['Sterne'] == 3) & (rh_diff <= -2), (final_df['Sterne'] == 2) & (final_df['Prozent'] >= 90), (final_df['Sterne'] == 2) & (final_df['Prozent'].between(80, 89)), (final_df['Sterne'] == 2) & (final_df['Prozent'].between(50, 79)), (final_df['Sterne'] == 1) & (final_df['Prozent'].between(90, 99)), (final_df['Sterne'] == 1) & (final_df['Prozent'].between(50, 89))]
            atk_choices = [points['atk_3s_vs_rh_p2'], points['atk_3s_vs_rh_0'], points['atk_3s_vs_rh_m2'], points['atk_2s_90'], points['atk_2s_80_89'], points['atk_2s_50_79'], points['atk_1s_90_99'], points['atk_1s_50_89']]
            atk_pts = np.select(atk_cond, atk_choices, default=0)

            bonus_aktiv_pts = points['bonus_aktiv']
            bonus_100_pts = np.where(final_df['Prozent'] == 100, points['bonus_100'], 0)
            mut_cond = [(rh_diff >= 3) & (final_df['Prozent'].between(30, 49)), (rh_diff >= 3)]
            mut_choices = [points['bonus_mut_extra'], points['bonus_mut']]
            mut_pts = np.select(mut_cond, mut_choices, default=0)

            final_df['punkte'] = ell_pts + atk_pts + bonus_aktiv_pts + bonus_100_pts + mut_pts
            result = final_df.groupby('Spieler')['punkte'].sum().reset_index()

            attack_counts = final_df['Spieler'].value_counts()
            alle_7_angriffe = attack_counts[attack_counts == 7].index
            result.loc[result['Spieler'].isin(alle_7_angriffe), 'punkte'] += points['bonus_alle_7']
            
            result = result.sort_values(by='punkte', ascending=False).reset_index(drop=True)
            result.index += 1

            st.subheader("🏆 Finale Bonus-Rangliste")
            st.dataframe(result, use_container_width=True)

            # --- NEU: BALKENDIAGRAMM ---
            st.subheader("📊 Visuelle Auswertung")
            
            # Daten für das Diagramm vorbereiten (Spieler als Index)
            chart_data = result.set_index('Spieler')
            
            st.bar_chart(chart_data['punkte'], color="#FFC300") # Goldene Farbe für die Balken
            # --- ENDE NEUER TEIL ---