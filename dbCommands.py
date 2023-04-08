import sqlite3

conn=None
cursor=None
def initConection():
    global conn, cursor
    conn=sqlite3.connect('database/database.db')
    cursor=conn.cursor()

def Insert(name,password):
    initConection()
    cursor=conn.execute("SELECT * FROM mainT WHERE name=?", (name,))
    row=cursor.fetchone()
    if(row!=None):
        return row
    conn.execute("INSERT INTO mainT (name, password) VALUES (?, ?)", (name, password))
    conn.commit()
    return None
def getRecords():
    initConection()
    cursor.execute("SELECT * FROM mainT")
    rows=cursor.fetchall()
    sortedRecordList=sorted(rows,key=lambda x: x[3] if x[3] is not None else 0,reverse=True)#This command put the rows in the descending order according the records.
    conn.close()
    return sortedRecordList[0:5]#It returns just the first five elements of the list
def login(name,password):
    initConection()
    try:
        cursor.execute(f"SELECT * FROM mainT WHERE name=? and password=?",(name,password))
        rows=cursor.fetchone()
    except:
        return None
    conn.close()
    return rows
def getUserRecord(name):
    initConection()
    cursor.execute("SELECT record FROM mainT WHERE name=?",(name,))
    record=cursor.fetchone()
    conn.close()
    return record
def setNewRecord(newRecord,name):
    initConection()
    currentRecord=getUserRecord(name)[0]
    initConection()
    if(newRecord>currentRecord):
        cursor.execute("UPDATE mainT SET record = ? WHERE name = ?",(newRecord,name))
        conn.commit()
    conn.close()

