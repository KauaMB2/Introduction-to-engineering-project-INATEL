import sqlite3

conn=None
cursor=None
def initConection():#Function to init the connnection
    global conn, cursor
    conn=sqlite3.connect('database/database.db')
    cursor=conn.cursor()

def Insert(name,password):#Function to insert data
    initConection()
    cursor=conn.execute("SELECT * FROM mainT WHERE name=?", (name,))#Define the query
    row=cursor.fetchone()#It returns just the one register
    if(row!=None):#If this data already exist in DB...
        return row
    #If the register doesnt exist, it will be inserted
    conn.execute("INSERT INTO mainT (name, password) VALUES (?, ?)", (name, password))#Define the query
    conn.commit()#Close connection
    return None
def getRecords():#Function to get all the records
    initConection()
    cursor.execute("SELECT * FROM mainT")
    rows=cursor.fetchall()#Retun all the records
    sortedRecordList=sorted(rows,key=lambda x: x[3] if x[3] is not None else 0,reverse=True)#This command put the rows in the descending order according the records.
    conn.close()#Close connection
    return sortedRecordList[0:5]#It returns just the first five elements of the list
def login(name,password):
    initConection()
    try:
        cursor.execute(f"SELECT * FROM mainT WHERE name=? and password=?",(name,password))#Define the query
        rows=cursor.fetchone()#It returns just one register in DB
    except:
        return None
    conn.close()#Close connection
    return rows
def getUserRecord(name):
    initConection()
    cursor.execute("SELECT record FROM mainT WHERE name=?",(name,))#Define the query
    record=cursor.fetchone()#It return just one register
    conn.close()#Close connection
    return record
def setNewRecord(newRecord,name):
    initConection()
    currentRecord=getUserRecord(name)[0]
    initConection()
    if(newRecord>currentRecord):
        cursor.execute("UPDATE mainT SET record = ? WHERE name = ?",(newRecord,name))#It defines the query
        conn.commit()#It perform the query
    conn.close()#Close connection




