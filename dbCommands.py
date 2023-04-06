import sqlite3
conn = sqlite3.connect('database.db')
cursor = conn.cursor()
def Insert(name, password):
    cursor=conn.execute("SELECT * FROM mainT WHERE name=?", (name,))
    row=cursor.fetchone()
    if(row!=None):
        return row
    conn.execute("INSERT INTO mainT (name, password) VALUES (?, ?)", (name, password))
    conn.commit()
    return None
def getRecords():
    cursor.execute("SELECT * FROM mainT")
    rows=cursor.fetchall()
    for i in rows:
        print(i)


