def pct(series):
    if len(series) == 0:
        return 0
    return round(series.mean() * 100, 1)


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
