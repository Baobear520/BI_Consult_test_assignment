# Sales Data ETL System

This project implements an ETL (Extract, Transform, Load) system for analyzing sales data from the FakeStore API.

## Features

- Data extraction from FakeStore API (products and users)
- PostgreSQL database integration
- Data transformations including:
  - Top 10 most expensive products analysis
  - User data normalization

## Prerequisites

- Python 3.8+
- PostgreSQL database
- pip (Python package manager)

## Installation

1. Clone the repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure environment variables:
   - Create a `.env` file in the `config/` directory with the following content:
     ```env
     DB_HOST=localhost
     DB_PORT=5432
     DB_NAME=your_db_name
     DB_USER=your_db_user
     DB_PASSWORD=your_db_password
     API_BASE_URL=https://fakestoreapi.in/api
     ```
   - Replace the values as needed for your environment.

### About `settings.py`

The `config/settings.py` file is responsible for loading configuration values for the project. It uses the `python-dotenv` package to load environment variables from the `.env` file located in the `config/` directory. These variables are used to configure the database connection and API access. The API configuration settings (timeout, retry attempts) you can adjust by editing them in the `settings.py`.

## Usage

Run the ETL process from the `task_3` directory:

```bash
python src/main.py
```

## How the ETL Flow Works

The ETL (Extract, Transform, Load) process in this project is orchestrated by the `src/main.py` script and consists of the following steps:

1. **Preparation**

   - The system ensures that the necessary database tables exist by running the `create_tables.sql` script.

2. **Extraction**

   - Data is fetched from the FakeStore API for both products and users using the `FakeStoreAPI` class.

3. **Loading**

   - The extracted product and user data is loaded into the PostgreSQL database using the `insert_product.sql` and `insert_user.sql` scripts.

4. **Transformation**

   - Data transformations are performed by executing SQL scripts:
     - `transform_most_expensive.sql`: Analyzes and stores the top 10 most expensive products.
     - `transform_ods_users.sql`: Normalizes and processes user data for further analysis.

5. **Error Handling**
   - The process includes robust error handling for API and database connection issues, as well as data validation errors. Errors are logged for troubleshooting.

The entire flow is managed by the `FakeStoreETLProcess` class, which implements the ETL steps and is executed when you run `main.py`.

## Interfaces

The project uses interface classes (abstract base classes) defined in `src/interfaces.py` to ensure a modular and extensible ETL architecture. These interfaces include:

- **ETLProcess**: Defines the structure for ETL processes, requiring methods for preparation, extraction, loading, transformation, and running the process.
- **ExtractorInterface**: Specifies the contract for data extraction classes (e.g., fetching data from APIs).
- **TransformerInterface**: Specifies the contract for data transformation classes (e.g., processing and transforming raw data).
- **DatabaseInterface**: Specifies the contract for database interaction classes (e.g., connecting, executing queries, loading data).

By using these interfaces, the project allows for easy extension or replacement of components (such as swapping out the API source or database backend) while maintaining a clear and consistent structure.

## Project Structure

```
├── config/          # Configuration files (.env, settings.py, utils.py)
├── sql/             # SQL scripts for table creation, data insertion, and transformation
├── src/             # Python source code (ETL logic, database, API, transformation)
└── README.md        # Project documentation
```

## Error Handling

The system includes error handling for:

- API connection issues
- Database connection problems
- Data validation errors
