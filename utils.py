import os
import logging
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

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

def get_engine(db_name="GRUPO_OLIVER"):
    """Create a SQLAlchemy engine using environment variables."""
    server = os.getenv("DB_SERVER", "localhost")
    user = os.getenv("DB_USER", "admin")
    password = os.getenv("DB_PASSWORD", "admin")
    
    # Standard connection string (adjust driver if needed)
    url = f"mssql+pyodbc://{user}:{password}@{server}/{db_name}?driver=ODBC+Driver+17+for+SQL+Server"
    
    # For testing without a real DB, you can use SQLite:
    # url = f"sqlite:///{db_name}.db" 
    return create_engine(url, pool_pre_ping=True)

def load_table(df: pd.DataFrame, dest_table: str, engine) -> None:
    """Upsert DataFrame into destination table."""
    try:
        df_existing = pd.read_sql_query(f"SELECT * FROM [dbo].[{dest_table}]", engine)
        
        # Simple delta check
        if not df.equals(df_existing):
            logger.info(f"  [{dest_table}] Updating table with {len(df)} rows.")
            df.to_sql(dest_table, con=engine, if_exists="replace", index=False)
        else:
            logger.info(f"  [{dest_table}] No updates required.")
    except Exception:
        # Table doesn't exist yet
        logger.info(f"  [{dest_table}] Table not found. Creating with {len(df)} rows.")
        df.to_sql(dest_table, con=engine, if_exists="replace", index=False)
