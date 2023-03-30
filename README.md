# Task Created using Python 3

**Requirements:** Create a python module that another developer can import, which allows them to take the text of an email (2 samples provided as files in the zip attached) and returns a result which gives them Subject, Message-ID, From Address, Total Size of Message and a flag which indicates if any attachments exist in the message.

## Features

- Can process single or multiple email files (EML format)
- Identify attachments and their file types
- Extract email metrics such as Subject, Message ID, From Address, and Total Message Size
- Check for the presence of attachments and their file types
- Easy to use

## Project Structure

- **top_sec_email_analyzer:** Main project directory.
- **email_analyzer:** Python module directory.
  - **__init__.py:** Initializes the module.
  - **email_analyzer.py:** Contains the main code for analyzing email files.
  - **log_config.py:** Provides logging configuration.
  - **custom_exceptions.py:** Defines custom exceptions for the module.
- **assets:** Directory containing email files for testing.
- **email_analyzer_use_case_samples.py:** Contains sample use cases for the module.
- **requirements.txt:** Specifies the required Python packages and their versions.
- **README.md:** Provides project documentation.

## Installation

1. Clone the repository:

```git clone https://github.com/ssrckashyap/top_sec_email_analyzer.git```


2. Change the working directory:

```cd top_sec_email_analyzer```


3. (Optional) Create a virtual environment:

```python -m venv venv```


4. Activate the virtual environment:

- For Windows:

```venv\Scripts\activate```

- For macOS/Linux:

```source venv/bin/activate```


5. Install the required dependencies:

```pip install -r requirements.txt```


## Usage

To use the Email Analyzer module, you can import it into your Python script and then call the appropriate functions:

```python
from email_analyzer import EmailAnalyzer

# Initialize the EmailAnalyzer object with the email file or directory path
mail_analyzer = EmailAnalyzer(file_or_directory_path)

# Read and parse the email(s)
mail_content = mail_analyzer.get_email_from_path()
processed_mail = mail_analyzer.parse_email(raw_email=mail_content)

# Get email metrics
metrics = mail_analyzer.get_email_metrics(parsed_email=processed_mail)
```

## Author
S S R C Kashyap




