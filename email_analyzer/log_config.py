"""
Module: log_config.py

This module configures the logger for the email_analyzer package. It sets the logging level, format,
and the file where logs will be saved. This configuration allows for consistent and centralized
logging throughout the project.

Author: S S R C Kashyap
Email: 1kasyap97@gmail.com
Reviewer: Daniel Caffrey
Email: dcaffrey@topsec.com
"""

import logging

# Configure the logger
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='./email_analyzer_logs.log')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Additional developer comments:
# - The logging level is set to INFO by default, which includes INFO, WARNING, ERROR, and CRITICAL levels to be logged.
# - The log format includes the timestamp, log level, and the log message.
# - Logs are saved to the email_analyzer_logs.log file in the same directory as the log_config module.