import streamlit as st
import pandas as pd
import plotly.express as px
from utils.dashboard_helpers import (
    filter_df,
    bar_distribution,
    cross_mobilisation_by_category,
    prepare_cahiers_elementaire_sixieme,
    cahiers_summary_table,
    cahiers_comparison_chart,
)


st.set_page_config(page_title="Dashboard MLF", layout="wide")
st.title("Analyse détaillée")

df = st.session_state["df"]

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

tab_croisements, tab_langues, tab_cahiers, tab_donnees = st.tabs(
    [
        "Croisements",
        "Focus langues",
        "Cahiers & rétroaction",
        "Données",
    ]
)

with tab_croisements:
    st.subheader("Croisements demandés")

    c1, c2, c3 = st.columns(3)

    with c1:
        with st.container(border=True):
            fig = cross_mobilisation_by_category(
                filtered,
                "modalite",
                "Mobilisation × modalités de travail",
            )
            st.plotly_chart(fig, use_container_width=True)

    with c2:
        with st.container(border=True):
            fig = cross_mobilisation_by_category(
                filtered,
                "organisation",
                "Organisation × mobilisation",
            )
            st.plotly_chart(fig, use_container_width=True)

    with c3:
        with st.container(border=True):
            fig = cross_mobilisation_by_category(
                filtered,
                "posture",
                "Mobilisation selon la posture enseignante",
            )
            st.plotly_chart(fig, use_container_width=True)

with tab_langues:
    st.subheader("Focus langues — premier degré")

    premier_degre = filtered[filtered["degre"] == "Premier degré"]

    if premier_degre.empty:
        st.info("Aucune donnée premier degré dans le périmètre sélectionné.")
    else:
        c1, c2 = st.columns(2)

        with c1:
            with st.container(border=True):
                fig = bar_distribution(
                    premier_degre,
                    "langue_groupe",
                    "Répartition français / autres langues",
                )
                st.plotly_chart(fig, use_container_width=True)

        with c2:
            with st.container(border=True):
                fig = cross_mobilisation_by_category(
                    premier_degre,
                    "langue_groupe",
                    "Mobilisation élevée selon la langue",
                )
                st.plotly_chart(fig, use_container_width=True)

        st.markdown("### Indicateurs demandés par langue")

        lang_tabs = st.tabs(["Posture", "Organisation", "Modalités"])

        with lang_tabs[0]:
            fig = bar_distribution(
                premier_degre,
                "posture",
                "Posture enseignante — premier degré",
                orientation="h",
            )
            st.plotly_chart(fig, use_container_width=True)

        with lang_tabs[1]:
            fig = bar_distribution(
                premier_degre,
                "organisation",
                "Organisation de salle — premier degré",
                orientation="h",
            )
            st.plotly_chart(fig, use_container_width=True)

        with lang_tabs[2]:
            fig = bar_distribution(
                premier_degre,
                "modalite",
                "Modalités de travail — premier degré",
            )
            st.plotly_chart(fig, use_container_width=True)

# with tab_cahiers:
#     st.subheader("Cahiers et rétroaction")

#     c1, c2 = st.columns(2)

#     with c1:
#         with st.container(border=True):
#             fig = bar_distribution(
#                 filtered,
#                 "correction_cahiers",
#                 "Correction des cahiers",
#             )
#             st.plotly_chart(fig, use_container_width=True)

#     with c2:
#         with st.container(border=True):
#             fig = bar_distribution(
#                 filtered,
#                 "presence_cahiers",
#                 "Taux de présence des cahiers",
#             )
#             st.plotly_chart(fig, use_container_width=True)

#     st.markdown("### Comparaison élémentaire / 6e")

#     subset = filtered[
#         (filtered["niveau_agrege"] == "Élémentaire")
#         | (filtered["niveau"].astype(str).str.contains("6e", case=False, na=False))
#     ]

#     if subset.empty:
#         st.info("Aucune donnée disponible pour la comparaison élémentaire / 6e.")
#     else:
#         with st.container(border=True):
#             fig = bar_distribution(
#                 subset,
#                 "presence_cahiers",
#                 "Correction des cahiers — élémentaire / 6e",
#             )
#             st.plotly_chart(fig, use_container_width=True)

#         st.dataframe(
#             subset[
#                 [
#                     "etablissement",
#                     "niveau",
#                     "niveau_agrege",
#                     "nombre_cahiers",
#                     "qualite_cahiers",
#                     "correction_cahiers",
#                     "usage_cahier",
#                     "presence_cahiers",
#                 ]
#             ],
#             use_container_width=True,
#             hide_index=True,
#         )

with tab_cahiers:
    st.subheader("Cahiers et rétroaction")

    c1, c2 = st.columns(2)

    with c1:
        with st.container(border=True):
            fig = bar_distribution(
                filtered,
                "correction_cahiers",
                "Correction des cahiers",
            )
            st.plotly_chart(fig, use_container_width=True)

    with c2:
        with st.container(border=True):
            fig = bar_distribution(
                filtered,
                "presence_cahiers",
                "Taux de présence des cahiers",
            )
            st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Comparaison élémentaire / sixième")

    subset = prepare_cahiers_elementaire_sixieme(filtered)

    if subset.empty:
        st.info("Aucune donnée disponible pour la comparaison élémentaire / sixième.")
    else:
        st.caption(
            "Comparaison centrée sur les indicateurs de cahiers : présence, correction, qualité et usage."
        )

        summary = cahiers_summary_table(subset)

        c1, c2, c3 = st.columns(3)

        with c1:
            with st.container(border=True):
                st.metric(
                    "Observations élémentaire",
                    int(
                        summary.loc[
                            summary["Groupe"] == "Élémentaire",
                            "Observations",
                        ].sum()
                    ),
                )

        with c2:
            with st.container(border=True):
                st.metric(
                    "Observations sixième",
                    int(
                        summary.loc[
                            summary["Groupe"] == "Sixième",
                            "Observations",
                        ].sum()
                    ),
                )

        with c3:
            with st.container(border=True):
                st.metric(
                    "Cahiers suivis",
                    f"{summary['Cahiers suivis (%)'].mean().round(1)}%",
                )

        with st.container(border=True):
            st.markdown("#### Synthèse des cahiers suivis")
            st.dataframe(
                summary,
                use_container_width=True,
                hide_index=True,
            )

        indicateurs_cahiers = [
            ("presence_cahiers", "Présence des cahiers — élémentaire vs sixième"),
            ("correction_cahiers", "Correction des cahiers — élémentaire vs sixième"),
            ("qualite_cahiers", "Qualité de tenue des cahiers — élémentaire vs sixième"),
            ("usage_cahier", "Usage répété du cahier — élémentaire vs sixième"),
        ]

        for col, title in indicateurs_cahiers:
            if col not in subset.columns:
                st.warning(f"Colonne absente : {col}")
                continue

            with st.container(border=True):
                fig = cahiers_comparison_chart(
                    subset,
                    col,
                    title,
                )
                st.plotly_chart(fig, use_container_width=True)

        with st.expander("Voir le détail des observations élémentaire / sixième"):
            st.dataframe(
                subset[
                    [
                        "etablissement",
                        "niveau",
                        "groupe_comparaison",
                        "nombre_cahiers",
                        "qualite_cahiers",
                        "correction_cahiers",
                        "usage_cahier",
                        "presence_cahiers",
                    ]
                ].sort_values(
                    [
                        "groupe_comparaison",
                        "etablissement",
                        "niveau",
                    ]
                ),
                use_container_width=True,
                hide_index=True,
            )

with tab_donnees:
    st.subheader("Données filtrées")

    with st.container(border=True):
        st.dataframe(filtered, use_container_width=True, hide_index=True)

    csv = filtered.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Télécharger les données filtrées",
        data=csv,
        file_name="donnees_filtrees_balades_pedagogiques.csv",
        mime="text/csv",
        use_container_width=True,
    )
