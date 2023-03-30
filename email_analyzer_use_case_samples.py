"""
This module demonstrates the usage of the EmailAnalyzer class to analyze email files.
The sample use cases include processing email files without attachments, email files with attachments,
and a directory containing email files with and without attachments.

Author: S S R C Kashyap
Email: 1kasyap97@gmail.com
Reviewer: Daniel Caffrey
Email: dcaffrey@topsec.com
"""


import json
from email_analyzer import EmailAnalyzer


def email_file_with_no_attachments(email_file_path: str):
    mail_analyzer = EmailAnalyzer(email_file_path)
    mail_content = mail_analyzer.get_email_from_path()
    processed_mail = mail_analyzer.parse_email(raw_email=mail_content)

    metrics = mail_analyzer.get_email_metrics(parsed_email=processed_mail)
    formatted_output = json.dumps(metrics, indent=4)
    print(f'\nUse Case - 1 output:\n'
          f'The Email Metrics for .eml file without attachments as follows:\n {formatted_output}')


def email_file_with_attachments(email_file_path: str):
    mail_analyzer = EmailAnalyzer(email_file_path)
    mail_content = mail_analyzer.get_email_from_path()
    processed_mail = mail_analyzer.parse_email(raw_email=mail_content)

    metrics = mail_analyzer.get_email_metrics(parsed_email=processed_mail)
    formatted_output = json.dumps(metrics, indent=4)
    print(f'\nUse Case - 2 output:\n'
          f'The Email Metrics for .eml file with attachments as follows:\n {formatted_output}')


def directory_containing_email_files_with_and_without_attachments(dir_path: str):
    mail_analyzer = EmailAnalyzer(dir_path)
    mail_content = mail_analyzer.get_email_from_path()
    processed_mail = mail_analyzer.parse_email(raw_email=mail_content)

    metrics = mail_analyzer.get_email_metrics(parsed_email=processed_mail)
    formatted_output = json.dumps(metrics, indent=4)
    print(f'\nUse Case - 3 output:\n'
          f'The Metrics when directory path is given as input path:\n {formatted_output}')


if __name__ == '__main__':
    directory_path = 'C:/Users/kashyap/PycharmProjects/top_sec_email_analyzer/assets'
    plain_email_file_path = 'assets/email-plain-text.eml'
    email_with_attachments_path = 'assets/email-with-attachments.eml'

    # Analyze and print metrics for an email file without attachments
    email_file_with_no_attachments(email_file_path=plain_email_file_path)

    # Analyze and print metrics for an email file with attachments
    email_file_with_attachments(email_file_path=email_with_attachments_path)

    # Analyze and print metrics for a directory containing email files with and without attachments
    directory_containing_email_files_with_and_without_attachments(dir_path=directory_path)
