from rapidfuzz import process, fuzz

# Databases and Companies
db_go = 'GRUPO OLIVER'
bases_datos = {"Oliver": "DB_OLIVER_OLIVER", "Rones": "DB_RONES", "Bodegas": "DB_BODEGAS_PEDRO"}
compania = ["Oliver", "Rones", "Bodegas"]

def fuzzy_match(value, choices):
    if not value: return None
    match = process.extractOne(value, choices, scorer=fuzz.partial_ratio)
    return match[0] if match and match[1] >= 80 else None

# ─────────────────────────────────────────────
# SQL Queries (Truncated for brevity, keep your existing SELECT statements)
# ─────────────────────────────────────────────
def sql_productos(value):
    return f"SELECT [ItemCode] as 'CodigoSAP'... FROM {value}.[dbo].[OITM]"

def sql_ventas(value):
    return f"SELECT T3.NAME AS 'Pais'... FROM {value}.[dbo].OINV T0..."

def sql_ordenes(value):
    return f"SELECT 'Order' AS Document... FROM {value}.[dbo].ORDR T0..."

# Keep your dicts here (productos_dict, client_name, grupo_cliente, etc.)
