import pandas as pd
import config as cf
from utils import logger, get_engine, load_table

def transform(df: pd.DataFrame, company: str) -> pd.DataFrame:
    df = df.copy()
    df["Compania"] = company
    df["UltimaActualizacion"] = pd.Timestamp.now()
    return df

def run():
    target_engine = get_engine("GRUPO_DRINKS")
    for key, db in cf.bases_datos.items():
        dest_table = f"Cashflow_{key}"
        logger.info(f"\nProcessing Cashflow: {db} -> {dest_table}")

        try:
            df_raw = cf.mock_cashflow()
            df_clean = transform(df_raw, key)
            load_table(df_clean, dest_table, target_engine)
        except Exception as exc:
            logger.error(f"  ERROR processing {db}: {exc}")
