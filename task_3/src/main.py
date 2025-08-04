"""Main ETL process execution script."""
import logging
from extractor import FakeStoreAPI
from transformer import DataTransformer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Execute the ETL process."""
    try:
        # Initialize components
        api_client = FakeStoreAPI()
        transformer = DataTransformer()

        # Create database tables
        logger.info("Creating database tables...")
        transformer.create_tables()

        # Extract data
        logger.info("Extracting data from FakeStore API...")
        products = api_client.get_products()
        users = api_client.get_users()

        # Load raw data
        logger.info("Loading raw data into database...")
        transformer.load_products(products)
        transformer.load_users(users)

        # Transform data
        logger.info("Transforming data...")
        transformer.transform_most_expensive()
        transformer.transform_users()

        logger.info("ETL process completed successfully")

    except Exception as e:
        logger.error(f"ETL process failed: {str(e)}")
        raise

if __name__ == "__main__":
    main()