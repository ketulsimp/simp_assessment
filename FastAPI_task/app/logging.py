import logging

logger = logging.Logger()
file_handler = logging.FileHandler(filename = 'log.log')
logger.addHandler(file_handler)

def send_upstock_logs(product_id,increase_by):
    logger.info(f"{product_id} stock has been increased by {increase_by}")
    
def send_restock_logs(product_id,increase_by):
    logger.info(f"{product_id} stock has been decreased by {increase_by}")