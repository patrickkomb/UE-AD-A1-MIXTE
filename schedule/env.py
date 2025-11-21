import os
from dotenv import load_dotenv
from pathlib import Path

# Load .env.local if it exists (when microservice running locally)
env_local = Path(__file__).resolve().parents[1] / ".env.local"
if env_local.exists():
    load_dotenv(env_local)

SCHEDULE_SERVICE_URL = os.getenv("SCHEDULE_SERVICE_URL", "localhost:3202")
MOVIES_SERVICE_URL = os.getenv("MOVIES_SERVICE_URL", "http://localhost:3200/graphql")
USE_MONGO = os.getenv("USE_MONGO", "false").lower() == "true"
MONGO_URL = os.getenv("MONGO_URL", "mongodb://root:example@localhost:27017/cinema?authSource=admin")
