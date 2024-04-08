import time
import mysql.connector

def db(mode=True):
    while True:
        try:
            connect = mysql.connector.connect(
            host="666.h.filess.io", port = 3307,
            database="patriciamemorytest_havingdish",
            user="patriciamemorytest_havingdish",
            password="c5adcbeb4321766cac7eb524b413920b77d99ef7")
            if connect.is_connected(): break
        except: time.sleep(1)
    while True:
        try: cursor = connect.cursor(prepared = mode)
        except: time.sleep(1)
        else: break
    return connect, cursor