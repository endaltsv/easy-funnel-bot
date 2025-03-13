from dotenv import load_dotenv
import os.path

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
ADMIN_ID = os.getenv("ADMIN_ID", "")


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.path.join(BASE_DIR, "..", "database")
DATABASE_PATH = os.path.join(DB_DIR, "database.db")


DATABASE_URL = f"sqlite+aiosqlite:///{DATABASE_PATH}"
