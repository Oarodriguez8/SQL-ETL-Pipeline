import pandas as pd
import config as cf
from utils import logger, get_engine, load_table

def transform(df: pd.DataFrame, company: str) -> pd.DataFrame:
    df = df.copy()
    df['Compania'] = company
    df["UltimaActualizacion"] = pd.Timestamp.now()
    
    # Mapping to clean column names
    col_map = {
        'Invoice Number': 'FacturaNum', 'Currency Exchange': 'TasaCambio',
        'Precio de Articulo': 'PrecioArticulo', 'Cantidad Total': 'Cantidad',
        'Monto Total': 'Valor', 'Comments': 'Comentarios'
    }
    df = df.rename(columns=col_map)
    return df

def run():
    target_engine = get_engine("GRUPO_EXPORT")
    for key, db in cf.bases_datos.items():
        dest_table = f"Ventas_{key}"
        logger.info(f"\nProcessing Ventas: {db} -> {dest_table}")

        try:
            # Replace with actual DB pull: df_raw = pd.read_sql(cf.sql_ventas(db), get_engine(db))
            df_raw = cf.mock_ventas() 
            df_clean = transform(df_raw, key)
            load_table(df_clean, dest_table, target_engine)
        except Exception as exc:
            logger.error(f"  ERROR processing {db}: {exc}")
