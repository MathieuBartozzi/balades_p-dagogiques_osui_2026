from pathlib import Path
import streamlit as st
from utils.loader import load_data
from utils.auth import is_allowed_user
from utils.cleaning import clean_dataframe
from utils.mapping import enrich_dataframe


# Racine du projet = dossier qui contient app.py
BASE_DIR = Path(__file__).resolve().parent

# Dossiers
IMAGES_DIR = BASE_DIR / "images"
PAGES_DIR = BASE_DIR / "pages"

# Fichiers images
LOGO_PRINCIPAL = IMAGES_DIR / "logo_principal.png"
LOGO_SECONDAIRE = IMAGES_DIR / "logo_secondaire.png"

# =========================
# Configuration initiale
# =========================
st.set_page_config(page_title="Dashboard MLF", layout="centered")

title = "Dashboard MLF"

# =========================
# CSS GLOBAL
# =========================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.main-title {
    text-align: center;
    color: #1a5b6e;
    font-size: 38px;
    font-weight: 700;
    margin: 2rem 0;
    letter-spacing: -0.5px;
}

[data-testid="stVerticalBlockBorderWrapper"] > div:nth-child(1) {
    padding: 60px 30px !important;
}

.login-subtitle {
    text-align: center;
    color: #3c4043;
    font-size: 16px;
    margin-bottom: 25px;
}

/* STYLISATION DU BOUTON NATIF ET AJOUT DU LOGO GOOGLE */
div.stButton > button {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    background-color: #f8fafc !important;
    color: #3c4043 !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 8px !important;
    padding: 12px 15px !important;
    font-weight: 500 !important;
    font-size: 15px !important;
    transition: all 0.2s !important;
    height: auto !important;
    position: relative;
}

/* Insertion du logo Google via CSS */
div.stButton > button::before {
    content: "";
    background: url('https://upload.wikimedia.org/wikipedia/commons/c/c1/Google_%22G%22_logo.svg') no-repeat center center;
    background-size: contain;
    width: 18px;
    height: 18px;
    margin-right: 12px;
}

div.stButton > button:hover {
    background-color: #f0f7f9 !important;
    border-color: #1a5b6e !important;
    color: #1a5b6e !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 6px -1px rgba(26, 91, 110, 0.1) !important;
}
</style>
""", unsafe_allow_html=True)

# =========================
# Page d'accueil / login
# =========================
if not st.user.is_logged_in:
    st.markdown(f'<div class="main-title">{title}</div>', unsafe_allow_html=True)

    _, col_mid, _ = st.columns([1, 2, 1])
    with col_mid:
        with st.container(border=True):
            st.markdown(
                '<div class="login-subtitle">Connectez-vous pour continuer</div>',
                unsafe_allow_html=True
            )

            if st.button("Continuer avec Google", use_container_width=True):
                st.login()

            st.markdown("<br>", unsafe_allow_html=True)
            _, col_img, _ = st.columns([0.5, 1, 0.5])
            with col_img:
                # st.image("image.png")
                st.image(str(LOGO_PRINCIPAL))


    st.stop()

# =========================
# Contrôle d'accès allowlist / domaine
# =========================
if not is_allowed_user(st.user.email):
    st.error("Accès refusé : votre compte Google n'est pas autorisé pour cette application.")

    if st.button("Se déconnecter", use_container_width=True):
        st.logout()

    st.stop()

# =========================
# Chargement des données
# =========================
if "df" not in st.session_state:
    with st.spinner("Chargement des données…"):
        df = load_data("file_id", gid_key="gid")

        if df.empty:
            st.warning("Aucune donnée chargée.")
            st.stop()


        #necessaire pour ajuster le mapping
        # st.dataframe(df)
        # st.write(df.columns.to_list())

        df = clean_dataframe(df)
        # st.write(df.columns.to_list())
        df = enrich_dataframe(df)


        st.session_state["df"] = df


# =========================
# Navigation multipage
# =========================
pages = [
    st.Page(
        "pages/dashboard.py",
        title="Dashboard",
        icon=":material/dashboard:",
        default=True,
    ),
    st.Page(
        "pages/analyse_detaillee.py",
        title="Analyse détaillée",
        icon=":material/analytics:",
    ),
]

pg = st.navigation(pages, position="top")

st.logo(str(LOGO_SECONDAIRE), size="large")

# =========================
# Sidebar avec infos utilisateur et bouton de déconnexion
# =========================
with st.sidebar:

    _, col,_=st.columns(3)
    with col:
        st.image(st.user.picture, width=80)

    st.success(f"Bienvenue {st.user.name} 👋")


    st.divider()

    if st.button("Se déconnecter", use_container_width=True):
        st.logout()

# =========================
# Exécution de la page active
# =========================
pg.run()
