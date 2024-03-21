from dbconnect import db

def create():
    connect, cursor = db()
    print("Veritabanına bağlanıldı.")
    
    # observations
    table = """
    CREATE TABLE observations(
    ID                      INT     PRIMARY KEY     NOT NULL,
    ABF                     CHAR(1)                 NOT NULL,
    A                       INT                     NOT NULL,
    AP                      INT                     NOT NULL,
    AN                      INT                     NOT NULL,
    B                       INT                     NOT NULL,
    BP                      INT                     NOT NULL,
    BN                      INT                     NOT NULL,
    DATE                    TEXT                    NOT NULL,
    VNAME                   TEXT                            ,
    VNUMBER                 TEXT                            ,
    GNAME                   TEXT                            ,
    GNUMBER                 TEXT                            ,
    BYEAR                   TEXT                            ,
    GENDER                  TEXT                            ,
    DEPARTMENT              TEXT                            ,
    SCORE                   TEXT                            ,
    SCORED                  TEXT                            ,
    EYEAR                   TEXT                            ,
    LGRAD                   TEXT                            ,
    DISEASE                 TEXT                            ,
    DISEASED                TEXT                            ,
    DRUG                    TEXT                            ,
    DRUGD                   TEXT                            ,
    HEALTH                  INT                             ,
    MEMORY                  INT                             ,
    PDRUG                   TEXT                            ,
    PDRUGD                  TEXT                            ,
    DIAGNOSIS               TEXT                            ,
    DIAGNOSISD              TEXT                            ,
    ARECALLRESULTS          TEXT                            ,
    ARECALLDURATION         TEXT                            ,
    BRECALLRESULTS          TEXT                            ,
    BRECALLDURATION         TEXT                            ,
    ARECOGNITIONWORDS       TEXT                            ,
    ARECOGNITIONBINARY      TEXT                            ,
    ARECOGNITIONSCALE       TEXT                            ,
    ARECOGNITIONDURATION    TEXT                            ,
    BRECOGNITIONWORDS       TEXT                            ,
    BRECOGNITIONBINARY      TEXT                            ,
    BRECOGNITIONSCALE       TEXT                            ,
    BRECOGNITIONDURATION    TEXT                            );"""
    cursor.execute(table)
    print("Veritabanında 'observations' tablosu oluşturuldu.")
    connect.commit()
    connect.close()

create()