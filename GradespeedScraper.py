from bs4 import BeautifulSoup
from Tkinter import *
import mechanize, platform

cj = mechanize.CookieJar()
br = mechanize.Browser()
isWindows = False
oneStudent = False

def centerDat(gui):
    gui.update_idletasks()
    xPos = (gui.winfo_screenwidth()/2) - (gui.winfo_width()/2)
    yPos = (gui.winfo_screenheight()/2) - (gui.winfo_height()/2)
    gui.geometry("+%d+%d" % (xPos, yPos))

def printMess(texty):
    popup = Tk()
    popup.title("Message")
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

    print hueHue
    
    specificWOver = Tk()
    getOverViewFrame(specificWOver, hueHue).pack()
    if oneStudent:
        newStuff = extractInfo(3, hueHue)
    else:
        newStuff = extractInfo(4, hueHue)
    print newStuff
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
    
    extracted = []
    
    for rows in indexList:
        extracted.append(rows.contents)

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

def GUIprintSel(page, Child, holdy):
    def studSelBut():
        GUISel.destroy()
        studentSel(holdy)

    GUISel = Tk()
    GUISel.title(Child)
    ovs = getOverViewFrame(GUISel, page)
    ovs.pack(expand = 1, pady = 8, padx = 8)
    if oneStudent==False:
        Button(GUISel,text="Select Student", command=studSelBut).pack(pady=10)
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
        GUIprintSel(oPage, "1st", namHold)

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
                tableGet(["BLARRRGHHH!"], 0, ["Trolol"])
            else:
                studentSel(studC.items)
        else:
            logGUIMeth()
    else:
        logGUIMeth()    

def logGUIMeth():
    def getLogin():
        uTemp=userHold.get()
        pTemp=passHold.get()
        logGUI.destroy()
        cycleStuff(uTemp,pTemp)
        return
    def entLog(evt):
        getLogin();
        return
    logGUI = Tk()
    logGUI.title("Login Window")
    Label(logGUI,text="Login to GradeSpeed").pack(padx=50,pady=(10,5))
    Label(logGUI,text="Username:").pack(padx=50, pady=(5,0))
    userHold = StringVar()
    userField = Entry(logGUI,textvariable=userHold)
    userField.pack(padx=50, pady=(0,5))
    userField.bind("<Key-Return>", entLog)
    Label(logGUI,text="Password:").pack(padx=50, pady=(5,0))
    passHold = StringVar()
    passField = Entry(logGUI,textvariable=passHold, show = "*")
    passField.pack(padx=50, pady=(0,5))
    passField.bind("<Key-Return>", entLog)
    Button(text="Login",command=getLogin).pack(padx=50, pady=(5,10))
    centerDat(logGUI)
    if(isWindows):
        logGUI.mainloop()

def main():
    global isWindows, br, cj
    if(platform.system()=="Windows"):
        isWindows = True
    br.set_cookiejar(cj)
    br.set_handle_robots(False)
    br.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0')]
    logGUIMeth()

if __name__ == "__main__":
    main()
