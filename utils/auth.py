import streamlit as st

# Récupération des secrets selon ton format exact
CLIENT_ID = st.secrets["auth"]["client_id"]
CLIENT_SECRET = st.secrets["auth"]["client_secret"]
REDIRECT_URI = st.secrets["auth"]["redirect_uri"]
AUTHORIZATION_URL = "https://accounts.google.com/o/oauth2/v2/auth" # Déduit de ton metadata_url

def get_login_url():
    """Construit l'URL d'autorisation Google."""
    # Tu utilises ici ta librairie OAuth ou une simple construction de string
    # Exemple simplifié :
    scope = "openid email profile"
    return f"{AUTHORIZATION_URL}?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope={scope}"

def get_logged_in_user():
    """
    Vérifie si l'utilisateur est connecté (ex: check dans st.session_state).
    Gère également l'interception du paramètre '?code=' dans l'URL après la redirection.
    """
    # if "user" in st.session_state:
    #     return st.session_state["user"]
    if "user" in st.session_state:

        user = st.session_state["user"]

    if is_allowed_user(user["email"]):
        return user

    del st.session_state["user"]
    return None

    # Logique pour intercepter le code depuis les query params et récupérer le token...
    # query_params = st.query_params
    # if "code" in query_params: ...

    return None

def logout_user():
    """Déconnecte l'utilisateur et nettoie le session_state."""
    if "user" in st.session_state:
        del st.session_state["user"]
    st.rerun()

def get_access_config():
    access = st.secrets.get("access", {})

    mode = access.get("mode", "domain").lower()
    allowed_domain = access.get("allowed_domain", "").lower()
    allowed_users = {
        email.lower() for email in access.get("allowed_users", [])
    }

    return mode, allowed_domain, allowed_users

def is_allowed_user(email: str) -> bool:

    mode, allowed_domain, allowed_users = get_access_config()

    email = email.lower().strip()

    if mode == "domain":
        return email.endswith(f"@{allowed_domain}")

    if mode == "allowlist":
        return email in allowed_users

    return False
