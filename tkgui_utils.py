from Tkinter import *


def center_gui(gui):
    gui.update_idletasks()
    x_pos = (gui.winfo_screenwidth()/2) - (gui.winfo_width()/2)
    y_pos = (gui.winfo_screenheight()/2) - (gui.winfo_height()/2)
    gui.geometry("+%d+%d" % (x_pos, y_pos))


def print_message(text, title="Message"):
    popup = Tk()
    popup.title(title)
    Label(popup, text=text).pack(padx=10, pady=10)
    center_gui(popup)

    popup.mainloop()