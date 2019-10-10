from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import time
import tkinter
from tkinter import *
import subprocess

os.chdir(os.path.dirname(os.path.realpath(__file__)))

def clickRenovarPrestamos():
    #Get UC3M credentials:
    if not os.path.isfile("AulaCredentials.txt"): #If we we dont have the credentials in a file already
        credentials = getCredentials() # TODO: NUMERO DE ESTUDIANTE y contrasena de aula global
        NIA = credentials[0]
        PASS = credentials[1]

    else: #Reading credentials from file in directory if it exists
        with open("AulaCredentials.txt") as f:
            lineList = [line.rstrip('\n') for line in open("AulaCredentials.txt")]
            NIA = lineList[0]
            PASS = lineList[1]

    #Config selenium driver and webpage
    driver = webdriver.Chrome(os.path.dirname(os.path.realpath(__file__))+'/chromedriver.exe')
    URL = 'https://bibliotecas.uc3m.es/primo-explore/account?vid=34UC3M_VU1&lang=en_US&section=overview'
    driver.get(URL)
    driver.implicitly_wait(8)

    #Click Login with Aulaglobal button:
    login_button = driver.find_elements_by_xpath('//*[@id="tab-content-0"]/div/md-content/md-list/md-list-item[1]/div/button')[0]
    login_button.click()

    #Fill login credentials
    username = driver.find_element_by_name("adAS_username")
    password = driver.find_element_by_name("adAS_password")

    username.send_keys(NIA)
    password.send_keys(PASS)
    driver.find_element_by_id("submit_ok").click()

    #Click 'Renew' button
    try:
        renew_button = driver.find_element_by_xpath('//*[@id="tab-content-1"]/div/div/div/prm-loans-overview/div/div/div/div/button')
    except Exception as e:
        print( "NO BOOKS TO RENEW")
        return e
    renew_button.click()
    print('[DONE]')

    listElem =  driver.find_element_by_xpath('//*[@id="tab-content-7"]/div/div/prm-loans/md-list')
    bookTitles = [item.get_attribute('title') for item in listElem.find_elements_by_tag_name('h3')]
    bookAuthors = [item.text for item in listElem.find_elements_by_tag_name('h4')]
    print('THE FOLLOWING BOOKS HAVE BEEN RENEWED:')
    for i in range(len(bookTitles)):
        print(str(i+1) + '. ' + bookTitles[i] + ' by ' + bookAuthors[i] + '.')

def getCredentials():
    root = Tk()
    root.iconbitmap('Logo_UC3M.ico')
    root.title('Login')

    L1 = Label(root, text = 'Log with your Aula Global account: ')
    L1.grid(row = 0, column = 0)

    USER_label = Label(root, text = "NIA/student ID:")
    USER_label.grid(row = 1, column = 0)
    USER_entry = Entry(root, bd = 5)
    USER_entry.grid(row = 1, column = 1)

    PASS_label = Label(root, text= 'Password/Contraseña:')
    PASS_label.grid(row = 2,column = 0)
    PASS_entry = Entry(root, bd = 5, show = '*')
    PASS_entry.grid(row = 0, column = 1)
    PASS_entry.grid(row = 2, column = 1)

    credentialsList = []
    def callback():
        username = USER_entry.get()
        PASS = PASS_entry.get()
        credentialsList.append(username)
        credentialsList.append(PASS)
        root.destroy()

    SUBMIT_button = Button(root, text="Submit", width=10, command=callback) # button named submit
    SUBMIT_button.grid(row=3, column=1) # position for button
    root.mainloop()
    return credentialsList

def installRequirementsWithPip():
    #To install required packages:
    subprocess.call([sys.executable, "-m", "pip", "install", "requirements.txt"])

installRequirementsWithPip()
clickRenovarPrestamos()
