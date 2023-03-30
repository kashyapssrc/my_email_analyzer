"""
Module: custom_email_analyzer_exceptions.py

This module defines custom exception classes for the email_analyzer module. These exceptions provide
specific error messages related to email file path validation and attachment processing. The logger
from the log_config module is used to log error messages.

Author: S S R C Kashyap
Email: 1kasyap97@gmail.com
Reviewer: Daniel Caffrey
Email: dcaffrey@topsec.com
"""

from .log_config import logger


class InvalidPathError(Exception):
    """
    InvalidPathError is raised when the provided path is not in the correct format.
    """
    def __init__(self, path: str, message: str = None):
        if message is None:
            message = f"Invalid path: '{path}'. Please check the provided path and ensure it is in the correct format " \
                      f"'/path_to_file/filename.eml'"
        logger.error(message)
        super().__init__(message)


class NotEmailFileError(Exception):
    """
    NotEmailFileError is raised when the provided file is not an email file (.eml).
    """
    def __init__(self, file_path: str, message: str = None):
        if message is None:
            message = f"Invalid email file path: '{file_path}'. Provided file is not an email file (.eml)"
        logger.error(message)
        super().__init__(message)


class NoEmailFilesInDirectoryError(Exception):
    """
    NoEmailFilesInDirectoryError is raised when the provided directory does not contain any EML files.
    """
    def __init__(self, directory_path: str, message: str = None):
        if message is None:
            message = f"Invalid path: '{directory_path}'. Directory does not contain any EML files."
        logger.error(message)
        super().__init__(message)


class AttachmentProcessingError(Exception):
    """
    AttachmentProcessingError is raised when there is an error processing an email attachment.
    """
    def __init__(self, attachment_name: str, message: str = None):
        if message is None:
            message = f"Error processing attachment '{attachment_name}'. Please check the file and try again."
        logger.error(message)
        super().__init__(message)
