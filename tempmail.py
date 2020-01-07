import json
import requests
import hashlib
import string
import random
import time

URL = None
mail = None
domainList = ["@janmail.org","@mailon.ws","@seo-mailer.com","@clsn1.com","@onmail.top","@jancloud.net","@clsn.top","@sammail.ws","@oncloud.ws","@seomail.top"]

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
def generateMail():
    global mail
    global URL
    mail = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(15)) + domainList[random.randint(0,9)] #random mail generation
    hashmail = hashlib.md5(mail.encode()) #hashing mail with MD5 for usage with tempmail api
    printMailAddress(mail)
    URL = "https://api4.temp-mail.org/request/mail/id/" + hashmail.hexdigest() + "/format/json"

def extractValues(obj, key):
    arr = []     #pull all values of specified key from nested json
    def extract(obj, arr, key): #recursively search for values of key in nested json
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    results = extract(obj, arr, key)
    return results
def printMail(obj):
    mail_from = extractValues(obj.json(), 'mail_from')
    mail_subject = extractValues(obj.json(), 'mail_subject')
    mail_text = extractValues(obj.json(), 'mail_text')
    mail_attachments = extractValues(obj.json(), 'mail_attachments')
    for i in range(0,len(mail_from)):
        print("-------------------------------------------------------------")
        print("[",i+1,"/",len(mail_from),"]",f" - {bcolors.BOLD}{bcolors.UNDERLINE}TO:{bcolors.ENDC}",mail,sep='') 
        print("[",i+1,"/",len(mail_from),"]",f" - {bcolors.BOLD}{bcolors.UNDERLINE}FROM:{bcolors.ENDC} ",mail_from[i],sep='')
        print("[",i+1,"/",len(mail_from),"]",f" - {bcolors.BOLD}{bcolors.UNDERLINE}SUBJECT:{bcolors.ENDC} ",mail_subject[i],sep='')
        print("[",i+1,"/",len(mail_from),"]",f" - {bcolors.BOLD}{bcolors.UNDERLINE}TEXT:{bcolors.ENDC} ",mail_text[i].replace("\n","\n\t\t"),sep='')
    print("-------------------------------------------------------------")
def printMailAddress(obj):
    hashobj = hashlib.md5(obj.encode())
    print("Your temporary mail is: " + obj)
    print("Your hashed mail address is: ", end ="")
    print(hashobj.hexdigest())
def deleteMail(obj):
    url = "https://api4.temp-mail.org/request/delete_address/id/" + hashlib.md5(obj.encode()) + "/format/json"
def refreshMail(obj):
    while 1==1:
        input(f"{bcolors.BOLD}{bcolors.OKGREEN}Press Enter to refresh mailbox...{bcolors.ENDC}")
        printMail(requests.get(obj))

#---------------------------------------------<main>---------------------------------------------
print(f"Generate new mail and open inbox - {bcolors.OKGREEN}1{bcolors.ENDC}")
print(f"Generate custom mail and open inbox - {bcolors.OKGREEN}2{bcolors.ENDC}")
print(f"Open inbox of previously generated mail - {bcolors.OKGREEN}3{bcolors.ENDC}")
print(f"Delete mail - {bcolors.OKGREEN}4{bcolors.ENDC}\n")
option = input("Enter your option: ")

#Generate new mail and open inbox
if option == "1":
    generateMail()
    refreshMail(URL)
        
#Generate custom mail and open inbox        
elif option == "2":
    mail = input("Enter custom name (without @domain.com): ") + domainList[random.randint(0,9)]
    custhashtempmail = hashlib.md5(mail.encode())
    custURL = "https://api4.temp-mail.org/request/mail/id/" + custhashtempmail.hexdigest() + "/format/json"
    printMailAddress(mail)
    refreshMail(custURL)
        
#Open inbox of previously generated mail        
elif option == "3":
    mail = input("Enter previously created tempmail: ")
    hashtempmail = hashlib.md5(mail.encode())
    prevURL = "https://api4.temp-mail.org/request/mail/id/" + hashtempmail.hexdigest() + "/format/json"
    printMailAddress(mail)
    refreshMail(prevURL)
        
#Delete Mail        
elif option == "4":
    deleteMail(input("Enter mail to delete: "))
    print(f"{bcolors.OKGREEN}Success\n{bcolors.ENDC}")
    
    
else:
    print(f"{bcolors.FAIL}Wrong option!{bcolors.ENDC}")
#---------------------------------------------</main>---------------------------------------------