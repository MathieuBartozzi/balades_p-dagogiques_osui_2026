import pandas as pd
import streamlit as st

@st.cache_data(show_spinner=True)
def load_data(file_key: str, gid_key: str | None = None) -> pd.DataFrame:
    """
    Charge un Google Sheet exporté en CSV à partir de st.secrets["google"].

    Exemples acceptés dans secrets.toml :

    [google]
    file_id = "..."
    gid = "..."

    ou :

    [google]
    result_id = "..."
    result_id_gid = "..."
    """
    try:
        google_secrets = st.secrets["google"]

        file_id = google_secrets[file_key]

        if gid_key is not None:
            gid = google_secrets.get(gid_key, "0")
        else:
            gid = google_secrets.get(f"{file_key}_gid", google_secrets.get("gid", "0"))

        url = (
            f"https://docs.google.com/spreadsheets/d/{file_id}/export"
            f"?format=csv&gid={gid}"
        )

        df = pd.read_csv(url)

        if df is None or df.empty:
            return pd.DataFrame()

        return df

    except KeyError as e:
        st.error(f"Clé manquante dans st.secrets['google'] : {e}")
        return pd.DataFrame()

    except pd.errors.EmptyDataError:
        st.warning(f"Le fichier '{file_key}' est vide.")
        return pd.DataFrame()

    except Exception as e:
        st.error(f"Erreur lors du chargement du fichier {file_key} : {e}")
        return pd.DataFrame()
# def load_data(file_key: str) -> pd.DataFrame:
#     """
#     Charge un fichier CSV stocké sur Google Drive à partir de la clé
#     définie dans .streamlit/secrets.toml.

#     Retourne toujours un DataFrame, même si le fichier est vide
#     ou qu'une erreur survient.
#     """
#     try:
#         file_id = st.secrets["google"][file_key]
#         # url = f"https://drive.google.com/uc?id={file_id}"
#         url = f"https://docs.google.com/spreadsheets/d/{file_id}/export?format=csv"

#         try:
#             df = pd.read_csv(url)
#         except pd.errors.EmptyDataError:
#             # Le fichier existe mais ne contient aucune donnée
#             return pd.DataFrame()

#         # Sécurité supplémentaire : si pandas retourne None ou objet inattendu
#         if df is None:
#             return pd.DataFrame()

#         return df

    # except KeyError:
    #     st.error(f"Clé introuvable dans st.secrets['google'] : {file_key}")
    #     return pd.DataFrame()

    # except Exception as e:
    #     st.error(f"Erreur lors du chargement du fichier {file_key} : {e}")
    #     return pd.DataFrame()
