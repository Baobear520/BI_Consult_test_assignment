"""Main ETL process execution script."""
import logging
from .extractor import FakeStoreAPI
from .transformer import FakeStoreDataTransformer
from .database import PostgresDriver    

logger = logging.getLogger(__name__)


def main():
    """Execute the ELT process."""
    try:
        # Initialize components
        api_client = FakeStoreAPI()
        db_driver = PostgresDriver()
        transformer = FakeStoreDataTransformer(db_driver)
        
        # Create database tables
        logger.info("Creating database tables...")
        transformer.create_tables(sql_file="create_tables.sql")

        # Extract data
        logger.info("Extracting data from FakeStore API...")
        products = api_client.fetch_data("products")
        users = api_client.fetch_data("users")

        # Load raw data
        logger.info("Loading raw data into database...")
        transformer.load_products(sql_file="insert_product.sql", data=products)
        transformer.load_users(sql_file="insert_user.sql", data=users)

        # Transform data
        logger.info("Transforming data...")
        transformer.transform_most_expensive(sql_file="transform_most_expensive.sql")
        transformer.transform_ods_users(sql_file="transform_ods_users.sql")

        logger.info("ETL process completed successfully")

    except Exception as e:
        logger.error(f"ETL process failed: {str(e)}")
        raise


if __name__ == "__main__":
    main()
