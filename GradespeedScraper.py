from bs4 import BeautifulSoup
from Tkinter import *
import mechanize, re

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

def netStuff(userNm, passWd):
    cj = mechanize.CookieJar()
    br = mechanize.Browser()
    br.set_cookiejar(cj)
    br.set_handle_robots(False)
    br.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0')]
    
    br.open("https://gradespeed.kleinisd.net/pc/Default.aspx")
    
    br.select_form("Form1")
    
    userCtrl = br.form.find_control("txtUserName")
    passwrdCtrl = br.form.find_control("txtPassword")
    
    userCtrl.value = userNm
    passwrdCtrl.value = passWd

    response = br.submit()
    
    
    br.select_form("aspnetForm")

    studC = br.form.find_control(nr=10)

    for options in studC.items:
        
        print options.name
        print
    
        br.select_form("aspnetForm")
        studCaux = br.form.find_control(nr=10)
        studCaux.value = [options.name]
        br.submit()
        
        oGrade = br.follow_link(text_regex="Grades")
        oPage = oGrade.read()
        narrowed = oPage.split("var")[3].split("document.write")[0].split("'")
        code=""
        for i in range(3,len(narrowed)):
            if i%2==1:
                code=code+narrowed[i]
        
        rawhtml = decodeString(code)
        woU8 = rawhtml.replace("&nbsp;","")

        getTableDat = BeautifulSoup(woU8)
        getTableDat.prettify()
        indexList = getTableDat.findAll("td")
        
        extracted = []
    
        for rows in indexList:
            extracted.append(rows.contents)
       
        matric = []
    
        for i in range(len(extracted)/12):
            holder = []
            for j in range(12):
                try:
                    holder.append(extracted[i*12+j])
                except Exception:
                    holder.append([])
            matric.append(holder)
        
        for rows in matric:
            for columns in rows:
                print columns
            print



def getLogin():
    uTemp=userHold.get()
    pTemp=passHold.get()
    logGUI.destroy()
    netStuff(uTemp,pTemp)
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

