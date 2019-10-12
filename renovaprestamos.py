import tkinter
from tkinter import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import time

os.chdir(os.path.dirname(os.path.realpath(__file__)))

class renovaApp_Tk(Tk):
    def __init__(self,parent):
        Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()

    def initialize(self):

        self.title('Login')
        self.iconbitmap('Logo_UC3M.ico')

        L1 = Label(self, text = 'Introduce tus credenciales de la UC3M para renovar tus prestamos: ')
        L1.pack()

        USER_label = Label(self, text = "NIA/student ID:")
        USER_label.pack()
        USER_entry = Entry(self, bd = 5)
        USER_entry.pack()

        PASS_label = Label(self, text= 'Contraseña/Password:')
        PASS_label.pack()
        PASS_entry = Entry(self, bd = 5, show = '*')
        PASS_entry.pack()

        def getEntry():
            return OUTPUT_entry

        def tryCrawl():
            '''
            Para obtener el input de las credenciales de Aula global del estudiante e iniciar el crawling.
            '''
            OUTPUT_entry = getEntry()
            OUTPUT_entry["state"] = NORMAL
            OUTPUT_entry.configure(foreground = 'black')
            OUTPUT_entry.delete('1.0', END)
            OUTPUT_entry.insert(END, "Output will be displayed here")
            OUTPUT_entry["state"] = DISABLED
            credentials = []
            URL = 'https://bibliotecas.uc3m.es/primo-explore/account?vid=34UC3M_VU1&lang=en_US&section=overview'
            NIA = USER_entry.get()
            PASS = PASS_entry.get()
            credentials.append(NIA)
            credentials.append(PASS)
            OUTPUT_entry = self.webCrawl(credentials,URL, self, OUTPUT_entry)

        def destroyRoot():
            print('[TASK HAS BEEN COMPLETED]')
            self.destroy()

        SUBMIT_button = Button(self, text="Renovar Prestamos", width=15, command=tryCrawl) # button named ok
        SUBMIT_button.pack(side=TOP,padx = 3, pady = 5) # position for button

        FINISH_button = Button(self, text="CERRAR", width=10, command= destroyRoot) # button named ok
        FINISH_button.pack(side = TOP) # position for button

        OUTPUT_entry = Text(self, bd = 0, bg = 'lightgrey', height = 5, width = 70, foreground = 'black', font=("Courier", 8))
        OUTPUT_entry.pack(side=LEFT, fill=BOTH, expand = YES)
        yscrollbar=Scrollbar(self, orient=VERTICAL, command=OUTPUT_entry.yview)
        yscrollbar.pack(side=TOP, fill=Y, pady = 10)
        OUTPUT_entry["yscrollcommand"]=yscrollbar.set

        OUTPUT_entry.insert(END, "Output will be displayed here")
        OUTPUT_entry["state"] = DISABLED

        self.grid_columnconfigure(0,weight=0)

        self.mainloop()

    def webCrawl(self,credentials, URL, root, OUTPUT_entry):
        '''
        Funcion principal para realizar el web crawl hacia la pagina web de prestamos
        de la biblioteca de la UC3M.
        '''
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--incognito')
        #options.add_argument('--headless')

        driver = webdriver.Chrome(os.path.dirname(os.path.realpath(__file__))+'/chromedriver.exe', options = options)
        driver.get(URL)
        driver.implicitly_wait(8)

        #Click Login with Aulaglobal button:
        login_button = driver.find_elements_by_xpath('//*[@id="tab-content-0"]/div/md-content/md-list/md-list-item[1]/div/button')[0]
        login_button.send_keys(Keys.RETURN)

        #Fill login credentials
        username = driver.find_element_by_name("adAS_username")
        password = driver.find_element_by_name("adAS_password")

        NIA = credentials[0]
        PASS = credentials[1]
        username.send_keys(NIA)
        password.send_keys(PASS)
        driver.find_element_by_id("submit_ok").send_keys(Keys.RETURN)

        time.sleep(2)
        print(driver.current_url)
        if driver.current_url != URL:
            s = "Error al iniciar sesion. Asegurate de que tus credenciales esten correctos e intenta de nuevo."
            print("[LOGIN ERROR. MAKE SURE YOUR CREDENTIALS ARE CORRECT]")
            # this creates text as a new label to the GUI
            OUTPUT_entry["state"] = NORMAL
            OUTPUT_entry.configure(foreground = 'red')
            OUTPUT_entry.delete('1.0', END)
            OUTPUT_entry.insert(END, s)
            OUTPUT_entry["state"] = DISABLED
            driver.quit()
            return OUTPUT_entry

        #Click 'Renew' button
        try:
            renew_button = driver.find_element_by_xpath('//*[@id="tab-content-1"]/div/div/div/prm-loans-overview/div/div/div/div/button')
        except Exception as e:
            print("[NO BOOKS TO RENEW]")
            s = "No tienes prestamos por renovar"
            OUTPUT_entry["state"] = NORMAL
            OUTPUT_entry.configure(foreground = 'black')
            OUTPUT_entry.delete('1.0', END)
            OUTPUT_entry.insert(END, s)
            OUTPUT_entry["state"] = DISABLED
            driver.quit()
            return OUTPUT_entry

        renew_button.send_keys(Keys.RETURN)
        print('[DONE]')
        listElem =  driver.find_element_by_xpath('//*[@id="tab-content-7"]/div/div/prm-loans/md-list')
        bookTitles = [item.get_attribute('title') for item in listElem.find_elements_by_tag_name('h3')]
        [button.click() for button in listElem.find_elements_by_tag_name('button')]
        bookAuthors = [item.text for item in listElem.find_elements_by_tag_name('h4')]
        vencimientos = [ [item[0].text, item[6].text ] for item in [elem.find_elements_by_tag_name('p') for elem in listElem.find_elements_by_tag_name('prm-loan') ] ]
        [print(info.text) for info in [elem.find_elements_by_tag_name('p') for elem in listElem.find_elements_by_tag_name('prm-loan') ][0] ]
        s = 'Se han renovado los siguientes libros:\n'
        for i in range(len(bookTitles)):
            vence = vencimientos[i][0].split(': ')[1]
            s += str(i+1) + '. ' + bookTitles[i] + ' by ' + bookAuthors[i] + '.\n'
            s += '\tVence: ' + vence + '\n' + '\tFecha maxima de renovacion: ' + vencimientos[i][1].split(': ')[1]
            print(s)
        OUTPUT_entry["state"] = NORMAL
        OUTPUT_entry.delete('1.0', END)
        OUTPUT_entry.configure(foreground = 'blue')
        OUTPUT_entry.insert(END, s)
        OUTPUT_entry["state"] = DISABLED
        driver.quit()
        return OUTPUT_entry

if __name__ == "__main__":
    app = renovaApp_Tk()
