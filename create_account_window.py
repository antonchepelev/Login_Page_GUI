import tkinter as tk
from tkinter import ttk
from tools_login import ConvertTuple, Criteria, hash_password, congrats
import string
import sqlite3

#test

def create_acc_window():
    #window for creating an account
    window = tk.Tk()
    window.title("Create an Account")
    window.geometry("400x340")
    window.resizable(False,False)
    window.configure(bg="white")
    #window.after(1000,style) 
    style = ttk.Style(window)
    # Create a new theme based on the "clam" theme
    style.theme_create("soft", parent="clam")
    style.theme_use("soft")
    style.configure("text.TLabel",font= ("Ubuntu",12,"bold"),foreground = "#e1090a",background = "white")
    style.configure("text.TFrame",background = "white")
    style.configure("create.TButton", font = ("Ubuntu",15,"bold"),foreground = "#e1090a",background = "white",borderwidth = 1, relief = "groove")
    style.configure("help.TButton",font = ("Ubuntu",12,"bold"),foreground = "#e1090a",background = "white")
    style.configure("close.TButton",font =("Ubuntu",12,"bold"),foreground = "#e1090a",background = "white")
    style.configure("again.TLabel",font =("Ubuntu",12,"bold"),foreground = "#e1090a",background = "white")
    
    #box for first name
    first_frame = ttk.Frame(window,style="text.TFrame")
    first_frame.pack(pady=10,side="top")
    first_label = ttk.Label(first_frame,text= "First name",style = "text.TLabel")
    first_label.pack(padx=15,side="left")
    first_box = ttk.Entry(first_frame,width=15,)
    first_box.pack(pady=10,padx=10,side="left")

    #box for last name
    last_frame = ttk.Frame(window,style="text.TFrame")
    last_frame.pack(pady=10,side="top")
    last_label = ttk.Label(last_frame,text = "Last name ",style = "text.TLabel")
    last_label.pack(padx=15,side="left")
    last_box = ttk.Entry(last_frame,width=15)
    last_box.pack(pady=10,padx=10,side="left")

    #box for username
    username_frame = ttk.Frame(window,style="text.TFrame")
    username_frame.pack(pady=10,side="top")
    username_label = ttk.Label(username_frame,text="Username ",style = "text.TLabel")
    username_label.pack(padx=15,side="left")
    username_box = ttk.Entry(username_frame,width=15)
    username_box.pack(pady=10,padx=10,side="left")

    #box for password
    password_frame = ttk.Frame(window,style="text.TFrame")
    password_frame.pack(pady=10,side="top")
    password_label = ttk.Label(password_frame,text ="Password  ",style = "text.TLabel")
    password_label.pack(padx=15,side ="left")
    password_box = ttk.Entry(password_frame,width=15)
    password_box.pack(pady=10,padx=10,side="left")


    #function used for adding users info to database once criteria is met
    def create_user_acc():
        

        first = first_box.get()
        first = first.capitalize()

        last = last_box.get()
        last = last.capitalize()

        username = username_box.get()
        password = password_box.get()

        meets_criteria = Criteria()
        letters = string.ascii_letters

        conn = sqlite3.connect('login_page.db')
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM Login_Data WHERE username = ?",(username,))

        conn.commit()
        
        check_user = (cursor.fetchone())
        

        #get input from the boxes
        

        #checking if first name criteria is True
        if not all(chars in letters for chars in first) or len(first) < 1:
            first_label.configure(text = "Try Again",style ="again.TLabel")
            first_box.delete(0,"end")

        else:
            first_label.configure(text= "First name",style = "text.TLabel")
            meets_criteria.first = True

        #checking if last name criteria is True
        if not all(chars in letters for chars in last) or len(last) < 1:
            last_label.configure(text = "Try Again",style = "again.TLabel")
            last_box.delete(0,"end")
        else:
            last_label.configure(text = "Last name ",style = "text.TLabel")
            meets_criteria.last = True

        #checking if username criteria is True
        if not len(username) > 1:
            username_label.configure(text = "Try Again",style = "again.TLabel")
            username_box.delete(0,"end")

        elif check_user is not None:
            #convert the existing username in database from tuple to str
            exists_user = ConvertTuple(check_user)
            if username == exists_user :
                username_label.configure(text = "Try Again",style = "again.TLabel")
                username_box.delete(0,"end")
        
        else:
            username_label.configure(text ="Username ",style = "text.TLabel")
            meets_criteria.user = True
            conn.commit()

        #checking if password criteria is True
        if not len(password) > 7 :
            password_label.configure(text = "Try Again",style = "again.TLabel")
            password_box.delete(0,"end")

        else:
            password_label.configure(text = "Password  ",style = "text.TLabel")
            meets_criteria.password = True



        if meets_criteria.user and meets_criteria.first and meets_criteria.last and meets_criteria.password == True:
            
            #hashes the users password
            hashed_password = hash_password(password)
            
            # Insert a new user
            user_data = (first, last, username,hashed_password)
            cursor.execute("""
                INSERT INTO Login_Data(first, last, username, password)
                VALUES (?, ?, ?, ?)
            """, user_data)

            conn.commit()

            #close cursor connection
            cursor.close()
            #close the database
            conn.close()
  

            congrats()


        
        
    create_button = ttk.Button(window,text="Create Account",style ="create.TButton",command=create_user_acc)
    create_button.pack(pady =20)


    #shows criteria for a persons info
    def help():
        help_window = tk.Tk()
        help_window.title("HELP")
        help_window.geometry("400x300")
        help_window.resizable(False,False)
        help_window.configure(background="white")

        style = ttk.Style(help_window)
        style.theme_create("soft", parent="clam")
        style.theme_use("soft")
        style.configure("close.TButton",font =("Ubuntu",15,"bold"),foreground = "#e1090a",background = "white",borderwidth = 1,relief = "groove")

        rules_text = tk.Text(help_window,font=("Ubuntu",12,"bold"),height=10,background="white",relief="flat")
        rules_text.insert(tk.END,"> First and last name may not include numbers   or special characters\n\n> If username is already in use it will ask you       to try again\n\n> Your password must be at least 8 characters    long\n\n")
        rules_text.configure(state="disabled")
        rules_text.pack(padx=20,pady=20)
        
        #close button for the help window
        def close():
            help_window.destroy()
        
        close_button = ttk.Button(help_window,text ="CLOSE",style = "close.TButton",command=close)
        close_button.pack()

        help_window.mainloop()



    help_button = ttk.Button(window,text="HELP",style = "help.TButton",command=help)
    help_button.place(x=345,y=300)

    def close():
        window.destroy()
    
    close_button = ttk.Button(window,text="CLOSE",style ="close.TButton",command=close)
    close_button.place(x=10,y=300)
    
    window.mainloop()
