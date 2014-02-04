from bs4 import *
from Tkinter import *
import mechanize, platform, os

cj = mechanize.CookieJar()
br = mechanize.Browser()
isWindows = False
oneStudent = False

def centerDat(gui):
    gui.update_idletasks()
    xPos = (gui.winfo_screenwidth()/2) - (gui.winfo_width()/2)
    yPos = (gui.winfo_screenheight()/2) - (gui.winfo_height()/2)
    gui.geometry("+%d+%d" % (xPos, yPos))

def printMess(texty, titlee="Messaage"):
    popup = Tk()
    popup.title(titlee)
    Label(popup, text = texty).pack(padx=10,pady=10)
    centerDat(popup)
    if(isWindows):
        popup.mainloop()

def decodeString(inpt):
    keyStr = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
    output = ""
    i=0
    while i < len(inpt):

        enc1 = keyStr.find(inpt[i])
        i=i+1
        enc2 = keyStr.find(inpt[i])
        i=i+1
        enc3 = keyStr.find(inpt[i])
        i=i+1
        enc4 = keyStr.find(inpt[i])
        i=i+1
        
        chr1 = (enc1 << 2) | (enc2 >> 4)
        chr2 = ((enc2 & 15) << 4) | (enc3 >> 2)
        chr3 = ((enc3 & 3) << 6) | enc4
        output = output + chr(chr1)
        
        if enc3 != 64:
            output = output + chr(chr2)

        if enc4 != 64:
            output = output + chr(chr3)
    return output

def studentSel(studys):
    name = str(studys)
    fname = name.split("label='")[1].split("'")[0]
    names=[fname]
    for i in range(1,len(studys)):
        names.append(name.split("label='")[i+1].split("'")[0])
    def buttPress():
        inde=0
        daTemp = var.get()
        for i in range(1,len(names)):
            if str(daTemp) in str(names[i]):
                inde = i
        studSel.destroy()
        tableGet(studys[inde], inde, studys)
    studSel = Tk()
    centerDat(studSel)
    studSel.title("Student Selection")
    var = StringVar()
    var.set(fname)
    Label(text="Select a student:").pack(padx=50, pady=(10,5))
    OptionMenu(studSel, var, *names).pack(padx=50, pady=10)
    Button(text="Continue", command=buttPress).pack(padx=50, pady=(5,10))
    if(isWindows):
        studSel.mainloop()
    

def inDepthDL(ending):
    link = "https://gradespeed.kleinisd.net/pc/ParentStudentGrades.aspx"+ending
    try:
        resp = br.open(link)
    except Exception:
        printMess("Sorry. There was an error.")

    hueHue = str(resp.read())

    specificWOver = Tk()
    specificWOver.title("Specific Grades")
    getOverViewFrame(specificWOver, hueHue).pack(expand = 1, pady = 8, padx = 8)
    if oneStudent:
        newStuff = extractInfo(3, hueHue)
    else:
        newStuff = extractInfo(4, hueHue)
    beauts = BeautifulSoup(newStuff)
    wTitle = beauts.h3.string
    print "%s\n" % wTitle
    columns = (beauts.find_all("td",class_="AssignmentName"),beauts.find_all("td",class_="DateAssigned"),beauts.find_all("td",class_="DateDue"),beauts.find_all("td",class_="AssignmentGrade"),beauts.find_all("td",class_="AssignmentNote"))
    formatStrTempl = "%-40s %8s %8s %8s\n"
    datRes= (formatStrTempl+"\n") % ("Assignment Name", "Assigned", "Due Date", "Grade") 
    for i in range(len(columns[0])):
        datRes = datRes + (formatStrTempl+" -Note: %s\n\n") % (columns[0][i].string,columns[1][i].string,columns[2][i].string,columns[3][i].string,columns[4][i].string)
    print datRes
    #printMess(datRes, titlee=wTitle)
    if oneStudent==False:
        getStudentButton(specificWOver).pack(pady=10)
    centerDat(specificWOver)
    if(isWindows):
        specificWOver.mainloop()

def getOverViewFrame(GUI, unProcPage):

    def inDepthSetup(str):
        GUI.destroy()
        inDepthDL(str)

    if oneStudent:
        done = extractInfo(2, str(unProcPage))
    else:
        done = extractInfo(3, str(unProcPage))

    getTableDat = BeautifulSoup(done)
    getTableDat.prettify()
    fRow=getTableDat.findAll("tr")
    tempCols = BeautifulSoup(str(fRow[0]))
    Cols = tempCols.findAll("th")
    numOCols= len(Cols)-1
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
    for headers in range(1,len(Cols)):
        Label(daFr, text=Cols[headers].contents[0]).grid(row=0, column=headers-1)
    for rows in range(len(matric)):
        holda = 1
        for columns in range(len(matric[rows])):
            temp=""
            isLink = False
            try:
                try:
                    temp = str(matric[rows][columns]).split(">")[1].split("<")[0]
                    if 'href="' in str(matric[rows][columns]):
                        isLink=True
                except Exception:
                    temp = str(matric[rows][columns][0])
            except: temp = "-"
            holda=holda+1
            if isLink:
                temper = str(matric[rows][columns]).split('href="')[1].split('"')[0]
                Button(daFr,text=temp, command=lambda temper = temper:inDepthSetup(temper)).grid(row=rows+1, column=columns)
            else:
                Label(daFr,text=temp).grid(row=rows+1, column=columns)
    return daFr

def getStudentButton(GUI):
    def studSelBut():
        GUISel.destroy()
        studentSel(holdy)
    return Button(GUI,text="Select Student", command=studSelBut)
        
def GUIprintSel(page, Child, holdy):
    GUISel = Tk()
    GUISel.title(Child)
    ovs = getOverViewFrame(GUISel, page)
    ovs.pack(expand = 1, pady = 8, padx = 8)
    if oneStudent==False:
        getStudentButton(GUISel).pack(pady=10)
    centerDat(GUISel)
    if(isWindows):
        GUISel.mainloop()

def extractInfo(index, unProcessed):
    narrowed = unProcessed.split("var")[index].split("document.write")[0].split("'")
    code=""
    for i in range(3,len(narrowed)):
        if i%2==1:
            code=code+narrowed[i]
    
    rawhtml = decodeString(code)
    woU8 = rawhtml.replace("&nbsp;","")
    return woU8;

def tableGet(options, iterator, namHold):
    global br
    if oneStudent!=True:
        name = str(namHold)
        name=name.split("label='")[iterator+1].split("'")[0]
        br.select_form("aspnetForm")
        studCaux = br.form.find_control(nr=10)
        studCaux.value = [options.name]
        br.submit()
    
    oGrade = br.follow_link(text_regex="Grades")
    oPage = oGrade.read()

    if oneStudent!=True:
        GUIprintSel(oPage, name, namHold)
    else:
        GUIprintSel(oPage, "Grades", namHold)

def cycleStuff(userNm, passWd):
    global oneStudent    
    Continue = True
    
    try:
        br.open("https://gradespeed.kleinisd.net/pc/Default.aspx")
    except Exception:
        printMess("Please check if you are connected to the internet.")
        Continue = False
        
    if Continue:
        br.select_form("Form1")
        
        userCtrl = br.form.find_control("txtUserName")
        passwrdCtrl = br.form.find_control("txtPassword")
        
        userCtrl.value = userNm
        passwrdCtrl.value = passWd

        br.submit()
        
        try:
            br.select_form("aspnetForm")
        except Exception:
            printMess("Incorrect Username and/or Password.")
            Continue = False
            
        if(Continue):            
            try:
                studC = br.form.find_control(nr=10)
            except Exception:
                oneStudent = True

            if oneStudent:
                tableGet(["None"], 0, ["None"])
            else:
                studentSel(studC.items)
        else:
            logGUIMeth("","")
    else:
        logGUIMeth("","")    

def logGUIMeth(username, password):
    def getLogin():
        uTemp=userHold.get()
        pTemp=passHold.get()
        if(isChecked.get()):
            logF = open("dep.dat", "w")
            logF.write(uTemp+" "+pTemp)
            logF.close()
        else:
            try:
                os.remove("dep.dat")
            except Exception:
                pass
        logGUI.destroy()
        cycleStuff(uTemp,pTemp)
        return

    def entLog(evt):
        getLogin();
        return

    def onCheckFlip():
        if(isChecked.get()):
            logF = open("dep.dat", "w")
            logF.write(userHold.get()+" "+passHold.get())
            logF.close()
        else:
            try:
                os.remove("dep.dat")
            except Exception:
                pass
        return

    logGUI = Tk()
    logGUI.title("Login Window")
    Label(logGUI,text="Login to GradeSpeed").pack(padx=50,pady=(10,5))
    Label(logGUI,text="Username:").pack(padx=50, pady=(5,0))
    userHold = StringVar()
    userHold.set(username)
    userField = Entry(logGUI,textvariable=userHold)
    userField.pack(padx=50, pady=(0,5))
    userField.bind("<Key-Return>", entLog)
    Label(logGUI,text="Password:").pack(padx=50, pady=(5,0))
    passHold = StringVar()
    passHold.set(password)
    passField = Entry(logGUI,textvariable=passHold, show = "*")
    passField.pack(padx=50, pady=(0,5))
    passField.bind("<Key-Return>", entLog)

    isChecked = BooleanVar()
    isChecked.set(len(username)>0)
    framey = Frame(logGUI)
    Checkbutton(framey, text="Remember Logon", var=isChecked, command=onCheckFlip).pack()
    framey.pack(pady=5)
    
    Button(text="Login",command=getLogin).pack(padx=50, pady=(5,10))
    centerDat(logGUI)
    if(isWindows):
        logGUI.mainloop()

def main():
    global isWindows, br, cj
    username=""
    password=""
    
    try:
        logonF = open("dep.dat")
        temp = logonF.read()
        username = str(temp).split(" ")[0]
        password = str(temp).split(" ")[1]
        logonF.close()
    except Exception:
        pass
        
    if(platform.system()=="Windows"):
        isWindows = True
    br.set_cookiejar(cj)
    br.set_handle_robots(False)
    br.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0')]
    logGUIMeth(username, password)

if __name__ == "__main__":
    main()
