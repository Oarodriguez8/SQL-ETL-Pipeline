import pandas as pd
import config as cf
from utils import logger, get_engine, load_table

def transform(df: pd.DataFrame, company: str) -> pd.DataFrame:
    df = df.copy()
    df["Compania"] = company
    df["UltimaActualizacion"] = pd.Timestamp.now()
    df["TipoProducto"] = df["CodigoSAP"].str[:2].map(cf.tipoproducto).fillna("Otros")
    
    # In a real scenario, you'd apply your nested dictionary fuzzy logic here
    # For mock purposes, we set dummy categories
    df["Marca"] = "Marca_X"
    df["Sub-Marca"] = "Sub_Y"
    df["Familia"] = "Fam_Z"
    
    if company == "Bodegas":
        df[["Marca", "Sub-Marca", "Familia"]] = None

    return df

def run():
    target_engine = get_engine("GRUPO_EXPORT")
    for key, db in cf.bases_datos.items():
        dest_table = f"Productos_{key}"
        logger.info(f"\nProcessing Productos: {db} -> {dest_table}")

        try:
            df_raw = cf.mock_productos()
            df_clean = transform(df_raw, company=key)
            load_table(df_clean, dest_table, target_engine)
        except Exception as exc:
            logger.error(f"  ERROR processing {db}: {exc}")
