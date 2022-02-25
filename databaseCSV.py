import pandas as pd
import sqlite3
from sqlite3 import Error

filename = "baby.csv"

#call this function if the date restrain changed, or first time running
def recountCSV(restrain = None):

    df = pd.read_csv(filename)
    # restrain the data by year limits
    df = df[df['Year'] > restrain[0]-1]
    df = df[df['Year'] < restrain[1]+1]

    # add a new column that is 1001 - ['Rank'] (1001 so last place still have 1 point)
    df['point'] = [1001] * df.shape[0] - df['Rank']

    dfmale = df[["Male", "point"]]
    dffemale = df[["Female", "point"]]

    dfmale = dfmale.groupby("Male").sum()
    dfmale = dfmale.sort_values(by=['point'], ascending=False)
    dffemale = dffemale.groupby("Female").sum()
    dffemale = dffemale.sort_values(by=['point'], ascending=False)

    dfmale["newrank"] = [i + 1 for i in range(dfmale.shape[0])]
    dffemale["newrank"] = [i + 1 for i in range(dffemale.shape[0])]

    conn = create_connection()
    dropold_table(conn)
    dfmale.to_sql(name='Male', con=conn)
    dffemale.to_sql(name='Female', con=conn)

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect("baby.db")
    except Error:
        print(Error)

    return conn

def dropold_table(conn):
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS Male;")
    c.execute("DROP TABLE IF EXISTS Female;")
    conn.commit()

def fetchid(id=None, name=None):
    conn = create_connection()
    c = conn.cursor()

    if id is not None:
        fetch1 = fetch2 = int(id)
    elif name is not None:
        sql = f"SELECT newrank FROM Male WHERE Male='{name}'"
        sql2 = f"SELECT newrank FROM Female WHERE Female='{name}'"

        c.execute(sql)
        fetch1 = c.fetchall()
        fetch1 = fetch1 if fetch1 == [] else fetch1[0][0]
        c.execute(sql2)
        fetch2 = c.fetchall()
        fetch2 = fetch2 if fetch2 == [] else fetch2[0][0]

    if fetch1 != []:
        sql3range = (1, 5) if fetch1 <= 3 else (fetch1 -2, fetch1 + 2)
        sql3 = f"SELECT * FROM Male WHERE (newrank BETWEEN {sql3range[0]} AND {sql3range[1]})"
        c.execute(sql3)
        fetch1 = c.fetchall()

    if fetch2 != []:
        sql4range = (1, 5) if fetch2 <= 3 else (fetch2 -2, fetch2 + 2)
        sql4 = f"SELECT * FROM Female WHERE (newrank BETWEEN {sql4range[0]} AND {sql4range[1]})"
        c.execute(sql4)
        fetch2 = c.fetchall()

    return (fetch1, fetch2)

