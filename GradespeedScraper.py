from bs4 import BeautifulSoup
from Tkinter import *
import mechanize, re

cj = mechanize.CookieJar()
br = mechanize.Browser()

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

def inDepthDL(ending):
    link = "https://gradespeed.kleinisd.net/pc/ParentStudentGrades.aspx"+ending
    try:
        br.open(link)
    except Exception:
        print "Sorry. There was an error."
    
    return 1

def GUIprintSel(Titles, Matrix, Child):
    GUISel = Tk()
    GUISel.title(Child)
    for rows in Matrix:
        holda = 1
        for columns in rows:
            try:
                try:
                    temp = "%s" % str(Titles[holda].contents[0]).ljust(7) + " : " + str(columns[0]).split(">")[1].split("<")[0]
                except Exception:
                    temp = "%s" % str(Titles[holda].contents[0]).ljust(7) + " : " + columns[0]
            except Exception:
                temp = "%s" % str(Titles[holda].contents[0]).ljust(7) + " : "
            holda=holda+1
            Label(GUISel,text=temp).pack()
        Label(GUISel,text="").pack()
    GUISel.mainloop()

def tableGet(options, oneStudent, iterator, namHold):
    if oneStudent!=True:
        name = str(namHold)
        name=name.split("label='")[iterator+1].split("'")[0]
        print name
        print
        br.select_form("aspnetForm")
        studCaux = br.form.find_control(nr=10)
        studCaux.value = [options.name]
        br.submit()
    
    oGrade = br.follow_link(text_regex="Grades")
    oPage = oGrade.read()
    if oneStudent:
        narrowed = oPage.split("var")[2].split("document.write")[0].split("'")
    else:
        narrowed = oPage.split("var")[3].split("document.write")[0].split("'")
    code=""
    for i in range(3,len(narrowed)):
        if i%2==1:
            code=code+narrowed[i]
    
    rawhtml = decodeString(code)
    woU8 = rawhtml.replace("&nbsp;","")

    getTableDat = BeautifulSoup(woU8)
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
        
    for rows in matric:
        holda = 1
        for columns in rows:
            try:
                try:
                    temp = "%s" % str(Cols[holda].contents[0]).ljust(7) + " : " + str(columns[0]).split(">")[1].split("<")[0]
                    print temp
                except Exception:
                    temp = "%s" % str(Cols[holda].contents[0]).ljust(7) + " : " + columns[0]
                    print temp
            except Exception:
                temp = "%s" % str(Cols[holda].contents[0]).ljust(7) + " : "
                print temp 
            holda=holda+1
        print
    #GUIprintSel(Cols, matric, name)

def cycleStuff(userNm, passWd):
    
    Continue = True
    
    try:
        br.open("https://gradespeed.kleinisd.net/pc/Default.aspx")
    except Exception:
        print "Please check if you are connected to the internet."
        Continue = False
        
    if Continue:
        br.select_form("Form1")
        
        userCtrl = br.form.find_control("txtUserName")
        passwrdCtrl = br.form.find_control("txtPassword")
        
        userCtrl.value = userNm
        passwrdCtrl.value = passWd

        response = br.submit()
        try:
            br.select_form("aspnetForm")
        except Exception:
            print "Incorrect Username and/or Password."
            Continue = False
            
        if(Continue):
            oneStudent=False
            
            try:
                studC = br.form.find_control(nr=10)
            except Exception:
                oneStudent = True

            if oneStudent:
                tableGet(["BLARRRGHHH!"], oneStudent, 0, ["Trolol"])
            else:
                it=0
                for options in studC.items:
                    tableGet(options, oneStudent, it, studC.items)
                    it=it+1
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
    logGUI = Tk()
    logGUI.geometry("200x200+250+250")
    logGUI.title("Login Window")
    Label(logGUI,text="").pack()
    logSign = Label(logGUI,text="Login to GradeSpeed").pack()
    Label(logGUI,text="").pack()
    userSign = Label(logGUI,text="Username:").pack()
    userHold = StringVar()
    userField = Entry(logGUI,textvariable=userHold).pack()
    Label(logGUI,text="").pack()
    passSign = Label(logGUI,text="Password:").pack()
    passHold = StringVar()
    passField = Entry(logGUI,textvariable=passHold, show = "*").pack()
    Label(logGUI,text="").pack()
    okBut = Button(text="Login",command=getLogin).pack()
    logGUI.mainloop()

def main():
    br.set_cookiejar(cj)
    br.set_handle_robots(False)
    br.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0')]
    logGUIMeth()

if __name__ == "__main__":
    
    main()
