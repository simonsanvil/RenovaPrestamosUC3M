from __future__ import print_function
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import time
import tkinter
from tkinter import *

os.chdir(os.path.dirname(os.path.realpath(__file__)))

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

#Get credentials:
if not os.path.isfile("AulaCredentials.txt"): #If we we dont have the credentials in a file already
    credentials = getCredentials() # TODO: NUMERO DE ESTUDIANTE y contrasena de aula global
    NIA = credentials[0]
    PASS = credentials[1]

else: #Reading credentials from file in directory if it exists
    with open("AulaCredentials.txt") as f:
        lineList = [line.rstrip('\n') for line in open("AulaCredentials.txt")]
        NIA = lineList[0]
        PASS = lineList[1]

driver = webdriver.Chrome(os.path.dirname(os.path.realpath(__file__))+'/chromedriver.exe')
URL = 'https://bibliotecas.uc3m.es/primo-explore/account?vid=34UC3M_VU1&lang=en_US&section=overview'#'https://developer.mozilla.org/en-US/docs/Web/HTML/Element/button'
driver.get(URL)

#Click Login with Aulaglobal button:
login_button = driver.find_elements_by_xpath('//*[@id="tab-content-0"]/div/md-content/md-list/md-list-item[1]/div/button')[0]
login_button.click()

#Fill login credentials
username = driver.find_element_by_name("adAS_username")
password = driver.find_element_by_name("adAS_password")

username.send_keys(NIA)
password.send_keys(PASS)

driver.find_element_by_id("submit_ok").click()
#
# driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 't')
# # driver.get(URL)
# #
time.sleep(3)
#Click 'Blocks + messages' button
blocks_button = driver.find_elements_by_xpath('//*[@id="tab-content-1"]/div/div/div/prm-messages-and-blocks-overview/div/div/md-list/md-list-item[1]/div/button')[0]
blocks_button.click()
