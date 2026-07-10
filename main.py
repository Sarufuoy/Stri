import tkinter as tk, tkinter
from tkinter import messagebox as mb
from mysql.connector import connect
import random
import json
from PIL import Image, ImageTk, ImageDraw
import uuid

mydb = connect(
    host="localhost",
    user="root",
    passwd="saransh2009",
    database="TRAINS")
cu = mydb.cursor()

'''
PARENT DATABASE -> TRAINS
NAMES OF TABLES USED IN THIS PROJECT ARE:-
-> SCHEDULES - Schedules of all trains
-> STATIONS - List of all stations
-> TRAININFO - Information about all trains
-> USERLOGIN - User login information
-> ADMINLOGIN - Admin login details
'''

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


class user:
    def __init__():
        pass
    
    def login(user:str, 
              password:str
              ):
        cu.execute('select log from userlogin')
        status = cu.fetchall()
        for i in status:
            if status == []:
                break
            if i[0] == hex(uuid.getnode()):
                mb.showerror('Error',
                             'Already logged in from another computer!')
                return False
            else:
                continue  
        cu.execute('Select * from userlogin where name = %s', (user,)) 
        fetch = cu.fetchall()
        if fetch == []:
            print(fetch + ' != ' + password)
            return False, print('Login Not Successfull')
        elif password != fetch[0][1]:
            print(fetch[0][1] + ' != ' + password)
            return False, print('Login Not Successfull')
        else:
            cu.execute(f'update userlogin set log = "{hex(uuid.getnode())}" where name = "{user}"')
            mydb.commit()
            cu.execute(f'select * from userlogin where name = "{user}"')
            return True, print('Login Successfull', cu.fetchall())
    
    def logout(user:str):
        cu.execute(f'update userlogin set log = "0" where name = "{user}"')
        mydb.commit()
        return True, print('Logout Successfull')
        
    def register(name, 
                 password, 
                 confirm_password, 
                 phone, 
                 email
                 ):
        cu.execute('Select * from userlogin')
        checkdata = cu.fetchall()
        if len(phone) != 10: 
            mb.showerror("Error", 
                         "Phone number must be 10 digits")
            return
        for i in checkdata:
            if i[0] == name:
                mb.showerror("Error", 
                             "Username already exists")
                return
            elif i[2] == phone:
                mb.showerror("Error", 
                             "Phone number already exists")
                return
            
            elif i[3] == email:
                mb.showerror("Error", 
                             "Email already exists")
                return
        if confirm_password != password:
            mb.showerror("Error", 
                         "Confirmed Password do not match")
            return
        
        id = None
        cu.execute('Select id from userlogin')
        fetch = cu.fetchall()
        if fetch == []:
            id = random.randint(100000000, 999999999)
        else:
            for i in fetch:
                id = random.randint(100000000, 999999999)
                if i != id:
                    print('id successful: ', id)
                    loopcount = 1
                    break
                else:
                    print("id Generated")

        cu.execute('Insert into userlogin (name, password, phone, email, wallet, id, log) values (%s, %s, %s, %s,%s, %s, %s)', 
                   (name, 
                    password, 
                    phone, 
                    email, 
                    5000.00, 
                    id, 
                    "0"))   
        mydb.commit() 
        return "Commited", print("Commited")

class admin:
    def __init__(self, 
                 username:str, 
                 password:str
                 ):
        self.username = username
        self.password = password

    def login(self):
        print('Admin Login Called..')
        cu.execute(f'Select * from adminlogin where uniqueid = "{self.username}"') 
        fetch = cu.fetchall()
        if fetch == []:
            return print("Username does not exist"), False
        elif self.username == fetch[0][0] and self.password == fetch[0][1]:
            return print('Login successful'), True
        else:
            return print("Incorrect Password"), False
        
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

    def get_schedule(self):
        result = []
        for i in self.trainpath:
            print(i)
            for l in self.stx:
                if i == l[1]:
                    result.append([l[0], l[2]])
                else:
                    print('err')
        return result

class mainwindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Train Ticket Reservation Window')
        self.geometry("900x500")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.resizable(False, False)
        container = tk.Frame(self)
        container.grid(row = 0, column=0, sticky='nsew')
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames={}

        for currentpage in (loginpage, secondpage):
            name = currentpage.__name__
            frame = currentpage(parent=container, controller=self)
            self.frames[name] = frame
            frame.grid(row=0, column=0, sticky='nsew')
        self.show_frame("loginpage")

    def show_frame(self, frname):
        frame = self.frames[frname]
        frame.tkraise()

class loginpage(tk.Frame):
    def __init__(self, 
                 parent, 
                 controller
                 ):
        super().__init__(parent)
        self.controller = controller
        img = Image.open("vb.png")
        img = img.resize((900, 500))
        self.bgimage = ImageTk.PhotoImage(img)   
        self.bg = tk.Label(self, image=self.bgimage)
        self.bg.place(x=0, y=0, relwidth=1, relheight=1)

        img = Image.open("title.png")
        img = img.resize((900, 39))

        self.titleimg = ImageTk.PhotoImage(img)

        self.title = tk.Label(self, image = self.titleimg,
                              padx=0,
                              pady=0,
                              borderwidth=0,
                              relief="flat",
                              highlightthickness=1,
                              highlightbackground="black",
                              )
        self.title.place(x=0, y=0)


        self.searchbg = tk.Label(self,
                                 padx=0,
                                 pady=0,
                                 bg="#76ABAE",
                                 highlightthickness=1,
                                 highlightbackground="black",
                                 relief="flat").place(x=55,
                                                        y=75,
                                                        width=450,
                                                        height=390)

        self.froentry = tk.Entry(self)
        self.froentry.place(x=110, y=115, width=115, height=20)

        self.toentry = tk.Entry(self)
        self.toentry.place(x=335, y=115, width=115, height=20)

        self.searchbtn = tk.Button(self, text="Search Trains", relief="groove", bg="#D0DBA9")
        self.searchbtn.place(x=230, y=115, height=20, width=100)
        
        self.frolab = tk.Label(self, text="From Station", relief="flat", bg="#76ABAE").place(x=110, y=101, width = 115, height=10)
        self.tolab = tk.Label(self, text="To Station", relief="flat", bg="#76ABAE").place(x=335, y=101, width = 115, height=10)
        self.stx = []
        self.stations=[]   
        g = basic.getdata('name, cords, code', 'stations')
        for i in g:
            self.stx.append([i[0], json.loads(i[1]), i[2]])
            self.stations.append(f"{i[0]} - {i[2]}")

        self.optionslist = tk.Listbox(self)
        self.optionslist.bind("<ButtonRelease-1>", 
                              lambda event: self.select_option(event, self.froentry, self.optionslist))
        
        self.froentry.bind(
            "<KeyRelease>",
            lambda event: self.filter_options(
                event, self.froentry, self.stations, self.optionslist))
        self.froentry.bind(
            "<FocusIn>", 
            lambda event: self.show_dropdown(self.froentry, self.optionslist))
        self.froentry.bind(
            "<FocusOut>",
            lambda event: self.hide_dropdown(self.optionslist, None))

        self.optionslist2 = tk.Listbox(self)
        self.optionslist2.bind("<ButtonRelease-1>",
                               lambda event: self.select_option(event, self.toentry, self.optionslist2))
        self.toentry.bind(
            "<KeyRelease>",
            lambda event: self.filter_options(
                event, self.toentry, self.stations, self.optionslist2))
        self.toentry.bind(
            "<FocusIn>", 
            lambda event: self.show_dropdown(self.toentry, self.optionslist2))
        self.toentry.bind(
            "<FocusOut>",
            lambda event: self.hide_dropdown(self.optionslist, None))


    def select_option(self, event, wid, li):
        selected_item = li.get(tk.ANCHOR)
        if selected_item:
            wid.delete(0, tk.END)
            wid.insert(0, selected_item)
        li.place_forget()

    def hide_dropdown(self, wid, event=None):
        self.after(150, lambda: wid.place_forget())
    
    def show_dropdown(self, wid, li ,event=None):
        if not li.winfo_ismapped():
            x = wid.winfo_x()
            y = wid.winfo_y() + 20
            w = wid.winfo_width()
            li.place(x=x, y=y, width=w)
            li.lift()
    
    def update_menu(self, data, li):
        li.delete(0, tk.END)
        for item in data:
            li.insert(tk.END, item)
    
    def filter_options(self, event, entry, options, li):
        typed_text = entry.get()
        if typed_text == '':
            filtered_data = options
        else:
            filtered_data = [item for item in options if typed_text.lower() in item.lower()]

        self.update_menu(filtered_data, li)
        self.show_dropdown(entry, li)

class secondpage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#00CCFF")

if __name__ == "__main__":
    app = mainwindow()
    app.mainloop()