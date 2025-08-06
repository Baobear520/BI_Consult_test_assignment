from typing import Any, Dict

from task_3.config.settings import DB_CONFIG


def check_db_config(params: Dict[str, Any] = DB_CONFIG) -> Dict[str, Any]:
    """Load database connection parameters from environment variables."""
    required_params = ("host", "port", "dbname", "user", "password")
    missing_params = [
        param for param in required_params if param not in params
    ]
    if missing_params:
        raise ValueError(
            f"Missing required database parameters: {', '.join(missing_params)}"
            f"Please check your environment variables."
        )

    return params