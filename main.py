import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from bson import ObjectId
from datetime import datetime

from database import db, create_document, get_documents
from schemas import Department, Faculty, Event, Notice, ContactMessage

app = FastAPI(title="School Management API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "School Management API is running"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    return response

# Utility to convert ObjectId to string in lists

def serialize_docs(docs):
    out = []
    for d in docs:
        d = dict(d)
        if d.get("_id"):
            d["_id"] = str(d["_id"])  # type: ignore
        out.append(d)
    return out

# Public content endpoints

@app.get("/departments")
async def list_departments(limit: Optional[int] = 50):
    docs = get_documents("department", {}, limit)
    return serialize_docs(docs)

@app.post("/departments")
async def create_department(payload: Department):
    _id = create_document("department", payload)
    return {"inserted_id": _id}

@app.get("/faculty")
async def list_faculty(limit: Optional[int] = 100, department: Optional[str] = None):
    filt = {"department": department} if department else {}
    docs = get_documents("faculty", filt, limit)
    return serialize_docs(docs)

@app.post("/faculty")
async def create_faculty(payload: Faculty):
    _id = create_document("faculty", payload)
    return {"inserted_id": _id}

@app.get("/events")
async def list_events(limit: Optional[int] = 20, upcoming: Optional[bool] = True):
    filt = {}
    if upcoming:
        filt = {"date": {"$gte": datetime.utcnow()}}
    docs = get_documents("event", filt, limit)
    return serialize_docs(docs)

@app.post("/events")
async def create_event(payload: Event):
    _id = create_document("event", payload)
    return {"inserted_id": _id}

@app.get("/notices")
async def list_notices(limit: Optional[int] = 20):
    docs = get_documents("notice", {}, limit)
    return serialize_docs(docs)

@app.post("/notices")
async def create_notice(payload: Notice):
    _id = create_document("notice", payload)
    return {"inserted_id": _id}

@app.post("/contact")
async def submit_contact(payload: ContactMessage):
    _id = create_document("contactmessage", payload)
    return {"message": "Received", "inserted_id": _id}


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
