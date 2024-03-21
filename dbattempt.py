import time
from dbconnect import db
from datetime import date

def attempt(declaration, demography):
    connect, cursor = db()
    cursor.execute("SELECT * FROM observations")
    columns = [column[0] for column in cursor.description]
    nid = len(cursor.fetchall())
    insert = """INSERT INTO observations(
    ID, ABF, A, AP, AN, B, BP, BN, DATE,
    VNAME, VNUMBER, GNAME, GNUMBER,
    BYEAR, GENDER, DEPARTMENT, SCORE, SCORED, EYEAR, LGRAD,
    DISEASE, DISEASED, DRUG, DRUGD, HEALTH, MEMORY,
    PDRUG, PDRUGD, DIAGNOSIS, DIAGNOSISD) VALUES (?,?,?,?,?,?,?,?,?, ?,?,?,?, ?,?,?,?,?,?,?, ?,?,?,?,?,?, ?,?,?,?);"""
    today = date.today().strftime("%Y-%m-%d")
    if nid % 4 == 0: values =    (nid+1, "A", 1, 1, 2, 2, 1, 2, today, *declaration, *demography)
    elif nid % 4 == 1: values =  (nid+1, "B", 2, 1, 2, 1, 1, 2, today, *declaration, *demography)
    elif nid % 4 == 2: values =  (nid+1, "A", 1, 2, 1, 2, 2, 1, today, *declaration, *demography)
    elif nid % 4 == 3: values =  (nid+1, "B", 2, 2, 1, 1, 2, 1, today, *declaration, *demography)

    while True:
        try:
            cursor.execute(insert, values)
            connect.commit()
            print(f"ID{nid} veritabanına işlendi.")
            cursor.execute("SELECT * FROM observations WHERE ID = ?", (nid+1,))
            observation = cursor.fetchone()[:9]
            connect.close()
        except: time.sleep(1)
        else: break

    # cursor.execute(insert, values)
    # connect.commit()
    # print(f"ID{nid} veritabanına işlendi.")
    # cursor.execute("SELECT * FROM observations WHERE ID = ?", (nid+1,))
    # observation = cursor.fetchone()[:9]
    # connect.close()
    return columns, observation

def put(table, column, values):
    connect, cursor = db()
    update = "UPDATE {} SET {} = ? WHERE ID = ?".format(table, column)
    while True:
        try:    
            cursor.execute(update, values)
            connect.commit()
            connect.close()  
        except: time.sleep(1)
        else: break   
    # cursor.execute(update, values)
    # connect.commit()
    # connect.close()