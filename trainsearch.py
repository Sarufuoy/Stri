import random 
from mysql.connector import connect
import json
db = connect(
    host="localhost",
    user="root",
    password="root",
    database="trains")
cursor = db.cursor()

cursor.execute("select code, cords from stations;")
sdata = cursor.fetchall()

l = {}
f = []
for i in sdata:
    k = i[1]
    l[f'{k}'] = i[0]

cursor.execute("SELECT fromnum, stxdata FROM traininfo")
tdata = cursor.fetchall()

for i in tdata:
    tcords = json.loads(i[1])
    w=[]
    for k in tcords:
        w.append(l[f'{k}'])
    f.append((i[0], w))
    
for i in f:
    loads = json.dumps(i[1])
    x = random.randrange(500, 1100, 100)
    try:
        print("INSERTING:------")
        print("train:", i[0])
        print("stations:", i[1][1])
        print("number:", x)
        print("----------------")

        cursor.execute(
            "INSERT INTO trst VALUES (%s, %s, %s)",
            (i[0], loads, x)
        )

        db.commit()
    except Exception as e:
        print("\nFailed! at:-")
        print("train number:", repr(i[0]))
        print("stations:", repr(i[1]))
        print("JSON:", repr(loads))
        print("random number:", repr(x))
        print("error:", e)
        if input("Do you want to continue? (y/n): ").lower() != 'y':
            break
        db.rollback()
