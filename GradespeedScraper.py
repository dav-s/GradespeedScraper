from bs4 import BeautifulSoup
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

userNm = raw_input("Enter Username: ")
passWd = raw_input("Enter Password: ")


br = mechanize.Browser()
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

    br.select_form("aspnetForm")
    studCaux = br.form.find_control(nr=10)
    studCaux.value = [options.name]
    br.submit()
    
    oGrade = br.follow_link(text_regex="Grades")
    oPage = oGrade.read()
    narrowed = oPage.split("'")
    code = narrowed[19]+narrowed[21]+narrowed[23]+narrowed[25]+narrowed[27]+narrowed[29]+narrowed[31]+narrowed[33]+narrowed[35]+narrowed[37]+narrowed[39]+narrowed[41]
    
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
