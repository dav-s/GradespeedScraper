from bs4 import *
from Tkinter import *
import mechanize, os, json
from stringcode import decode_string, encode_string
from tkgui_utils import center_gui, print_message

br = mechanize.Browser()
is_one_student = False
nameInfo = None


def studentSel():
    name = str(nameInfo)
    fname = name.split("label='")[1].split("'")[0]
    names = [fname]
    for i in range(1, len(nameInfo)):
        names.append(name.split("label='")[i+1].split("'")[0])

    def buttPress():
        inde = 0
        daTemp = var.get()
        for i in range(1, len(names)):
            if str(daTemp) in str(names[i]):
                inde = i
        studSel.destroy()
        tableGet(nameInfo[inde], inde, nameInfo)
    studSel = Tk()
    center_gui(studSel)
    studSel.title("Student Selection")
    var = StringVar()
    var.set(fname)
    Label(text="Select a student:").pack(padx=50, pady=(10, 5))
    OptionMenu(studSel, var, *names).pack(padx=50, pady=10)
    Button(text="Continue", command=buttPress).pack(padx=50, pady=(5, 10))
    
    studSel.mainloop()
    

def inDepthDL(ending):
    link = config["specific-url"]+ending
    resp = None
    try:
        resp = br.open(link)
    except Exception:
        print_message("Sorry. There was an error.")

    hueHue = str(resp.read())

    specificWOver = Tk()
    specificWOver.title("Specific Grades")
    getOverViewFrame(specificWOver, hueHue).pack(expand=1, pady=8, padx=8)
    if is_one_student:
        newStuff = extractInfo(3, hueHue)
    else:
        newStuff = extractInfo(4, hueHue)
    beauts = BeautifulSoup(newStuff)
    wTitle = beauts.h3.string
    print class_grades_to_pretty_string(beauts)
    #printMess(beautDat(beauts), title=wTitle)
    if not is_one_student:
        getStudentButton(specificWOver).pack(pady=10)
    center_gui(specificWOver)
    
    specificWOver.mainloop()


def class_grades_to_pretty_string(beaut):
    tempTypesG = zip(beaut.find_all(class_="CategoryName"), beaut.find_all(class_="DataTable"))
    heads = [titless.string for titless in beaut.find(class_="TableHeader").find_all("th")]
    heads = heads[0:len(heads)-1]
    modPat = "%-45s"
    for headTitle in heads[1:len(heads)-1]:
        modPat += " %"+str(len(headTitle) if (len(headTitle)>7) else 8)+"s"
    curAvg = beaut.find(class_="CurrentAverage").string
    numsODash = 15 + len(beaut.h3.string) + len(curAvg)
    strRes = ("-"*numsODash)+"\n"
    strRes += "--- %s ---  %s  ---\n%s\n\n%s\n\n" % (beaut.h3.string, curAvg, ("-"*numsODash), (modPat % tuple(heads[0:len(heads)-1])))
    modPat += "\n -Note:%s\n\n"
    for tup in tempTypesG:
        datas = tup[1].find_all(class_=["DataRow", "DataRowAlt"])
        if len(datas)!=0:
            strRes += "-- %s --  Average : %s  --\n\n" % (tup[0].string, datas[len(datas)-1].findNextSibling("tr").find_all("td")[3].string)
        else:
            strRes += "-- %s --\n\n" % tup[0].string
        for row in datas:
            strRes += modPat % tuple([text.string for text in row.find_all("td")][0:len(heads)])
        strRes += "\n"
    return strRes + "\n"


def getOverViewFrame(GUI, unProcPage):

    def inDepthSetup(stri):
        GUI.destroy()
        inDepthDL(stri)

    if is_one_student:
        done = extractInfo(2, str(unProcPage))
    else:
        done = extractInfo(3, str(unProcPage))

    getTableDat = BeautifulSoup(done)
    getTableDat.prettify()
    fRow = getTableDat.findAll("tr")
    tempCols = BeautifulSoup(str(fRow[0]))
    Cols = tempCols.findAll("th")
    numOCols = len(Cols)-1
    indexList = getTableDat.findAll("td")
    
    extracted = [rows.contents for rows in indexList]

    matric = []
    
    for i in range(len(extracted)/numOCols):
        holder = []
        for j in range(numOCols):
            try:
                holder.append(extracted[i*numOCols+j])
            except Exception:
                holder.append([])
        matric.append(holder)
    
    daFr = Frame(GUI)
    for headers in range(1, len(Cols)):
        Label(daFr, text=Cols[headers].contents[0]).grid(row=0, column=headers-1)
    for rows in range(len(matric)):
        holda = 1
        for columns in range(len(matric[rows])):
            temp = ""
            isLink = False
            try:
                try:
                    temp = str(matric[rows][columns]).split(">")[1].split("<")[0]
                    if 'href="' in str(matric[rows][columns]):
                        isLink=True
                except Exception:
                    temp = str(matric[rows][columns][0])
            except: temp = "-"
            holda += 1
            if isLink:
                temper = str(matric[rows][columns]).split('href="')[1].split('"')[0]
                Button(daFr, text=temp, command=lambda temper = temper: inDepthSetup(temper)).grid(row=rows+1, column=columns)
            else:
                Label(daFr, text=temp).grid(row=rows+1, column=columns)
    return daFr


def getStudentButton(GUI):
    def studSelBut():
        GUI.destroy()
        studentSel()
    return Button(GUI, text="Select Student", command=studSelBut)


def GUIprintSel(page, Child, holdy):
    GUISel = Tk()
    GUISel.title(Child)
    ovs = getOverViewFrame(GUISel, page)
    ovs.pack(expand=1, pady=8, padx=8)
    if not is_one_student:
        getStudentButton(GUISel).pack(pady=10)
    center_gui(GUISel)
    
    GUISel.mainloop()


def extractInfo(index, unProcessed):
    narrowed = unProcessed.split("var")[index].split("document.write")[0].split("'")
    code=""
    for i in range(3, len(narrowed)):
        if i % 2 == 1:
            code += narrowed[i]
    
    rawhtml = decode_string(code)
    woU8 = rawhtml.replace("&nbsp;", "")
    return woU8


def tableGet(options, iterator, namHold):
    global br

    name = str(namHold)

    if not is_one_student:
        name = name.split("label='")[iterator+1].split("'")[0]
        br.select_form("aspnetForm")
        studCaux = br.form.find_control(nr=10)
        studCaux.value = [options.name]
        br.submit()
    
    oGrade = br.follow_link(text_regex="Grades")
    oPage = oGrade.read()

    if not is_one_student:
        GUIprintSel(oPage, name, namHold)
    else:
        GUIprintSel(oPage, "Grades", namHold)


def cycleStuff(username, password):
    global is_one_student, nameInfo
    should_continue = True
    
    try:
        br.open(config["main-url"])
    except Exception:
        print_message("Please check if you are connected to the internet.", title="Could Not Connect")
        should_continue = False
        
    if should_continue:
        br.select_form("Form1")
        
        userCtrl = br.form.find_control("txtUserName")
        passwrdCtrl = br.form.find_control("txtPassword")
        
        userCtrl.value = username
        passwrdCtrl.value = password

        br.submit()
        
        try:
            br.select_form("aspnetForm")
        except Exception:
            print_message("Incorrect Username and/or Password.", title="Error")
            should_continue = False
            
        if should_continue:
            try:
                studC = br.form.find_control(nr=10)
                nameInfo = studC.items
                studentSel()
            except Exception:
                is_one_student = True
                tableGet(None, 0, None)
        else:
            login_gui(*(get_file_tuple()))
    else:
        login_gui(*(get_file_tuple()))


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
        cycleStuff(temp_username, temp_password)
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


def get_file_tuple():
    if os.path.isfile("dep.dat"):
        logon_file = open("dep.dat")
        temp = decode_string(logon_file.read())
        logon_file.close()
        return str(temp).split(" ")[0], str(temp).split(" ")[1]
    return "", ""


def main():
    global br, config
    br.set_handle_robots(False)

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
