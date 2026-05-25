import re
import unicodedata
import pandas as pd


def normalize_colname(col: str) -> str:
    col = str(col).strip().lower()
    col = unicodedata.normalize("NFKD", col).encode("ascii", "ignore").decode("utf-8")
    col = re.sub(r"[^a-z0-9]+", "_", col)
    return col.strip("_")


def make_unique_columns(columns):
    seen = {}
    unique_cols = []

    for col in columns:
        base = normalize_colname(col)

        if base not in seen:
            seen[base] = 0
            unique_cols.append(base)
        else:
            seen[base] += 1
            unique_cols.append(f"{base}_{seen[base]}")

    return unique_cols


def normalize_text(value):
    if value is None:
        return None

    if isinstance(value, float) and pd.isna(value):
        return None

    value = str(value).strip()
    value = value.replace("–", "-")
    value = value.replace("—", "-")
    value = re.sub(r"\s+", " ", value)

    return value if value else None


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Important : éviter les noms de colonnes dupliqués
    df.columns = make_unique_columns(df.columns)

    # Nettoyage uniquement colonne par colonne, en évitant les doublons
    object_cols = df.select_dtypes(include=["object"]).columns

    for col in object_cols:
        df[col] = df[col].map(normalize_text)

    return df
