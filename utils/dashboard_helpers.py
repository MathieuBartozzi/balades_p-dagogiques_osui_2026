import pandas as pd
import plotly.express as px
import streamlit as st

from utils.palette import PRIMARY, CHART_COLORS


def safe_col(df, col):
    if col not in df.columns:
        st.warning(f"Colonne absente : {col}")
        return pd.Series(dtype="object")
    return df[col]


def pct(series):
    if len(series) == 0:
        return 0
    return round(series.mean() * 100, 1)


# def filter_df(df, etablissement, degre, niveaux, langue):
#     filtered = df.copy()

#     if etablissement != "Tous":
#         filtered = filtered[filtered["etablissement"] == etablissement]

#     if degre != "Tous":
#         filtered = filtered[filtered["degre"] == degre]

#     if niveaux:
#         filtered = filtered[filtered["niveau_agrege"].isin(niveaux)]

#     if langue != "Toutes":
#         filtered = filtered[filtered["langue_groupe"] == langue]

#     return filtered

def filter_df(df, etablissement, degre, niveaux, langue):
    filtered = df.copy()

    if etablissement != "Tous":
        filtered = filtered[filtered["etablissement"] == etablissement]

    if degre != "Tous":
        filtered = filtered[filtered["degre"] == degre]

    if niveaux:
        filtered = filtered[filtered["niveau_agrege"].isin(niveaux)]

    if langue == "Français":
        filtered = filtered[filtered["langue_francais"]]

    elif langue == "Arabe":
        filtered = filtered[filtered["langue_arabe"]]

    elif langue == "Anglais":
        filtered = filtered[filtered["langue_anglais"]]

    elif langue == "Espagnol":
        filtered = filtered[filtered["langue_espagnol"]]

    elif langue == "Bilingue / plurilingue":
        filtered = filtered[filtered["langue_bilingue"]]

    elif langue == "Non renseigné":
        filtered = filtered[filtered["langue_groupe"] == "Non renseigné"]

    return filtered


def kpi_card(label, value, suffix="", help_text=None):
    with st.container(border=True):
        st.metric(label=label, value=f"{value}{suffix}", help=help_text)


def compute_kpis(df):
    return {
        "Observations": len(df),
        "Engagement élevé": pct(df["engagement_eleve"]),
        "Mobilisation élevée": pct(df["mobilisation_elevee"]),
        "Ambiance favorable": pct(df["ambiance_favorable"]),
        "Posture accompagnante": pct(df["posture_accompagnante"]),
        "Modalités actives": pct(df["modalite_active"]),
        "Organisation flexible": pct(df["organisation_flexible"]),
        "Cahiers suivis": pct(df["cahiers_suivis"]),
    }


def bar_distribution(df, col, title, orientation="h"):
    data = (
        df[col]
        .fillna("Non renseigné")
        .value_counts(normalize=True)
        .mul(100)
        .round(1)
        .reset_index()
    )
    data.columns = [col, "Pourcentage"]

    if orientation == "h":
        fig = px.bar(
            data,
            x="Pourcentage",
            y=col,
            orientation="h",
            text="Pourcentage",
            color=col,
            color_discrete_sequence=CHART_COLORS,
        )
    else:
        fig = px.bar(
            data,
            x=col,
            y="Pourcentage",
            text="Pourcentage",
            color=col,
            color_discrete_sequence=CHART_COLORS,
        )

    fig.update_layout(
        title=title,
        showlegend=False,
        margin=dict(l=10, r=10, t=50, b=10),
        height=450,
        xaxis_title=None,
        yaxis_title=None,
    )
    fig.update_xaxes(
        range=[0, data["Pourcentage"].max() * 1.18],
        title_text=None,
    )
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig.update_yaxes(tickangle=-30)

    return fig



def score_distribution(df, score_col, title, labels):
    data = (
        df[score_col]
        .dropna()
        .astype(int)
        .value_counts(normalize=True)
        .mul(100)
        .reindex([1, 2, 3, 4], fill_value=0)
        .round(1)
        .reset_index()
    )

    data.columns = ["Score", "Pourcentage"]
    data["Libellé"] = data["Score"].map(labels)

    fig = px.pie(
        data,
        names="Libellé",
        values="Pourcentage",
        color="Libellé",
        color_discrete_sequence=CHART_COLORS,
        hole=0.45,
    )

    fig.update_traces(
        textinfo="percent",
        textposition="inside",
        insidetextorientation="radial",
        hovertemplate="%{label}<br>%{value:.1f}%<extra></extra>",
    )

    fig.update_layout(
        title=title,
        showlegend=True,
        margin=dict(l=10, r=10, t=50, b=10),
        height=380,
    )

    return fig


# def cross_mobilisation_by_category(df, category_col, title):
#     data = (
#         df.groupby(category_col, dropna=False)["mobilisation_elevee"]
#         .mean()
#         .mul(100)
#         .round(1)
#         .reset_index()
#     )
#     data[category_col] = data[category_col].fillna("Non renseigné")

#     fig = px.bar(
#         data,
#         x=category_col,
#         y="mobilisation_elevee",
#         text="mobilisation_elevee",
#         color=category_col,
#         color_discrete_sequence=CHART_COLORS,
#     )
#     fig.update_layout(
#         title=title,
#         yaxis_title="% mobilisation élevée",
#         xaxis_title="",
#         showlegend=False,
#         margin=dict(l=10, r=10, t=50, b=10),
#         height=400,
#     )
#     fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
#     return fig

# def cross_mobilisation_by_category(df, category_col, title):
#     data = (
#         df.groupby(category_col, dropna=False)["mobilisation_elevee"]
#         .mean()
#         .mul(100)
#         .round(1)
#         .reset_index()
#     )
#     data[category_col] = data[category_col].fillna("Non renseigné")
#     data = data.sort_values("mobilisation_elevee", ascending=False)


#     fig = px.bar(
#         data,
#         y=category_col,
#         y="mobilisation_elevee",
#         text="mobilisation_elevee",
#         orientation="h",
#         color=category_col,
#         color_discrete_sequence=CHART_COLORS,
#     )

#     fig.update_layout(
#         title=title,
#         yaxis_title="% mobilisation élevée",
#         xaxis_title="",
#         showlegend=False,
#         margin=dict(l=10, r=10, t=50, b=90),
#         height=400,
#         yaxis=dict(
#             range=[0, 100],
#             tickformat=".0f",
#         ),
#     )

#     fig.update_traces(
#         texttemplate="%{text:.1f}%",
#         textposition="outside",
#         cliponaxis=False,
#     )

#     fig.update_xaxes(
#         tickangle=-30,
#         automargin=True,
#     )

#     return

def cross_mobilisation_by_category(df, category_col, title):
    data = (
        df.groupby(category_col, dropna=False)["mobilisation_elevee"]
        .mean()
        .mul(100)
        .round(1)
        .reset_index()
    )

    data[category_col] = data[category_col].fillna("Non renseigné")
    data = data.sort_values("mobilisation_elevee", ascending=False)

    fig = px.bar(
        data,
        x="mobilisation_elevee",
        y=category_col,
        text="mobilisation_elevee",
        orientation="h",
        color=category_col,
        color_discrete_sequence=CHART_COLORS,
    )

    fig.update_layout(
        title=title,
        xaxis_title="% mobilisation élevée",
        yaxis_title="",
        showlegend=False,
        margin=dict(l=10, r=40, t=50, b=40),
        height=400,
        xaxis=dict(
            range=[0, 100],
            tickformat=".0f",
        ),
    )

    fig.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside",
        cliponaxis=False,
    )

    fig.update_yaxes(
        automargin=True,
    )

    return fig

def summary_table(df):
    group = (
        df.groupby("etablissement")
        .agg(
            observations=("etablissement", "size"),
            mobilisation_elevee=("mobilisation_elevee", "mean"),
            engagement_eleve=("engagement_eleve", "mean"),
            ambiance_favorable=("ambiance_favorable", "mean"),
            posture_accompagnante=("posture_accompagnante", "mean"),
        )
        .reset_index()
    )

    for col in [
        "mobilisation_elevee",
        "engagement_eleve",
        "ambiance_favorable",
        "posture_accompagnante",
    ]:
        group[col] = (group[col] * 100).round(1)

    return group
