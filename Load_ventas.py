# __________________________________________________________________________
# Import - Importar Librerias.
# __________________________________________________________________________


import pandas as pd
import config as cf
from utils import get_engine, load_table, logger

# __________________________________________________________________________
# Engine Factory - Conexiones Compartidas.
# __________________________________________________________________________

def export_table(x: int, db: str, engine) -> pd.DataFrame:
    df = pd.read_sql_query(cf.sql_ventas(db), engine)    
    df['Compania'] = cf.compania[x]
    return df 

# __________________________________________________________________________
# Transform - Modificar tablas para carga.
# __________________________________________________________________________

def transform(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["UltimaActualizacion"] = pd.Timestamp.now()
    
    df = df[['Compania','Codigo', 'Fecha', 'Invoice Number',
             'Currency Exchange', 'Código', 'Precio de Articulo',
             'Cantidad Total', 'Monto Total', 'Costo', 'Net Revenue', 'Comments']]
             
    df.columns = ['Compania','Codigo', 'Fecha', 'FacturaNum',
                  'Tasa Cambio', 'Código', 'Precio Articulo',
                  'Cantidad', 'Valor', 'Costo', 'Net Revenue', 'Comentarios']
    return df

# __________________________________________________________________________
# Load - Carga Tabla a SQL Server.
# __________________________________________________________________________

def run():
    target_engine = get_engine("GRUPO_DRINKS")
    
    for x, (key, db) in enumerate(cf.bases_datos.items()):
        dest_table = f"Ventas_{key}"
        logger.info(f"\nProcessing: {db} -> {dest_table}")

        try:
            source_engine = get_engine(db)
            df_raw = export_table(x, db, source_engine)
            df_clean = transform(df_raw)
            load_table(df_clean, dest_table, target_engine)
        except Exception as exc:
            logger.error(f"ERROR processing {db}: {exc}")
            
if __name__ == "__main__":
    run()
