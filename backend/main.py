from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import database

app = FastAPI()
category = None

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

@app.get("/info")
async def root():
    conn = database.get_db_connection()
    items = conn.execute('SELECT * FROM win_prog').fetchall()
    conn.close()
    data = [dict(item) for item in items]
    return data

@app.get("/categories")
async def categories():
    conn = database.get_db_connection()
    items = conn.execute('SELECT category FROM win_prog').fetchall()
    print(items)
    conn.close()
    data = sorted(set(str(item['Category']) for item in items))
    return data