

 # Grupo Drinks Data Pipeline: Operational Guide & Architecture Overview

This document provides a comprehensive operational guide for executing, maintaining, and scaling the consolidated data pipeline for Grupo_Bebidas. It details the system architecture, step-by-step execution workflows, operational procedures, and strategic recommendations for moving from development/mock stages to enterprise production.

---

## 1. Executive Summary

The Grupo Oliver Data Engineering Pipeline is designed to extract raw operational data from three distinct source databases (`DB_EXPORT`, `DB_LOCAL`, and `DB_SUPPLY`), execute complex data-cleaning transformations, and load the unified results into a centralized staging and reporting repository (`GRUPO_DRINKS`). 

The pipeline addresses several legacy operational challenges:
* **Decentralization:** Consolidates scattered transactional databases into a structured data warehouse schema.
* **Data Inconsistency:** Automatically resolves human error and naming disparities in customer and product entries using advanced fuzzy matching heuristics.
* **Security Vulnerabilities:** Eliminates hardcoded credentials via standard `.env` configuration file isolation.
* **Redundancy (DRY Compliance):** Centralizes connections, logging, and state management into an isolated utility framework (`utils.py`).

---

## 2. Core Architectural Framework

The pipeline utilizes a modular multi-tier ETL (Extract, Transform, Load) model. Instead of relying on a singular monolithic script, individual sub-domains are partitioned into distinct operational files orchestrated by a central executor.

### System Diagram & Flow
1. **Orchestration Layer (`main.py`):** Acts as the main application trigger, sequentializing sub-pipeline execution.
2. **Domain Pipelines (`load_*.py`):** Contain specialized business transformations, data mapping rules, and schema assertions.
3. **Utility & Infrastructure Layer (`utils.py`):** Inherits low-level database pooling parameters, file logging configurations, and idempotent ingestion handlers (`to_sql` updates).
4. **Configuration & Data Layer (`config.py`):** Houses metadata, regex/fuzzy dictionaries, static mappings, and staging query strings.

---

Step 1: Initialization

Execute the master process from the command-line interface or scheduling wrapper:
Bash

```python main.py```

Upon execution, utils.py boots the logger, instantiates a file-writer appender to pipeline.log, and securely reads database coordinates from the environment.
Step 2: Extraction

The orchestrator walks through each registered sub-pipeline sequentially (Ventas -> Clientes -> Ordenes -> Productos -> Cashflow -> Calendario). For each domain, the pipeline connects to the respective source instances defined in config.py (DB_OLIVER_OLIVER, DB_RONES, and DB_BODEGAS_PEDRO) and queries the raw operational tables.

Upon execution, `utils.py` boots the logger, instantiates a file-writer appender to `pipeline.log`, and securely reads database coordinates from the environment.

### Step 3: Extraction

The orchestrator walks through each registered sub-pipeline sequentially (`Ventas` -> `Clientes` -> `Ordenes` -> `Productos` -> `Cashflow` -> `Calendario`). For each domain, the pipeline connects to the respective source instances defined in `config.py` (`DB_EXPORT`, `DB_LOCAL`, and `DB_SUPPLY`), and queries the raw operational tables.

### Step 3: Transformation & Data Harmonization

Dataframes undergo structural changes to normalize outputs across different company entities:

* **Timestamping:** An `UltimaActualizacion` field is injected with the precise current runtime timestamp.
* **Fuzzy Token Harmonization:** Transaction fields are run against dictionaries using `rapidfuzz.process.extractOne` with a token-sorting ratio algorithm. Brand names, sub-brands, and client groups are mapped to uniform naming conventions.
* **Schema Standardization:** Source column naming conventions (Spanish/English mixed schemas, such as `CardCode`, `DocDate`, `TotalSumSy`) are mapped uniformly to a standardized target language schema.

### Step 4: Loading & Idempotence Checks

The pipeline hands dataframes off to the `load_table()` engine within `utils.py`. The framework checks if the table exists:

* **If missing:** The table is constructed from the dataframe schema.
* **If present:** A delta check is computed. If rows or values differ from existing structures, a fresh transactional state is written (`if_exists="replace"`). If data remains structurally equivalent, the operation skips to avoid unnecessary locking or database fragmentation.

---

## 5. Domain Component Deep-Dive

### 5.1 Sales/Invoicing (`load_ventas.py`)

Processes commercial activity from invoices and credit notes (`OINV` and `ORIN`). It aggregates quantities, computes net operational margins, standardizes foreign currency exchanges against the native rate, and isolates terminal product codes (`PT%`).

### 5.2 Customer Relations (`load_clientes.py`)

Extracts master customer ledgers (`OCRD`). It applies dual-tiered token sorting string checks against client mapping tables to group regional clients, flags status parameters (`Activo`/`Inactivo`), and normalizes geographic locations for accurate regional business analytics.

### 5.3 Inventory & Master Items (`load_productos.py`)

Tracks standard material classifications, base pricing matrices, and dimensional attributes (`OITM`). It creates structural brand taxonomies (`Marca`, `Sub-Marca`, `Familia`). For `Bodegas`, it automatically bypasses brand mapping rules since its warehouse items don't follow hierarchical configurations.

### 5.4 Order Logs (`load_ordenes.py`)

Pulls pending order volumes from sales documents (`ORDR` / `RDR1`), tracks overall status structures (`Open`, `Cancelled`, `Closed`), and performs dynamic currency conversion to evaluate order pipelines uniformly in USD.

### 5.5 Cashflow Ledger (`load_cashflow.py`)

Tracks liquid asset velocities across AR collections (`ORCT`), AP accounts (`OVPM`), and standardized bank ledger updates (`OJDT`). It filters non-cash modifications to guarantee clean visibility into liquidity inflows and outflows.

### 5.6 Operational Calendar (`load_calendario.py`)

An automated date-spine matrix generator. It populates dynamic time metrics (`Anio-Mes`, `NombreMes`, `EsFinDeSemana`, `EsDiaLaboral`) through the current year's end, providing a standardized dimension table for date filters and time-series aggregations.

---

## 6. Recommendations & Best Practices

To transition this framework into an enterprise-grade production ecosystem, implement the following engineering enhancements:

### 6.1 Production Code Transition (Crucial Step)

The codebase includes mock-data wrappers within `config.py` for testing and GitHub isolation. **Before publishing to production, modify the data loops.** Replace the testing functions with active SQL query calls:
```python
# Production Extraction Pattern Example
source_engine = get_engine(db)
df_raw = pd.read_sql_query(cf.sql_ventas(db), source_engine)
```


### 6.2 Automation & Scheduling

* **Windows Ecosystem:** Wrap execution in an explicit Batch script (`.bat`) and schedule via **Windows Task Scheduler** to trigger nightly at low-traffic times (e.g., 2:00 AM).
* **Linux / Cloud Transition:** Utilize a lightweight **Cron job** or implement an enterprise orchestrator like **Apache Airflow** or **Prefect** to monitor job dependencies, task retries, and visual execution states.

### 6.3 Performance Optimization & Ingestion Scaling

* **Batch Chunking:** For large historical tables (e.g., millions of historical invoice rows), pass the `chunksize` parameter to `to_sql()` and `read_sql_query()` to manage memory limits:
```python
df.to_sql(dest_table, con=engine, if_exists="replace", chunksize=5000, method="multi")

```


* **Target Engine Indexing:** Since tables are replaced upon structure modification, consider executing a post-load SQL step via SQLAlchemy to reconstruct Clustered/Non-Clustered indexes on primary analytical filtering components like `Fecha`, `CodigoSAP`, or `CardCode`.

### 6.4 Monitoring, Logging & Alerting

* **Centralized Diagnostics:** Expand the error-handling blocks inside `main.py` and individual pipeline wrappers to dispatch email alerts or webhooks (e.g., Slack or Microsoft Teams channels) using Python's `requests` or `smtplib` libraries whenever an unhandled extraction exception or driver dropout halts operations.
* **Log Rotation:** Over continuous production runs, the text-based log file (`pipeline.log`) will expand. Substitute the default logging handler with a `RotatingFileHandler` to automatically partition logs once a file size limit is reached.
"""


```
