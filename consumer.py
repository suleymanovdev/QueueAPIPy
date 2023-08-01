from rabbitmq_methods import connect_to_rabbitmq
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Starting consumer service...")
    connect_to_rabbitmq()
