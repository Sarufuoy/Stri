from mysql.connector import connect as c
import json

db = c(host="localhost",
       user="root",
       passwd="root",
       database="TRAINS")
cu = db.cursor()
###############################################
class basicfunctions:
    def __init__(self):
        pass   
    def getdata(self,
                type:str, 
                name: str
                ):
        cu.execute(f'select {type} from {name}')
        k = cu.fetchall()
        return k
    def getdatawhere(self,
                    type:str, 
                    name:str, 
                    where:str
                    ):
        cu.execute(f'select {type} from {name} where {where}')
        k = cu.fetchall()
        return k  
basic = basicfunctions()

class traindata:
    def __init__(self, 
                 trainno: str):
        self.number = trainno
        self.trainpath = json.loads(basic.getdatawhere('stxdata', 'traininfo', f'fromnum = "{self.number}"')[0][0])
        self.stx = []
        g = basic.getdata('name, cords, code', 'stations')
        for i in g:
            self.stx.append([i[0], json.loads(i[1]), i[2]])

    def get_train(self):
        data = basic.getdatawhere('*', 'traininfo', f'fromnum = "{self.number}"')
        return data

    def get_schedule(self, code: bool):
        result = []
        if code == False:
            for i in self.trainpath:
                for l in self.stx:
                    if i == l[1]:
                        result.append([l[0], l[2]])
            return result
        elif code == True:
            for i in self.trainpath:
                for l in self.stx:
                    if i == l[1]:
                        result.append(l[2])
            return result           
###############################################

class find:
    def __init__(self, fro, to):
        self.fromstation = fro
        self.tostation = to
        

t = traindata(input("Enter Train Number: "))
schedule = t.get_schedule(True)
print(schedule)
    
