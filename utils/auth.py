# import streamlit as st

# # Récupération des secrets selon ton format exact
# CLIENT_ID = st.secrets["auth"]["client_id"]
# CLIENT_SECRET = st.secrets["auth"]["client_secret"]
# REDIRECT_URI = st.secrets["auth"]["redirect_uri"]
# AUTHORIZATION_URL = "https://accounts.google.com/o/oauth2/v2/auth" # Déduit de ton metadata_url

# def get_login_url():
#     """Construit l'URL d'autorisation Google."""
#     # Tu utilises ici ta librairie OAuth ou une simple construction de string
#     # Exemple simplifié :
#     scope = "openid email profile"
#     return f"{AUTHORIZATION_URL}?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope={scope}"

# def get_logged_in_user():
#     """
#     Vérifie si l'utilisateur est connecté (ex: check dans st.session_state).
#     Gère également l'interception du paramètre '?code=' dans l'URL après la redirection.
#     """
#     # if "user" in st.session_state:
#     #     return st.session_state["user"]
#     if "user" in st.session_state:

#         user = st.session_state["user"]

#     if is_allowed_user(user["email"]):
#         return user

#     del st.session_state["user"]
#     return None

#     # Logique pour intercepter le code depuis les query params et récupérer le token...
#     # query_params = st.query_params
#     # if "code" in query_params: ...

#     return None

# def logout_user():
#     """Déconnecte l'utilisateur et nettoie le session_state."""
#     if "user" in st.session_state:
#         del st.session_state["user"]
#     st.rerun()

# def get_access_config():
#     access = st.secrets.get("access", {})

#     mode = access.get("mode", "domain").lower()
#     allowed_domain = access.get("allowed_domain", "").lower()
#     allowed_users = {
#         email.lower() for email in access.get("allowed_users", [])
#     }

#     return mode, allowed_domain, allowed_users

# def is_allowed_user(email: str) -> bool:

#     mode, allowed_domain, allowed_users = get_access_config()

#     email = email.lower().strip()

#     if mode == "domain":
#         return email.endswith(f"@{allowed_domain}")

#     if mode == "allowlist":
#         return email in allowed_users

#     return False

import streamlit as st
import pandas as pd
from urllib.parse import urlparse


CLIENT_ID = st.secrets["auth"]["client_id"]
CLIENT_SECRET = st.secrets["auth"]["client_secret"]
REDIRECT_URI = st.secrets["auth"]["redirect_uri"]
AUTHORIZATION_URL = "https://accounts.google.com/o/oauth2/v2/auth"


def get_login_url():
    """Construit l'URL d'autorisation Google."""
    scope = "openid email profile"
    return (
        f"{AUTHORIZATION_URL}"
        f"?client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&response_type=code"
        f"&scope={scope}"
    )


def google_sheet_url_to_csv_url(sheet_url: str, tab_name: str | None = None) -> str:
    """
    Transforme une URL Google Sheet en URL CSV exportable.

    Fonctionne si le Google Sheet est accessible publiquement ou partagé avec l'app.
    """
    sheet_id = sheet_url.split("/d/")[1].split("/")[0]

    # Version simple : lit le premier onglet visible du Google Sheet.
    # Pour cibler précisément un onglet par nom, il faut idéalement utiliser gspread
    # ou récupérer le gid de l'onglet.
    return f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"


@st.cache_data(ttl=300)
def load_allowed_users_from_google_sheet(
    sheet_url: str,
    tab_name: str,
    email_column: str,
) -> set[str]:
    csv_url = google_sheet_url_to_csv_url(sheet_url, tab_name)

    df = pd.read_csv(csv_url)

    if email_column not in df.columns:
        raise ValueError(
            f"Colonne '{email_column}' introuvable dans le Google Sheet. "
            f"Colonnes trouvées : {list(df.columns)}"
        )

    emails = (
        df[email_column]
        .dropna()
        .astype(str)
        .str.lower()
        .str.strip()
    )

    return set(emails)


def get_access_config():
    access = st.secrets.get("access", {})

    mode = access.get("mode", "domain").lower()
    allowed_domain = access.get("allowed_domain", "").lower().strip()

    allowed_users = {
        email.lower().strip()
        for email in access.get("allowed_users", [])
    }

    sheet_url = access.get("allowed_users_google_sheet")
    sheet_tab = access.get("allowed_users_sheet_tab", "allowed_users")
    email_column = access.get("allowed_users_column", "email")

    if sheet_url:
        allowed_users = load_allowed_users_from_google_sheet(
            sheet_url=sheet_url,
            tab_name=sheet_tab,
            email_column=email_column,
        )

    return mode, allowed_domain, allowed_users


def is_allowed_user(email: str) -> bool:
    mode, allowed_domain, allowed_users = get_access_config()

    email = email.lower().strip()

    if mode == "domain":
        return email.endswith(f"@{allowed_domain}")

    if mode == "allowlist":
        return email in allowed_users

    return False


def get_logged_in_user():
    """
    Vérifie si l'utilisateur est connecté.
    """
    if "user" not in st.session_state:
        return None

    user = st.session_state["user"]
    email = user.get("email", "")

    if is_allowed_user(email):
        return user

    del st.session_state["user"]
    return None


def logout_user():
    """Déconnecte l'utilisateur et nettoie le session_state."""
    if "user" in st.session_state:
        del st.session_state["user"]

    st.rerun()
