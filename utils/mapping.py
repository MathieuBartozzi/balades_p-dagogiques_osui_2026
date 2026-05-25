import pandas as pd


RAW_TO_BUSINESS = {
    "etablissement": "etablissement",
    "niveau": "niveau",
    "cycle": "cycle",
    "2nombre_d_eleves_dans_la_classe": "nombre_eleves",
    "accueil_en_cours": "accueil",
    "organisation_de_la_classe": "organisation",
    "modalite_dominante_dactivite_des_eleves": "modalite",
    "engagement_dans_la_classe": "engagement",
    "ambiance_de_travail_et_la_stabilite_du_cadre": "ambiance",
    "niveau_de_mobilisation_intellectuelle": "mobilisation",
    "nombre_de_cahiers_observes": "nombre_cahiers",
    "qualite_moyenne_de_la_tenue_des_cahiers_observes": "qualite_cahiers",
    "les_cahiers_sont_ils_corriges_par_l_enseignant": "correction_cahiers",
    "cahier_usage_repete": "usage_cahier",
    "cahier_taux_de_presence_tranches_de_25": "presence_cahiers",
    "type_de_support_employe_par_l_enseignant": "supports",
    "langue_de_travail_de_lenseignant": "langue",
    "niveau_de_maitrise_de_la_langue_de_travail_de_lenseignant": "maitrise_langue",
    "posture_de_lenseignant_dans_la_seance": "posture",
    "faits_observables_uniquement": "faits_observables",
}


def rename_business_columns(df):
    df = df.copy()

    rename_dict = {}

    for raw_col, business_col in RAW_TO_BUSINESS.items():
        if raw_col in df.columns:
            rename_dict[raw_col] = business_col

    df = df.rename(columns=rename_dict)

    return df


def map_niveau_agrege(niveau):
    if pd.isna(niveau):
        return "Non renseigné"

    n = str(niveau).lower()

    if any(x in n for x in ["ps", "ms", "gs"]):
        return "Maternelle"

    if any(x in n for x in ["cp", "ce1", "ce2", "cm1", "cm2"]):
        return "Élémentaire"

    if any(x in n for x in ["6e", "5e", "4e", "3e"]):
        return "Collège"

    if any(x in n for x in ["2nde", "1ere", "1ère", "terminale"]):
        return "Lycée"

    return "Non renseigné"


def map_degre(niveau_agrege):
    if niveau_agrege in ["Maternelle", "Élémentaire"]:
        return "Premier degré"

    if niveau_agrege in ["Collège", "Lycée"]:
        return "Second degré"

    return "Non renseigné"


def extract_niveau_score(value):
    if pd.isna(value):
        return None

    value = str(value)

    if "Niveau 1" in value:
        return 1

    if "Niveau 2" in value:
        return 2

    if "Niveau 3" in value:
        return 3

    if "Niveau 4" in value:
        return 4

    return None


def map_engagement_score(value):
    if pd.isna(value):
        return None

    value = str(value)
    value = value.replace("–", "-")
    value = value.replace(" ", "")

    mapping = {
        "0-25%": 1,
        "25-50%": 2,
        "50-75%": 3,
        "75-100%": 4,
    }

    return mapping.get(value)


def detect_langues(value):
    if pd.isna(value) or str(value).strip() == "":
        return []

    value = str(value).lower()

    langues = []

    if "français" in value or "francais" in value:
        langues.append("Français")

    if "arabe" in value:
        langues.append("Arabe")

    if "anglais" in value or "english" in value:
        langues.append("Anglais")

    if "espagnol" in value or "espagnole" in value or "spanish" in value:
        langues.append("Espagnol")

    return langues


def map_langue_groupe(value):
    langues = detect_langues(value)

    if len(langues) == 0:
        return "Non renseigné"

    if len(langues) == 1:
        return langues[0]

    return "Bilingue / plurilingue"


def enrich_dataframe(df):
    df = df.copy()

    df = rename_business_columns(df)

    df["niveau_agrege"] = df["niveau"].apply(map_niveau_agrege)

    df["degre"] = df["niveau_agrege"].apply(map_degre)

    df["engagement_score"] = df["engagement"].apply(
        map_engagement_score
    )

    df["ambiance_score"] = df["ambiance"].apply(
        extract_niveau_score
    )

    df["mobilisation_score"] = df["mobilisation"].apply(
        extract_niveau_score
    )

    df["langues_detectees"] = df["langue"].apply(detect_langues)

    df["langue_groupe"] = df["langue"].apply(map_langue_groupe)

    df["langue_francais"] = df["langues_detectees"].apply(lambda x: "Français" in x)
    df["langue_arabe"] = df["langues_detectees"].apply(lambda x: "Arabe" in x)
    df["langue_anglais"] = df["langues_detectees"].apply(lambda x: "Anglais" in x)
    df["langue_espagnol"] = df["langues_detectees"].apply(lambda x: "Espagnol" in x)

    df["langue_bilingue"] = df["langues_detectees"].apply(lambda x: len(x) >= 2)

    df["engagement_eleve"] = df["engagement_score"].eq(4)

    df["mobilisation_elevee"] = df["mobilisation_score"].isin([3, 4])

    df["ambiance_favorable"] = df["ambiance_score"].isin([3, 4])

    df["posture_accompagnante"] = df["posture"].isin([
        "Circulation et accompagnement régulier",
        "Accompagnement individualisé majoritaire",
    ])

    df["modalite_active"] = df["modalite"].isin([
        "Binôme",
        "Travail de groupe",
    ])

    df["organisation_flexible"] = df["organisation"].isin([
        "Îlots",
        "En U",
        "Modulaire",
    ])

    df["cahiers_suivis"] = df["correction_cahiers"].isin([
        "Oui",
        "Partiellement",
    ])

    return df
