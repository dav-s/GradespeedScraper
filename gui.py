from gradespeedscraper.wrapper import Wrapper, Link
from gradespeedscraper.tkgui_utils import center_gui
from Tkinter import Tk, StringVar, BooleanVar, Frame, Label, LabelFrame, Button, Checkbutton, Entry
#from ttk import Label, Frame, Checkbutton, Button, LabelFrame, Entry
from config import main_url
import os
from base64 import encodestring, decodestring

wrap = Wrapper(main_url)


def login_gui(username, password):
    def get_login(evt=None):
        temp_username = username_holder.get()
        temp_password = password_holder.get()
        if remember_login_holder.get():
            logon_file = open("dep.dat", "w")
            logon_file.write(encodestring(temp_username+" "+temp_password))
            logon_file.close()
        elif os.path.isfile("dep.dat"):
            os.remove("dep.dat")
        login_tk.destroy()
        wrap.login(temp_username, temp_password)
        overview_gui()
        return

    def on_checkbox_flip():
        if remember_login_holder.get():
            logon_file = open("dep.dat", "w")
            logon_file.write(encodestring(username_holder.get()+" "+password_holder.get()))
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
    username_field.bind("<Key-Return>", get_login)
    Label(login_tk, text="Password:").pack(padx=50, pady=(5, 0))
    password_holder = StringVar()
    password_holder.set(password)
    password_field = Entry(login_tk, textvariable=password_holder, show="*")
    password_field.pack(padx=50, pady=(0, 5))
    password_field.bind("<Key-Return>", get_login)

    remember_login_holder = BooleanVar()
    remember_login_holder.set(len(username) > 0)
    login_frame = Frame(login_tk)
    Checkbutton(login_frame, text="Remember Logon", var=remember_login_holder, command=on_checkbox_flip).pack()
    login_frame.pack(pady=5)

    Button(text="Login", command=get_login).pack(padx=50, pady=(5, 10))
    center_gui(login_tk)

    login_tk.mainloop()


def specific_frame(gui, link):
    # TODO: Handle resizing if there is too much information displayed.
    res = wrap.get_class_grades(link)
    main_frame = LabelFrame(gui, text=res["class_name"] + " - " + res["current_average"])
    for sec in res["sections"]:
        frame_name = sec["name"]
        if sec["average"]:
            frame_name += " - " + sec["average"]
        temp_frame = LabelFrame(main_frame, text=frame_name, padx=20, pady=5)
        for i, h in enumerate(sec["grades"]["headers"]):
            Label(temp_frame, text=h).grid(row=1, column=i)
        for i, r in enumerate(sec["grades"]["rows"]):
            for j, c in enumerate(r):
                Label(temp_frame, text=c).grid(row=i+2, column=j)
        temp_frame.pack(padx=20, pady=5)
    main_frame.pack(padx=10, pady=(0, 10))


def specific_gui(link):
    gui = Tk()
    overview_frame(gui)
    specific_frame(gui, link)
    center_gui(gui)
    gui.mainloop()


def overview_frame(gui):
    def click_link(link):
        gui.destroy()
        specific_gui(link)
    res = wrap.get_student_grades_overview()
    frame = LabelFrame(gui, text=res["student_name"], padx=20, pady=10)
    for i, t in enumerate(res["grades"]["headers"]):
        Label(frame, text=str(t)).grid(row=0, column=i)
    for i, r in enumerate(res["grades"]["rows"]):
        for j, c in enumerate(r):
            if isinstance(c, Link):
                Button(frame, command=lambda l=c: click_link(l), text=str(c))\
                    .grid(row=i+1, column=j)
            elif c:
                Label(frame, text=str(c)).grid(row=i+1, column=j)
    frame.pack(padx=10, pady=10)
    gui.title(res["student_name"])


def overview_gui():
    gui = Tk()
    overview_frame(gui)
    center_gui(gui)
    gui.mainloop()


def get_file_tuple():
    if os.path.isfile("dep.dat"):
        logon_file = open("dep.dat")
        temp = decodestring(logon_file.read())
        logon_file.close()
        return str(temp).split(" ")[0], str(temp).split(" ")[1]
    return "", ""


def main():
    login_gui(*(get_file_tuple()))

if __name__ == "__main__":
    main()
