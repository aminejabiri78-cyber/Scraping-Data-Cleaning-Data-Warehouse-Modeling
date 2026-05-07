from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

def get_engine():
    return create_engine(
        f"postgresql+psycopg2://{os.getenv('USER')}:{os.getenv('PASS')}@"
        f"{os.getenv('HOST')}:{os.getenv('PORT')}/{os.getenv('DB_NAME')}"
    )