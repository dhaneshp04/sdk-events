from fastapi import FastAPI, Request
from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client["cdp"]
sdk_events = db["sdk_events"]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to your domain later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/sdk/collect")
async def collect_anything(request: Request):
    try:
        data = await request.json()
    except Exception:
        raw = await request.body()
        try:
            decoded = raw.decode("utf-8")
            data = {"_raw_string": decoded}
        except:
            data = {"_raw_bytes": str(raw)}

    data["_received_at"] = datetime.utcnow()
    sdk_events.insert_one(data)
    print("📩 SDK Data Stored:", data)
    return {"status": "ok", "message": "Stored"}
