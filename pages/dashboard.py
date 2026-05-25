import streamlit as st
from utils.dashboard_helpers import (
    filter_df,
    kpi_card,
    compute_kpis,
    bar_distribution,
    score_distribution,
    cross_mobilisation_by_category,
    summary_table,
)



st.set_page_config(page_title="Dashboard MLF", layout="wide")
st.title("Dashboard pédagogique")

df = st.session_state["df"]

# with st.sidebar:
#     st.header("Filtres")

#     etablissement = st.selectbox(
#         "Établissement",
#         ["Tous"] + sorted(df["etablissement"].dropna().unique()),
#     )

#     degre = st.selectbox(
#         "Degré",
#         ["Tous"] + sorted(df["degre"].dropna().unique()),
#     )

#     niveaux = st.multiselect(
#         "Niveau",
#         sorted(df["niveau_agrege"].dropna().unique()),
#     )

#     langue = st.selectbox(
#         "Langue",
#         ["Toutes"] + sorted(df["langue_groupe"].dropna().unique()),
#     )

# filtered = filter_df(df, etablissement, degre, niveaux, langue)

with st.sidebar:
    st.header("Filtres")

    etablissement = st.selectbox(
        "Établissement",
        ["Tous"] + sorted(df["etablissement"].dropna().unique()),
    )

    degre = st.selectbox(
        "Degré",
        ["Tous"] + sorted(df["degre"].dropna().unique()),
    )

    niveaux = st.multiselect(
        "Niveau",
        sorted(df["niveau_agrege"].dropna().unique()),
    )

    langue = st.selectbox(
        "Langue",
        [
            "Toutes",
            "Français",
            "Arabe",
            "Anglais",
            "Espagnol",
            "Bilingue / plurilingue",
            "Non renseigné",
        ],
    )

filtered = filter_df(df, etablissement, degre, niveaux, langue)

st.caption(f"{len(filtered)} observations dans le périmètre sélectionné.")

if filtered.empty:
    st.warning("Aucune donnée ne correspond aux filtres sélectionnés.")
    st.stop()

tab_synthese, tab_pratiques, tab_comparaison = st.tabs(
    ["Vue synthétique", "Pratiques pédagogiques", "Comparaison"]
)

with tab_synthese:
    st.subheader("Indicateurs principaux")

    kpis = compute_kpis(filtered)

    row1 = st.columns(4)
    with row1[0]:
        kpi_card("Observations", kpis["Observations"])
    with row1[1]:
        kpi_card("Engagement élevé", kpis["Engagement élevé"], "%")
    with row1[2]:
        kpi_card("Mobilisation élevée", kpis["Mobilisation élevée"], "%")
    with row1[3]:
        kpi_card("Ambiance favorable", kpis["Ambiance favorable"], "%")

    row2 = st.columns(4)
    with row2[0]:
        kpi_card("Posture accompagnante", kpis["Posture accompagnante"], "%")
    with row2[1]:
        kpi_card("Modalités actives", kpis["Modalités actives"], "%")
    with row2[2]:
        kpi_card("Organisation flexible", kpis["Organisation flexible"], "%")
    with row2[3]:
        kpi_card("Cahiers suivis", kpis["Cahiers suivis"], "%")

    st.divider()

    c1, c2 = st.columns(2)

    with c1:
        with st.container(border=True):
            fig = score_distribution(
                filtered,
                "mobilisation_score",
                "Mobilisation intellectuelle",
                {
                    1: "N1 - Exécution",
                    2: "N2 - Compréhension guidée",
                    3: "N3 - Réflexion",
                    4: "N4 - Raisonnement",
                },
            )
            st.plotly_chart(fig, use_container_width=True)

    with c2:
        with st.container(border=True):
            fig = score_distribution(
                filtered,
                "ambiance_score",
                "Ambiance de classe",
                {
                    1: "N1 - Tendu",
                    2: "N2 - Fluctuant",
                    3: "N3 - Calme",
                    4: "N4 - Serein",
                },
            )
            st.plotly_chart(fig, use_container_width=True)

with tab_pratiques:
    st.subheader("Pratiques observées")

    c1, c2, c3 = st.columns(3)

    with c1:
        with st.container(border=True):
            fig = bar_distribution(
                filtered,
                "posture",
                "Posture enseignante",
            )
            st.plotly_chart(fig, use_container_width=True)

    with c2:
        with st.container(border=True):
            fig = bar_distribution(
                filtered,
                "modalite",
                "Modalités de travail",
            )
            st.plotly_chart(fig, use_container_width=True)

    with c3:
        with st.container(border=True):
            fig = bar_distribution(
                filtered,
                "organisation",
                "Organisation de la salle",
            )
            st.plotly_chart(fig, use_container_width=True)

with tab_comparaison:
    st.subheader("Comparaison rapide")

    c1, c2 = st.columns(2)

    with c1:
        with st.container(border=True):
            fig = cross_mobilisation_by_category(
                filtered,
                "modalite",
                "Mobilisation élevée selon les modalités de travail",
            )
            st.plotly_chart(fig, use_container_width=True)

    with c2:
        with st.container(border=True):
            fig = cross_mobilisation_by_category(
                filtered,
                "organisation",
                "Mobilisation élevée selon l’organisation de salle",
            )
            st.plotly_chart(fig, use_container_width=True)

    with st.container(border=True):
        st.markdown("### Synthèse par établissement")
        st.dataframe(
            summary_table(filtered),
            use_container_width=True,
            hide_index=True,
        )
