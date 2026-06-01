import pandas as pd
import datetime as dt
from utils import logger, get_engine, load_table

def create_calendar_df(start_date: str, end_date: str) -> pd.DataFrame:
    df = pd.DataFrame({"Fecha": pd.date_range(start=start_date, end=end_date, freq="D")})
    df["Anio"] = df["Fecha"].dt.year
    df["Mes"] = df["Fecha"].dt.month
    df["DiaSemana"] = df["Fecha"].dt.weekday + 1
    
    _MESES = {1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio", 
              7: "Julio", 8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"}
    
    df["Anio-Mes"] = df["Anio"].astype(str) + "-" + df["Mes"].astype(str).str.zfill(2)
    df["NombreMes"] = df["Mes"].map(_MESES)
    df["EsFinDeSemana"] = df["DiaSemana"].isin([6, 7])
    df["EsDiaLaboral"] = ~df["EsFinDeSemana"]
    return df

def run():
    start_date = "2022-01-01"
    end_date = f"{dt.datetime.now().year}-12-31"
    target_engine = get_engine("GRUPO_OLIVER")
    
    logger.info(f"\nRunning Calendario pipeline: {start_date} -- {end_date}")
    try:
        df = create_calendar_df(start_date, end_date)
        load_table(df, "Calendario", target_engine)
    except Exception as exc:
        logger.error(f"  ERROR processing Calendario: {exc}")
