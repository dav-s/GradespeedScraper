from gradespeedscraper.wrapper import Wrapper, Link
from gradespeedscraper.tkgui_utils import center_gui
from gradespeedscraper.stringcode import encode_string, decode_string
from Tkinter import Tk, Label, StringVar, Entry, BooleanVar, Frame, Checkbutton, Button
import json
import os


def login_gui(username, password):
    def get_login():
        temp_username = username_holder.get()
        temp_password = password_holder.get()
        if remember_login_holder.get():
            logon_file = open("dep.dat", "w")
            logon_file.write(encode_string(temp_username+" "+temp_password))
            logon_file.close()
        else:
            if os.path.isfile("dep.dat"):
                os.remove("dep.dat")
        login_tk.destroy()
        wrapper_gui(temp_username, temp_password)
        return

    def enter_login(evt):
        get_login()
        return

    def on_checkbox_flip():
        if remember_login_holder.get():
            logon_file = open("dep.dat", "w")
            logon_file.write(encode_string(username_holder.get()+" "+password_holder.get()))
            logon_file.close()
        else:
            if os.path.isfile("dep.dat"):
                os.remove("dep.dat")
        return

    login_tk = Tk()
    login_tk.title("Login Window")
    Label(login_tk, text="Login to GradeSpeed").pack(padx=50, pady=(10, 5))
    Label(login_tk, text="Username:").pack(padx=50, pady=(5, 0))
    username_holder = StringVar()
    username_holder.set(username)
    username_field = Entry(login_tk, textvariable=username_holder)
    username_field.pack(padx=50, pady=(0, 5))
    username_field.bind("<Key-Return>", enter_login)
    Label(login_tk, text="Password:").pack(padx=50, pady=(5, 0))
    password_holder = StringVar()
    password_holder.set(password)
    password_field = Entry(login_tk, textvariable=password_holder, show="*")
    password_field.pack(padx=50, pady=(0, 5))
    password_field.bind("<Key-Return>", enter_login)

    remember_login_holder = BooleanVar()
    remember_login_holder.set(len(username) > 0)
    login_frame = Frame(login_tk)
    Checkbutton(login_frame, text="Remember Logon", var=remember_login_holder, command=on_checkbox_flip).pack()
    login_frame.pack(pady=5)

    Button(text="Login", command=get_login).pack(padx=50, pady=(5, 10))
    center_gui(login_tk)

    login_tk.mainloop()


def wrapper_gui(username, password):
    wrap = Wrapper(config["specific-url"])
    wrap.login(username, password)
    res = wrap.get_student_grades_overview()
    gui = Tk()
    gui.title(res["student_name"])
    for i, t in enumerate(res["grades"]["headers"]):
        Label(gui, text=str(t)).grid(row=0, column=i)
    for i, r in enumerate(res["grades"]["rows"]):
        for j, c in enumerate(r):
            if isinstance(c, Link):
                Button(gui, text=str(c)).grid(row=i+1, column=j)
            elif c:
                Label(gui, text=str(c)).grid(row=i+1, column=j)
    center_gui(gui)
    gui.mainloop()


def get_file_tuple():
    if os.path.isfile("dep.dat"):
        logon_file = open("dep.dat")
        temp = decode_string(logon_file.read())
        logon_file.close()
        return str(temp).split(" ")[0], str(temp).split(" ")[1]
    return "", ""


def main():
    global config

    if os.path.isfile("config.json"):
        conf_file = open("config.json")
        config = json.loads(conf_file.read())
        conf_file.close()
    else:
        print 'You need to have the "config.json".'
        return

    login_gui(*(get_file_tuple()))

if __name__ == "__main__":
    main()