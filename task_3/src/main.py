"""Main ETL process execution script."""
import logging
from task_3.src.extractor import FakeStoreAPI
from task_3.src.transformer import FakeStoreDataTransformer
from task_3.src.database import PostgresDriver  
from task_3.src.interfaces import ETLProcess


logger = logging.getLogger(__name__)


class FakeStoreETLProcess(ETLProcess):
    def __init__(self, api_client: FakeStoreAPI, db_driver: PostgresDriver, transformer: FakeStoreDataTransformer):
        super().__init__(api_client, db_driver, transformer)

    def prepare(self):
        """Prepare the ETL process."""
        self.transformer.run_sql_file(sql_file="create_tables.sql")

    def extract(self):
        """Extract the data."""
        products = self.api_client.fetch_data("products")
        users = self.api_client.fetch_data("users")
        return products, users

    def load(self, products, users):
        """Load the data."""
        self.transformer.load_products(sql_file="insert_product.sql", data=products)
        self.transformer.load_users(sql_file="insert_user.sql", data=users)

    def transform(self):
        """Transform the data."""
        self.transformer.run_sql_file(sql_file="transform_most_expensive.sql")
        self.transformer.run_sql_file(sql_file="transform_ods_users.sql")

    def run(self):
        """Run the ETL process."""
        self.prepare()
        products, users = self.extract()
        self.load(products, users)
        self.transform()


def main():
    """Execute the ELT process."""
    try:
        api_client = FakeStoreAPI()
        db_driver = PostgresDriver()
        transformer = FakeStoreDataTransformer(db_driver)
        etl_process = FakeStoreETLProcess(api_client, db_driver, transformer)
        
        etl_process.run()
        logger.info("ETL process completed successfully")

    except Exception as e:
        logger.error(f"ETL process failed: {str(e)}")
        raise


if __name__ == "__main__":
    main()
