from dotenv import load_dotenv
import os

UPLOAD_PATH = 'static/'
MODEL_NAME = "gemini-1.5-flash"

load_dotenv()

class Utils:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", os.getenv("GOOGLE_API_KEY"))
    UPLOAD_DIR = "files"
    OUTPUT_DIR = "outputs"
    MODEL_NAME = "gemini-1.5-flash"

utils = Utils()
