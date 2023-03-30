"""
Module: email_analyzer.py

Description: This module provides functionality to analyze email files and extracting the metrics of an email
to gather the relevant information such as if the email has attachments, who is the sender, the email subject, and
Header information. The functionality can handle both single email files and directories containing email files.


Author: S S R C Kashyap
Email: 1kasyap97@gmail.com
Reviewer: Daniel Caffrey
Email: dcaffrey@topsec.com

Task Information: The following code is produced to satisfy the following requirements 'Create a python module that
another developer can import, which allows them to take the text of an email (2 samples provided as files in the zip
attached) and returns a result which gives them Subject, Message-ID, From Address, Total Size of Message and a flag
which indicates if any attachments exist in the message.'
"""

# Import Statements
import os
from email.message import Message
from email.parser import Parser
from pathlib import Path

# Importing Union and List from the typing module to provide type hints for functions that can return multiple types
from typing import Union, List

# Importing python-magic module's to identify the attachment file-type from the email attachments
import magic

# Importing custom exceptions from custom_email_analyzer_exceptions.py to raise proper exception messages
from .custom_email_analyzer_exceptions import InvalidPathError, NotEmailFileError, NoEmailFilesInDirectoryError, \
    AttachmentProcessingError

# importing the initialized logger from log_config.py to use the same logger instance across the package/s
from .log_config import logger


class EmailAnalyzer:
    """
    EmailAnalyzer is a class for analyzing and extracting information from email files (EML format).

    It can handle single email files or a directory containing multiple email files. The class provides methods
    to get the email file from the path provided and read the email contents, parse email headers and body, and
    extract metrics such as subject, sender, attachments, etc.

    Attributes:
        email_file_path (str): The path to the email file or directory containing email files.
    """
    def __init__(self, email_file_path: str):
        """
        Initializes the EmailAnalyzer class with the provided email_file_path.

        Args:
            email_file_path (str): The path to the email file or directory containing email files.
        """

        self._email_file_path = email_file_path

        # flags to check if the path provided is a file or a directory
        self._is_file: bool = False
        self._is_dir: bool = False

        # To store multiple raw emails if the input path is a directory
        self._multiple_raw_emails: list = []
        # To store the parsed email file in the form of Message type if input is a single email file
        self._parsed_email: Message = None
        # Store a list of parsed email Message objects for multiple email files
        self._multiple_parsed_emails: list = []
        # Store metrics for the current email item being processed
        self.current_mail_item_metrics: dict = {}
        # Store metrics for all parsed email items
        self.parsed_mail_metrics: dict = {}
        # Store the total size of the email file(s) in bytes
        self._total_email_size = os.path.getsize(self._email_file_path)
        # Flag to check if the email has attachments
        self._has_attachments: bool = False
        # Store the file name of the attachment, if any
        self.__attachment_file_name: str = None
        # Store the detected type of the attachment, if any
        self.__attachment_type: str = None
        # Store the detected types of multiple attachments, if any
        self.__multiple_attachment_types: dict = {}
        # Store attachment-related information, such as presence and type
        self._attachment_information: dict = {}

    def _path_checker(self):
        """
        Validates the email file path or directory containing email files provided in the EmailAnalyzer constructor.
        Checks if the path exists and contains valid email file types (EML files).
        Raises appropriate custom exceptions in case of invalid input.

        Raises:
            InvalidPathError: If the provided path is not a string.
            FileNotFoundError: If the provided path does not exist.
            NotEmailFileError: If the provided path is a file, but not an email (EML) file.
            NoEmailFilesInDirectoryError: If the provided path is a directory, but it does not contain any EML files.
        """

        try:
            # The following 'if' conditions check the file path and validate it, if the provided path is not valid one
            # we log them in a seperate log file using the defined logger and raise exception
            if not isinstance(self._email_file_path, str):
                logger.error("Invalid path")
                raise InvalidPathError(self._email_file_path)

            if not os.path.exists(self._email_file_path):
                logger.error("invalid path")
                raise FileNotFoundError(f"The provided file path does not exist: '{self._email_file_path}'")

            if os.path.isfile(self._email_file_path):
                if self._email_file_path.endswith(".eml"):
                    logger.info(f"Valid email File Path")
                    self._is_file = True  # if the path provided is a file then we are enabling this flag
                else:
                    logger.error(f"Invalid email File Path: Provided file is not an email file")
                    raise NotEmailFileError(file_path=self._email_file_path,
                                            message="Invalid email File Path: Provided file is not an email file")
            elif os.path.isdir(self._email_file_path):
                # Check if the provided path is a directory containing email files
                #  Iterate through the files in the directory and filter out the EML files.
                email_files = [file for file in os.listdir(self._email_file_path) if file.endswith('.eml')]
                if email_files:
                    logger.info("Valid path: Directory containing EML files.")
                    self._is_dir = True  # if the path is a directory then we are enabling the flag

                else:
                    logger.error("Invalid path: Directory does not contain any EML files.")
                    raise NoEmailFilesInDirectoryError(directory_path=self._email_file_path,
                                                       message="Invalid path: Directory does not contain any EML files.")

        except InvalidPathError as err:

            logger.error(err)

        except FileNotFoundError as err:

            logger.error(err)

        except NotEmailFileError as err:

            logger.error(err)

        except NoEmailFilesInDirectoryError as err:

            logger.error(err)

        except Exception as err:

            logger.error(f"An unexpected error occurred: {err}")

    def get_email_from_path(self) -> Union[str, list]:
        """
        This method retrieves raw email data from the given path (single file or directory).

        This method first checks if the provided path is a file or a directory using _path_checker() and enables the
        respective flags _is_file and _is_dir accordingly.

        If it's a file, the method reads and returns the content of the file as a string.
        If it's a directory, it iterates through the email files in the directory, reads their contents,
        and appends them to a list of raw emails, which is then returned.

        Returns:
            Union[str, list]: If a single file is provided, returns raw email content as a string.
                              If a directory is provided, returns a list of raw email contents.
        """
        # Check and validate the provided path (file or directory) using _path_checker().
        self._path_checker()

        if self._is_file:
            # If the path is a single email file, read the file's content and return it as a string.
            with open(self._email_file_path, 'r', encoding='utf-8') as email_file:
                raw_email = email_file.read()
            return raw_email
        elif self._is_dir:
            # If the path is a directory containing email files, iterate through the files,
            # read their contents, and append them to the _multiple_raw_emails list.
            for email_file in os.listdir(self._email_file_path):

                file_path = Path(self._email_file_path) / email_file

                with open(file_path, 'r+', encoding='utf-8') as file:
                    raw_email = file.read()
                self._multiple_raw_emails.append(raw_email)

            # Return the list of raw email contents.
            return self._multiple_raw_emails

    def parse_email(self, raw_email: Union[str, list]) -> Union[Message, List[Message]]:
        """
        Parses raw email data and returns a parsed email object or a list of parsed email objects.

        This method uses the email.parser.Parser class to parse the raw email data.
        If a single raw email is provided (as a string), the method parses and returns it as a Message object.
        If a list of raw emails is provided, it iterates through the list, parses each email, and appends
        the resulting Message objects to a list, which is then returned.

        Args:
            raw_email (Union[str, list]): Raw email data as a string or a list of strings.

        Returns:
            Union[Message, List[Message]]: A parsed email object (Message) if a single email is provided,
                                           or a list of parsed email objects if a list of emails is provided.
        """
        # Initialize the email Parser object.
        email_parser = Parser()
        if isinstance(raw_email, str):
            # If a single raw email is provided, parse it and return the resulting Message object.
            self._parsed_email = email_parser.parsestr(raw_email)
            return self._parsed_email

        else:
            # If a list of raw emails is provided, iterate through the list, parse each email,
            # and append the resulting Message objects to the _multiple_parsed_emails list.
            for raw_email_item in raw_email:
                self._multiple_parsed_emails.append(email_parser.parsestr(raw_email_item))

            # Return the list of parsed email objects (Message instances).
            return self._multiple_parsed_emails

    @staticmethod
    def _identify_attachments(attachment_data: str) -> str:
        """
        Identifies the file type of an attachment using the `python-magic` library and returns a descriptive string.

        This method analyzes the provided attachment data and returns a string describing the identified
        file type. The `magic` library is used to determine the MIME type of the attachment.

        Args:
            attachment_data (str): The file path of the attachment.

        Returns:
            str: A descriptive string indicating the type of the attachment.
        """
        # Use the magic library to determine the MIME type of the attachment.
        file_type = magic.from_file(attachment_data, mime=True)

        # Return a descriptive string based on the identified MIME type.
        if file_type.startswith('text/'):
            return "The attachment seems like a document report"
        elif file_type.startswith('application/pdf'):
            return "The attachment seems like an invoice"
        elif file_type.startswith('image/'):
            return "The attachment seems like an image"
        elif file_type.startswith('audio/'):
            return "The attachment seems like an audio file"
        elif file_type.startswith('application/vnd.ms-excel'):
            return "The attachment seems like a spreadsheet"
        elif file_type.startswith('application/zip'):
            return "The attachment seems like a compressed file"
        elif file_type.startswith('application/octet-stream'):
            return "The attachment seems like a code file"
        else:
            return "The attachment file type is Un-Known"

    def __check_mail_attachments(self, parsed_email: Message) -> dict:
        """
        This private method checks for attachments in a parsed email message, identifies their types,
        and extracts relevant information about them. The method returns a dictionary containing the
        attachment information.

        Args:
            parsed_email (Message): A parsed email object (instance of email.message.Message).

        Returns:
            dict: A dictionary containing attachment information, such as whether the email has
            attachments, the attachment file names, and their types.

        Raises:
            AttachmentProcessingError: If there's an error while processing the email attachments.
        """
        try:
            # Set the default state to no attachments initially
            self._has_attachments = False

            # If the email is a multipart message, iterate through its parts
            if parsed_email.is_multipart():
                for part in parsed_email.walk():

                    # Check if the current part is an attachment
                    if part.get_content_disposition() == 'attachment':
                        self._has_attachments = True
                        self.__attachment_file_name = part.get_filename()
                        attachment_data = part.get_payload(decode=True)

                        # Write the attachment data to a temporary file
                        with open(self.__attachment_file_name, 'wb') as attachment_file:
                            attachment_file.write(attachment_data)

                        # Identify the attachment type
                        self.__attachment_type = self._identify_attachments(self.__attachment_file_name)
                        self.__multiple_attachment_types[self.__attachment_file_name] = self.__attachment_type

                        # Update the attachment information dictionary
                        self._attachment_information['Has Attachment'] = self._has_attachments
                        self._attachment_information['Attachment File Name'] = self.__attachment_file_name
                        self._attachment_information['Attachment File Type'] = self.__attachment_type

                        # Remove the temporary attachment file
                        os.remove(self.__attachment_file_name)

                        return self._attachment_information

            else:
                # If the email is not a multipart message, it has no attachments
                self._has_attachments = False
                self._attachment_information['Has Attachment'] = self._has_attachments
            return self._attachment_information

        except AttachmentProcessingError as attachment_error:
            # Log any attachment processing errors
            logger.error(attachment_error)

    def get_email_metrics(self, parsed_email: Union[Message, List[Message]]) -> dict:
        """
        This method extracts metrics from the parsed email(s), such as subject, message ID, from address,
        total message size, and attachment information. It returns a dictionary containing these metrics
        for single or multiple emails.

        Args:
            parsed_email (Union[Message, List[Message]]): A parsed email object or a list of parsed email
                objects (instances of email.message.Message).

        Returns:
            dict: A dictionary containing email metrics, such as subject, message ID, from address,
            total message size, and attachment information.

        """
        # Check if parsed_email is a single email message or a list of messages
        if isinstance(parsed_email, Message):
            # If parsed_email is a single email message, extract the metrics and attachment information
            information = self.__check_mail_attachments(parsed_email=parsed_email)
            self.current_mail_item_metrics['Subject'] = parsed_email['subject']
            self.current_mail_item_metrics['Message ID'] = parsed_email['message-id']
            self.current_mail_item_metrics['From Address'] = parsed_email['from']
            self.current_mail_item_metrics['Total Message Size'] = self._total_email_size

            self.current_mail_item_metrics['Has Attachments'] = information['Has Attachment']
            if self.current_mail_item_metrics['Has Attachments']:
                self.current_mail_item_metrics['Attachment File Name'] = information['Attachment File Name']
                self.current_mail_item_metrics['Attachment File Type'] = information['Attachment File Type']

            self.parsed_mail_metrics[f'Item- 1'] = self.current_mail_item_metrics

            return self.parsed_mail_metrics

        else:
            # If parsed_email is a list of email messages, extract the metrics and attachment information
            # for each message and store it in the parsed_mail_metrics dictionary
            for index, parsed_item in enumerate(parsed_email):
                self.current_mail_item_metrics = {'Subject': parsed_item['subject'],
                                                  'Message ID': parsed_item['message-id'],
                                                  'From Address': parsed_item['from'],
                                                  'Total Message Size': self._total_email_size}

                information = self.__check_mail_attachments(parsed_email=parsed_item)

                self.current_mail_item_metrics['Has Attachments'] = information['Has Attachment']
                if self.current_mail_item_metrics['Has Attachments']:
                    self.current_mail_item_metrics['Attachment File Name'] = information['Attachment File Name']
                    self.current_mail_item_metrics['Attachment File Type'] = information['Attachment File Type']

                self.parsed_mail_metrics[f'Item-{index + 1}'] = self.current_mail_item_metrics

            return self.parsed_mail_metrics
