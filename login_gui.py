import tkinter as tk
from tkinter import ttk
from tools_login import ConvertTuple, congrats
import sqlite3
from create_account_window import create_acc_window
import bcrypt


#main window for login page
root =tk.Tk()
root.title('Login Page')
root.geometry('400x200')
root.resizable(False, False)
root.configure(bg='white')


#style for theme and widgets
style = ttk.Style(root)
style.theme_create("soft", parent="clam")
style.theme_use("soft")
style.configure("soft.TLabel",font= ("Ubuntu",12,"bold"),foreground = "#e1090a",background = "white")
style.configure("little.TButton",font= ("Ubuntu",7,"bold"),foreground = "#e1090a",background ="white")
style.configure("login.TButton",font= ("Ubuntu",15,"bold"),foreground = "#e1090a",background ="white",borderwidth = 1,relief = "groove")

#username string display
username_label = ttk.Label(root,text = "Username ",style= "soft.TLabel")
username_label.pack(pady=8)

#entry box for users input
username_box = ttk.Entry(root,width=20)
username_box.pack()

#password string display
password_label = ttk.Label(root,text = "Password",style= "soft.TLabel")
password_label.pack(pady=8)

#entry box for users input
password_box = ttk.Entry(root,width=20,show ="*")
password_box.pack()

#button that opens up a create an account window
no_acc_button = ttk.Button(root, text = "dont have an account?",style="little.TButton",command= create_acc_window)
no_acc_button.pack(side="right")



#checks if users given username and password matches an existing one in the database
#if username and password is valid then 'congrats' is called
# if not the username and password entry box reset
def login():
    style.configure("red.TEntry",bordercolor = "red")

    #grabs users input from the entry boxes
    username = username_box.get() 
    password = password_box.get()
    
    #connect to the database 
    conn = sqlite3.connect('login_page.db')

    #allows python code to be exectued in a sqlite database
    cursor = conn.cursor()

    #selects row based on users input for username
    cursor.execute("SELECT * FROM Login_Data WHERE username = ?",(username,))

    #saved to variable for indexing purposes
    users_data = cursor.fetchone()

    #converts password into bytes with the 'utf-8' encoding
    hashed_pwd = bytes(password,encoding="utf-8")
  
    if users_data is not None and  username == ConvertTuple(users_data[2]) and bcrypt.checkpw(hashed_pwd,users_data[3]):
        congrats()

    else:
        username_box.configure(style="red.TEntry")
        password_box.configure(style="red.TEntry")
        username_box.delete(0,"end")
        password_box.delete(0,"end")

#login button widget
login_button = ttk.Button(root, text = "LOGIN",style = "login.TButton",command=login)
login_button.place(x=170,y=125)


root.mainloop()
