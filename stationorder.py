from mysql.connector import connect
import json 

db=connect(
    host="localhost",
    user="root",
    passwd="saransh2009",
    database="trains"
    )
cu=db.cursor()
#u.execute("""
"""CREATE TABLE train_stops (
    trainno VARCHAR(20),
    station_code VARCHAR(20),
    stop_order INT,
    PRIMARY KEY (trainno, stop_order),
    INDEX idx_station (station_code),
    INDEX idx_station_order (station_code, stop_order)
)"""
#""")

"""cu.execute("select number, path from trst")
k = cu.fetchall()
for i in k:
    trainno  = i[0]
    path = json.loads(i[1])
    for order, station in enumerate(path):
        #cu.execute("""
"""            INSERT INTO train_stops
            (trainno, station_code, stop_order)
            VALUES (%s, %s, %s)"""
        #""", (trainno, station, order))

cu.execute("""
        SELECT DISTINCT a.trainno
        FROM train_stops a
        JOIN train_stops b
            ON a.trainno = b.trainno
        WHERE a.station_code='NDLS'
        AND b.station_code='BBS'
        AND a.stop_order < b.stop_order;
           """)
print(cu.fetchall())
