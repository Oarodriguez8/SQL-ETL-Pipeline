import pandas as pd
import numpy as np
from rapidfuzz import process, fuzz

(`DB_EXPORT`, `DB_LOCAL`, and `DB_SUPPLY`)

# Databases and Companies
db_go = 'GRUPO_DRINKS'
bases_datos = {"Exportacion": "DB_EXPORT", "Local": "DB_LOCAL", "Bodegas": "DB_SUPPLY"}
compania = ["Export", "Local", "Supply"]

# Mappings
tipoproducto = {"PT": "Producto Terminado", "SV": "Servicios", "BP": "Botellas Producto Terminado"}
grupo_cliente = {'ACCIONISTA': 'ACCIONISTA', 'LOCAL': 'NACIONAL', 'Internacionales': 'INTERNACIONAL'}
pais_corregido = {"C00020": "USA", "C00103": "Czech Republic", "C00097": "Austria"}

# Helper
def fuzzy_match(value, choices, threshold=80):
    if pd.isna(value) or value == "":
        return None
    match = process.extractOne(value, choices, scorer=fuzz.token_sort_ratio)
    return match[0] if match and match[1] >= threshold else None

# ─────────────────────────────────────────────
# Mock Data Generators (Replace with pd.read_sql in production)
# ─────────────────────────────────────────────

def mock_ventas():
    return pd.DataFrame({
        'Codigo': ['C001', 'C002'], 'CardName': ['Inversiones TUNC', 'Local Corp'],
        'Fecha': pd.to_datetime(['2023-10-01', '2023-10-02']),
        'Invoice Number': ['INV-100', 'INV-101'], 'Currency Exchange': [56.5, 1.0],
        'Código': ['PT-100', 'SV-200'], 'Articulo': ['Ron Punta Cana', 'Servicio Embotellado'],
        'Precio de Articulo': [15.0, 50.0], 'Cantidad Total': [100, 5],
        'Monto Total': [1500.0, 250.0], 'Costo': [800.0, 100.0],
        'Net Revenue': [700.0, 150.0], 'Comments': ['Ok', 'Rush']
    })

def mock_clientes():
    return pd.DataFrame({
        'CardCode': ['C001', 'C002'], 'CardName': ['Inversiones TUNC', 'Test Client'],
        'CustomerType': ['C', 'C'], 'validFor': ['Y', 'N'],
        'Address': ['Street 1', 'Street 2'], 'Phone': ['555-1234', '555-9876'],
        'ContactPerson': ['John', 'Jane'], 'Email': ['j@test.com', 'a@test.com'],
        'AccountBalance': [1000.0, 0.0], 'TaxGroup': ['TG1', 'TG2'],
        'CustomerGroup': ['Internacionales', 'LOCAL'], 'PymntConditions': ['Net30', 'Cash'],
        'Country': ['C00020', 'DO'], 'Pais': ['USA', 'Dom Rep'], 'CreateDate': pd.Timestamp.now()
    })

def mock_ordenes():
    return pd.DataFrame({
        'Document': ['Order', 'Order'], 'OrderNumber': [1001, 1002],
        'OrderDate': pd.to_datetime(['2023-10-01', '2023-10-02']),
        'CustomerCode': ['C001', 'C002'], 'CustomerName': ['Client A', 'Client B'],
        'SKU': ['PT-100', 'SV-200'], 'Quantity': [50, 10], 'Price': [20.0, 5.0],
        'LineTotal': [1000.0, 50.0], 'Comments': ['None', 'None'], 'QuoteStatus': ['Open', 'Closed']
    })

def mock_productos():
    return pd.DataFrame({
        'CodigoSAP': ['PT-100', 'SV-200', 'BP-300'],
        'Descripcion': ['Puntacana Club XOX', 'Servicio Generico', 'Botella Vacia']
    })

def mock_cashflow():
    return pd.DataFrame({
        'Date': pd.to_datetime(['2023-10-01', '2023-10-02']),
        'Period': ['2023-10', '2023-10'], 'Flow Type': ['AR Receipt', 'AP Payment'],
        'BP Code': ['C001', 'V001'], 'BP Name': ['Client A', 'Vendor B'],
        'Document No': [5001, 6001], 'Reference': ['REF1', 'REF2'],
        'Bank Account': ['BHD Principal', 'Banreservas'], 'Currency': ['USD', 'DOP'],
        'Amount (Doc)': [1000.0, 500.0], 'Amount (FC)': [1000.0, 0.0],
        'Inflow': [1000.0, 0.0], 'Outflow': [0.0, 500.0], 'Remarks': ['Paid', 'Rent']
    })from rapidfuzz import process, fuzz


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
