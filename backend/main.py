from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import database

app = FastAPI()
category = None
newUser = None
os_c = None

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

@app.get("/info-win")
async def root():
    conn = database.get_db_connection()
    items = conn.execute('SELECT * FROM win_prog').fetchall()
    conn.close()
    data = [dict(item) for item in items]
    return data

@app.get("/info-lin")
async def root():
    conn = database.get_db_connection()
    items = conn.execute('SELECT * FROM lin_prog').fetchall()
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

@app.get("/categories-lin")
async def categories():
    global os_c
    conn = database.get_db_connection()
    items = conn.execute('SELECT category, compatibility FROM lin_prog').fetchall()
    print(items)
    conn.close()
    categories = []
    for item in items:
        if os_c in str(item['compatibility']):
            categories.append(str(item['category']))
    data = sorted(set(str(item) for item in categories))
    print(os_c)
    return data

#CONTINUE
@app.get("/lin-os")
async def linuxOS():
    conn = database.get_db_connection()
    items = conn.execute('SELECT compatibility from lin_prog').fetchall()
    print(items)
    conn.close()
    unsorted_array = list(set(item for sublist in items for item in sublist))
    unique_items = set()
    for item in unsorted_array:
        unique_items.update(item.split(','))
    data = sorted(list(unique_items))
    return data
@app.post("/get-lin-os")
async def getLinOS(os: dict):
    global os_c
    os_c = os['_value']
    return os

@app.post("/new-user-register")
async def user_reg(userInfo: dict):
    global newUser
    newUser = userInfo

@app.get("/add-new-user")
async def add_user():
    global newUser
    conn = database.get_db_connection()
    users_db = conn.execute('SELECT username, email from user_info').fetchall()
    users = [[str(item['username']), str(item['email'])] for item in users_db]
    
    user_exists = any(newUser['username'] == user[0] and newUser['email'] == user[1] for user in users)
    
    if not user_exists:
        info = tuple(newUser.values())
        conn.execute('INSERT INTO user_info(username, email, password) VALUES (?, ?, ?)', info)
        conn.commit()
    return newUser