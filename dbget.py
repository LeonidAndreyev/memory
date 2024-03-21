import pandas as pd
from dbconnect import db

def get_by_rows():
    connect, cursor = db()
    print("Veritabanına bağlanıldı.")

    cursor.execute(f"SELECT * FROM observations")
    columns = [column[0] for column in cursor.description]
    elements = cursor.fetchall()
    connect.close()
    data = pd.DataFrame(data=elements, columns=columns)
    data.to_excel("data.xlsx", index=False)

get_by_rows()  