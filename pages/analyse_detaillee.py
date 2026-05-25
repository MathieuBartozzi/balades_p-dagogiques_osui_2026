import streamlit as st
import pandas as pd
import plotly.express as px


from utils.dashboard_helpers import (
    filter_df,
    bar_distribution,
    cross_mobilisation_by_category,
    score_distribution,
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

    subset = filtered[
        (filtered["niveau_agrege"] == "Élémentaire")
        | (
            filtered["niveau"]
            .astype(str)
            .str.contains(r"6e|6ème|6eme|sixième|sixieme", case=False, na=False)
        )
    ].copy()

    if subset.empty:
        st.info("Aucune donnée disponible pour la comparaison élémentaire / sixième.")
    else:
        subset["groupe_comparaison"] = "Élémentaire"

        subset.loc[
            subset["niveau"]
            .astype(str)
            .str.contains(r"6e|6ème|6eme|sixième|sixieme", case=False, na=False),
            "groupe_comparaison",
        ] = "Sixième"

        ordre_groupes = ["Élémentaire", "Sixième"]

        subset["groupe_comparaison"] = pd.Categorical(
            subset["groupe_comparaison"],
            categories=ordre_groupes,
            ordered=True,
        )

        st.caption(
            "Comparaison centrée sur les indicateurs de cahiers : présence, correction, qualité et usage."
        )

        synthese = (
            subset.groupby("groupe_comparaison", observed=False)
            .agg(
                observations=("groupe_comparaison", "size"),
                cahiers_suivis=("cahiers_suivis", "mean"),
            )
            .reset_index()
        )

        synthese["Cahiers suivis (%)"] = (
            synthese["cahiers_suivis"] * 100
        ).round(1)

        synthese = synthese.drop(columns=["cahiers_suivis"])
        synthese.columns = ["Groupe", "Observations", "Cahiers suivis (%)"]

        k1, k2 = st.columns(2)

        with k1:
            st.metric(
                "Observations élémentaire",
                int(
                    synthese.loc[
                        synthese["Groupe"] == "Élémentaire",
                        "Observations",
                    ].sum()
                ),
            )

        with k2:
            st.metric(
                "Observations sixième",
                int(
                    synthese.loc[
                        synthese["Groupe"] == "Sixième",
                        "Observations",
                    ].sum()
                ),
            )

        with st.container(border=True):
            st.markdown("#### Synthèse des cahiers suivis")
            st.dataframe(
                synthese,
                use_container_width=True,
                hide_index=True,
            )

        indicateurs_cahiers = [
            ("presence_cahiers", "Présence des cahiers"),
            ("correction_cahiers", "Correction des cahiers"),
            ("qualite_cahiers", "Qualité de tenue des cahiers"),
            ("usage_cahier", "Usage répété du cahier"),
        ]

        for col, titre in indicateurs_cahiers:
            if col not in subset.columns:
                st.warning(f"Colonne absente : {col}")
                continue

            data = (
                subset.assign(reponse=subset[col].fillna("Non renseigné"))
                .groupby(["groupe_comparaison", "reponse"], observed=False)
                .size()
                .reset_index(name="Nombre")
            )

            data["Pourcentage"] = (
                data["Nombre"]
                / data.groupby("groupe_comparaison", observed=False)["Nombre"].transform("sum")
                * 100
            ).round(1)

            with st.container(border=True):
                fig = px.bar(
                    data,
                    x="Pourcentage",
                    y="reponse",
                    color="groupe_comparaison",
                    barmode="group",
                    text="Pourcentage",
                    orientation="h",
                    category_orders={
                        "groupe_comparaison": ordre_groupes,
                    },
                    title=f"{titre} — élémentaire vs sixième",
                )

                fig.update_layout(
                    xaxis_title="% des observations du groupe",
                    yaxis_title="",
                    legend_title="Groupe",
                    margin=dict(l=10, r=40, t=60, b=40),
                    height=420,
                )

                fig.update_xaxes(
                    range=[0, 100],
                    tickformat=".0f",
                )

                fig.update_traces(
                    texttemplate="%{text:.1f}%",
                    textposition="outside",
                    cliponaxis=False,
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
                    ["groupe_comparaison", "etablissement", "niveau"]
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
