# __________________________________________________________________________
# Import Libraries - Importar Librerias.
# __________________________________________________________________________

import os
import logging
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv


# __________________________________________________________________________
# 1.0 Import enviroment variables
# __________________________________________________________________________

load_dotenv()

# __________________________________________________________________________
# 1.1 Import Log Module -  Importar Modulo p. Logs
# __________________________________________________________________________

# Centralized Logging Setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("pipeline.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# __________________________________________________________________________
# SQL Engine Factory - Crear Motor p. SQL
# __________________________________________________________________________

def get_engine(db_name="GRUPO_OLIVER"):
    """Create a SQLAlchemy engine using environment variables."""
    server = os.getenv("DB_SERVER")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    
    url = f"mssql+pyodbc://{user}:{password}@{server}/{db_name}?driver=ODBC+Driver+17+for+SQL+Server"
    return create_engine(url, pool_pre_ping=True)

# __________________________________________________________________________
# Export - Leer Tabla Fuente.
# __________________________________________________________________________

def load_table(df: pd.DataFrame, dest_table: str, engine) -> None:
    """Upsert DataFrame into destination table."""
    try:
        df_existing = pd.read_sql_query(f"SELECT * FROM [dbo].[{dest_table}]", engine)
        if not df.equals(df_existing):
            logger.info(f"[{dest_table}] Updating data... ({len(df)} rows)")
            df.to_sql(dest_table, con=engine, if_exists="replace", index=False)
        else:
            logger.info(f"[{dest_table}] No updates required.")
    except Exception:
        logger.info(f"[{dest_table}] Table not found. Creating with {len(df)} rows...")
        df.to_sql(dest_table, con=engine, if_exists="replace", index=False)
