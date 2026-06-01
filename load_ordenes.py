import pandas as pd
import config as cf
from utils import logger, get_engine, load_table

def transform(df: pd.DataFrame, company: str) -> pd.DataFrame:
    df = df.copy()
    df["Compania"] = company
    df["UltimaActualizacion"] = pd.Timestamp.now()
    
    col_map = {
        'Document': 'Documento', 'OrderNumber': 'OrdenNum', 'OrderDate': 'FechaOrden',
        'CustomerCode': 'CodigoCliente', 'LineTotal': 'Valor', 'Comments': 'Comentarios',
        'QuoteStatus': 'StatusOrden'
    }
    return df.rename(columns=col_map)

def run():
    target_engine = get_engine("GRUPO_EXPORT")
    for key, db in cf.bases_datos.items():
        dest_table = f"Ordenes_{key}"
        logger.info(f"\nProcessing Ordenes: {db} -> {dest_table}")

        try:
            df_raw = cf.get_mock_ordenes()
            df_clean = transform(df_raw, key)
            load_table(df_clean, dest_table, target_engine)
        except Exception as exc:
            logger.error(f"  ERROR processing {db}: {exc}")
