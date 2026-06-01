import pandas as pd
import config as cf
from utils import logger, get_engine, load_table

def transform(df: pd.DataFrame, company: str) -> pd.DataFrame:
    df = df.copy()
    df["Compania"] = company
    df["UltimaActualizacion"] = pd.Timestamp.now()

    # Vectorized Fuzzy Matching
    df["ClienteNombre"] = df["CardName"].apply(
        lambda x: cf.fuzzy_match(x, list(cf.client_name.keys()))
    ).map(cf.client_name).fillna(df["CardName"]).str.title()

    df["GrupoCliente"] = df["CustomerGroup"].apply(
        lambda x: cf.fuzzy_match(x, list(cf.grupo_cliente.keys()))
    ).map(cf.grupo_cliente).fillna(df["CustomerGroup"]).str.title()

    if company == 'Oliver':
        df["Pais_corregido"] = df["Country"].map(cf.pais_corregido_export).fillna(df["Pais"])

    return df

def run():
    target_engine = get_engine("GRUPO_EXPORT")
    for key, db in cf.bases_datos.items():
        dest_table = f"Clientes_{key}"
        logger.info(f"\nProcessing Clientes: {db} -> {dest_table}")

        try:
            df_raw = cf.mock_clientes() 
            df_clean = transform(df_raw, key)
            load_table(df_clean, dest_table, target_engine)
        except Exception as exc:
            logger.error(f"  ERROR processing {db}: {exc}")
