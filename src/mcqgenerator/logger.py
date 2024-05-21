import logging
import os
from datetime import datetime

# Generate a log file name with a compatible format
LOG_FILE = f"{datetime.now().strftime('On_date_%Y-%m-%d_at_time_%H-%M-%S')}.log"

# Ensure the 'logs' directory exists
log_path = os.path.join(os.getcwd(), "logs")
os.makedirs(log_path, exist_ok=True)

# Full path for the log file
LOG_FILEPATH = os.path.join(log_path, LOG_FILE)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    filename=LOG_FILEPATH,
    format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s"
)
