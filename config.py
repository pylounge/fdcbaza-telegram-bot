import os
from dotenv import load_dotenv

load_dotenv()

settings = {
    'TOKEN': os.getenv('TELEGRAM_TOKEN'),
    'LOG_FILE': os.getenv('LOG_FILE_PATH'),
    'DOC_URL': os.getenv('DOC_URL')
}
