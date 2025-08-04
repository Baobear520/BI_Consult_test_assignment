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

3. Configure database connection:
   - Copy `config/database.ini.example` to `config/database.ini`
   - Update with your database credentials

## Usage

Run the ETL process:
```bash
python src/main.py
```

## Project Structure

```
├── config/          # Configuration files
├── sql/            # SQL scripts
├── src/            # Python source code
└── tests/          # Test files
```

## Error Handling

The system includes error handling for:
- API connection issues
- Database connection problems
- Data validation errors