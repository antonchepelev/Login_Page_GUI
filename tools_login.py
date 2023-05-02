import tkinter as tk
from tkinter import ttk


#class for making sure all the criteria is true before adding user info to database
class Criteria:
    def __init__(self):  
        self.first = False
        self.last = False
        self.user = False
        self.password = False



#when data is pulled from sqlite database the info comes in tuple form
#this converts it to str
def ConvertTuple(tup):
        try:
            str = ''
            for item in tup:
                str = str + item
            return str
        except ValueError:
             pass



import bcrypt

#hashing algorithm using a random salt value
def hash_password(password):
    password = bytes(password,encoding="utf-8")
    salt = bcrypt.gensalt() # Generate a salt

    hashed_password = bcrypt.hashpw(password, salt) # Hash the password
    return hashed_password


#used for testing features after all criteria is met 
def congrats():
    congrats_root = tk.Tk()
    congrats_root.title("")
    congrats_root.geometry("100x50")

    label = ttk.Label(congrats_root,text = "congrats")
    label.pack()

    congrats_root.mainloop()





