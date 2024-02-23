from fastapi import FastAPI
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import database

app = FastAPI()
category = None
newUser = None
os_c = None
user_active = False

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

@app.post("/register")
async def register_user(userInfo: dict):
    conn = database.get_db_connection()
    users_db = conn.execute('SELECT username, email FROM user_info WHERE username = ? OR email = ?', (userInfo['username'], userInfo['email'])).fetchone()
    
    if users_db:
        return JSONResponse(status_code=400, content={"message": "Username or email already exists."})
    
    conn.execute('INSERT INTO user_info(username, email, password) VALUES (?, ?, ?)', (userInfo['username'], userInfo['email'], userInfo['password']))
    conn.commit()
    conn.close()
    return {"message": "User added successfully"}

@app.get("/get-users-login")
async def user_login():
    conn = database.get_db_connection()
    users_db = conn.execute('SELECT username, email, password FROM user_info').fetchall()
    users = [[str(item['username']),str(item['email']),str(item['password'])] for item in users_db]
    return users

@app.post("/post-users-activity")
async def users_activity(userActivity: dict):
    global user_active
    conn = database.get_db_connection()
    active = conn.execute('SELECT username, is_active FROM user_activity WHERE username = ? AND is_active = 1',userActivity['_value']['username']).fetchone()
    if active:
        return JSONResponse(status_code=400, content={"message": "User already have logined"})
    
    conn.execute('INSERT INTO user_activity(username,is_active) VALUES (?,?)',[userActivity['_value']['username'],userActivity['_value']['is_active']])
    result = conn.execute('SELECT username, is_active FROM user_activity').fetchall()
    conn.commit()
    conn.close()
    # print(result)
    for res in result:
        for value in res:
            print(value)
            if value == '1':
                user_active = True
    return userActivity
@app.get("get-user-activity")
async def getActivity():
    global user_active
    return user_active