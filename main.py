import load_calendario
import load_clientes
import load_ordenes
import load_productos
import load_ventas
import load_cashflow
from utils import logger

def update_all_pipelines():
    logger.info("=========================================")
    logger.info("Starting Full Pipeline Update...")
    logger.info("=========================================")
    
    # Execute individual pipelines
    load_ventas.run()
    load_clientes.run()
    load_ordenes.run()
    load_productos.run()
    load_cashflow.run()
    load_calendario.run()
    
    logger.info("=========================================")
    logger.info("Pipeline Update Complete.")
    logger.info("=========================================")

if __name__ == "__main__":
    update_all_pipelines()
