# coding=utf8
import pandas as pd
import time, sqlite3, os, json, datetime
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from PyQt6.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QMessageBox, QCheckBox, QVBoxLayout, QWidget, QLabel, QFileDialog, QComboBox
from PyQt6 import QtWidgets
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
hoje = datetime.datetime.now()
dataFormatada = hoje.strftime('%d-%m-%Y')
conectar = sqlite3.connect('banco2.db')
cursor = conectar.cursor()
cursor.execute('CREATE TABLE if not exists UserData (user text, "group" text, listaCtts text, caminhoXlsx text)')
cursor.execute("""
    CREATE TABLE IF NOT EXISTS CaminhosHtml (
        newMessage TEXT,
        drawerArrow TEXT,
        forward TEXT,
        checkBoxes TEXT,
        toFowardArrow TEXT,
        contactSearch TEXT,
        cancelSearch TEXT,
        sendButton TEXT,
        celula1 TEXT,
        celula2 TEXT,
        celula3 TEXT,
        classGp TEXT,
        sideBar TEXT
    )
""")
cursor.execute("SELECT newMessage, drawerArrow, forward, checkBoxes, toFowardArrow, contactSearch, cancelSearch, sendButton, celula1, celula2, celula3, classGp, sideBar FROM CaminhosHtml")
resultado = cursor.fetchone()
conectar.commit()
cursor.close()

app = QApplication([])

class zapbot:
    def UserDatadb(self, user):
       

        if self.checkboxXl.isChecked():
            bot.definirLista()
        if self.checkboxGp.isChecked():
            bot.abrirZap()
            time.sleep(15)
            titles_list = []

            # Encontrar a barra lateral uma vez
            sidebar = self.driver.find_element(By.XPATH, f"{resultado[12]}")

            # Execute JavaScript para rolar a barra lateral
            while True:
                # Rolar a barra lateral
                self.driver.execute_script("arguments[0].scrollTop += 1000;", sidebar)
                time.sleep(2)  # Espere um pouco após rolar para que a página carregue
                
                # Encontre todos os elementos com a classe "_ak8q" na página atual
                titles = self.driver.find_elements(By.CSS_SELECTOR, f"{resultado[11]}")

                # Extraia e imprima o texto desses elementos
                for title in titles:
                    titles_list.append(title.text)
                
                # Verifique se chegou ao final da lista rolando
                end_of_list = self.driver.execute_script("return arguments[0].scrollHeight - arguments[0].scrollTop === arguments[0].clientHeight;", sidebar)
                if end_of_list:
                    break

            lista_sem_repeticao = list(set(titles_list))
            listaGps = json.dumps(lista_sem_repeticao)
        listaSerializada = json.dumps(self.listaCompleta)
        cursor = conectar.cursor()

        # Convertendo a lista em uma string JSON
        #listaCtts_str = json.dumps(listaCtts)



        cursor.execute("""UPDATE UserData SET listaCtts = :listaCtts, "group" = :group, caminhoXlsx = :caminhoXlsx WHERE user = :user""",
            {
                'listaCtts': (listaSerializada if (self.checkboxXl.isChecked() and not self.checkboxGp.isChecked())
                             else (listaGps if (self.checkboxGp.isChecked() and not self.checkboxXl.isChecked())
                                   else [listaSerializada, listaGps])),
                'group':self.cttNomeEdit.text(),
                'caminhoXlsx':self.listaContatosEdit.text(),# if self.checkboxXl.isChecked() else "",
                'user': user,
            })

        cursor.execute("SELECT listaCtts FROM UserData WHERE user = :user",{'user': user,})
        listaSerializada = cursor.fetchone()[0]
        self.listaCtts= json.loads(listaSerializada)
        conectar.commit()
        cursor.close()
        #if self.checkbox.isChecked() == True:
        #    self.listaCtts = self.listaCtts[self.armazenado[4]:]
           
        self.listaCtts = [item for item in self.listaCtts if "?" not in item]
        for i in range(len(self.listaCtts)):
   
            self.listaCtts[i] = self.listaCtts[i].replace("  ", " ")
            self.listaCtts[i] = self.listaCtts[i].replace("?", "")
            self.listaCtts[i] = self.listaCtts[i].rstrip()
            self.listaCtts[i] = self.listaCtts[i].replace("  ", " ")
        if not self.checkboxGp.isChecked():
            bot.abrirZap()

        bot.disparar()

        '''    def Continuar(self):

        cursor = conectar.cursor()
        conectar.commit()
        cursor.close()'''

    def CaminhosHtmldb(self):

        cursor = conectar.cursor()
        cursor.execute("DELETE FROM CaminhosHtml")
        cursor.execute("""
            INSERT INTO CaminhosHtml (
                newMessage, drawerArrow, forward, checkBoxes, toFowardArrow,
                contactSearch, cancelSearch, sendButton, celula1, celula2,
                celula3, classGp, sideBar
            ) VALUES (
                :newMessage, :drawerArrow, :forward, :checkBoxes, :toFowardArrow,
                :contactSearch, :cancelSearch, :sendButton, :celula1, :celula2,
                :celula3, :classGp, :sideBar
            )
        """, {
            'newMessage': tela2.newMessageEdit.text(),
            'drawerArrow': tela2.drawerArrowEdit.text(),
            'forward': tela2.forwardEdit.text(),
            'checkBoxes': tela2.checkBoxesEdit.text(),
            'toFowardArrow': tela2.toFowardArrowEdit.text(),
            'contactSearch': tela2.contactSearchEdit.text(),
            'cancelSearch': tela2.cancelSearchEdit.text(),
            'sendButton': tela2.sendButtonEdit.text(),
            'celula1': tela2.celula1.text(),
            'celula2': tela2.celula2.text(),
            'celula3': tela2.celula3.text(),
            'classGp': tela2.classGpEdit.text(),
            'sideBar': tela2.sideBarEdit.text(),
        })

        conectar.commit()
        cursor.close()

    def abrirZap(self):
        self.nomeArquivo = f'{self.usuariosComboBox.currentText()}_{dataFormatada}.txt'
        self.window.close()
        options = webdriver.FirefoxOptions()
        options.add_argument('lang=pt-br')
        diretorio_atual = os.getcwd()  # Obtém o diretório atual
        caminho_geckodriver = os.path.join(diretorio_atual, "geckodriver.exe")

        s = Service(executable_path=caminho_geckodriver)
        self.driver=webdriver.Firefox(service=s)
       
        time.sleep(5)
        self.driver.get('https://web.whatsapp.com/')
        time.sleep(10)

    def simulate_mouseover(driver, element):
        script = """
        var evt = new MouseEvent('mouseover', {
            view: window,
            bubbles: true,
            cancelable: true
        });
        arguments[0].dispatchEvent(evt);
        """
        driver.execute_script(script, element)

    def disparar(self):
        
        WebDriverWait(self.driver, 500).until(EC.presence_of_element_located((By.XPATH, f"//span[@title='{self.cttNomeEdit.text()}']")))
        time.sleep(10)
        erru=0
        contact = WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, f"//span[@title='{self.cttNomeEdit.text()}']"))
        )
        contact.click()
        
        while len(self.listaCtts) > 0:
            try:
                contact = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, f"//span[@title='{self.cttNomeEdit.text()}']"))
                )
                for _ in range(3):
                    try:
                        contact.click()
                        break
                    except:
                        time.sleep(1)
                new_message = WebDriverWait(self.driver, 1200).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, f"{resultado[0]}"))
                )
                script = """
                var evt = new MouseEvent('mouseover', {
                    view: window,
                    bubbles: true,
                    cancelable: true
                });
                arguments[0].dispatchEvent(evt);
                """
                self.driver.execute_script(script, new_message)
                time.sleep(1)
                
                self.driver.execute_script("arguments[0].scrollIntoView();", new_message)
                context_menu_button = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, f"{resultado[1]}"))
                )
                context_menu_button.click()

                forward_option = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, f"{resultado[2]}"))
                )
                time.sleep(1)
                forward_option.click()
                time.sleep(1)
                checkboxes = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, f"{resultado[3]}"))
                )

                for checkbox in checkboxes:
                    if not checkbox.is_selected():
                        self.driver.execute_script("arguments[0].scrollIntoView();", checkbox)
                        time.sleep(1)
                        self.driver.execute_script("arguments[0].click();", checkbox)
                
                to_foward = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, f"{resultado[4]}")))
                to_foward.click()

                search_box = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, f"{resultado[5]}"))
                )
                list_range = min(5, len(self.listaCtts))
                x=0
                while x < list_range:
                    try:
                        search_box.click()
                        time.sleep(1)
                        ActionChains(self.driver).send_keys(self.listaCtts[0]).perform()
                        time.sleep(1)
                        contact_send = WebDriverWait(self.driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, f"//span[@title='{self.listaCtts[0]}']"))
                        )
                        contact_send.click()
                        time.sleep(1)
                        erase = WebDriverWait(self.driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, f"{resultado[6]}"))
                        )

                        erase.click()
                        del self.listaCtts[0]
                        x+=1
                    except:
                        try:
                            with open(self.nomeArquivo, 'a', encoding='utf-8') as arquivo:
                                arquivo.write(f'{self.listaCtts[0]}\n')
                            time.sleep(1)
                            WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, f'{resultado[6]}')))
                            apaga=self.driver.find_element(By.XPATH, f'{resultado[6]}')
                            apaga.click()
                            erru=erru+1
                            x+=1
                            del self.listaCtts[0]
                        except:
                            
                            erru=erru+1
                            x+=1
                            del self.listaCtts[0]

                send_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, f"{resultado[7]}"))
                )
                send_button.click()
                time.sleep(1)
                contact.click()
            except:               
                time.sleep(1)
        with open(self.nomeArquivo, 'a') as arquivo:
            arquivo.write(f'Total de erros: {erru}')
        time.sleep(300)
        self.driver.quit()


    def tela1(self):
        self.window = QtWidgets.QWidget()
        self.window.setGeometry(100, 100, 570, 500)
        self.window.setWindowTitle("Tela 1")

        cursor = conectar.cursor()
        cursor.execute('SELECT user, "group", listaCtts, caminhoXlsx FROM UserData')
        self.armazenado = cursor.fetchone()

        cursor.execute('SELECT user FROM UserData')
        self.usuariosCadastrados = cursor.fetchall()
        cursor.close()

        # Campo para selecionar usuário cadastrado
        usuariosLabel = QtWidgets.QLabel("Usuários cadastrados:", self.window)
        usuariosLabel.setGeometry(20, 20, 200, 20)
        self.usuariosComboBox = QComboBox(self.window)
        self.usuariosComboBox.setGeometry(20, 40, 400, 40)
        self.usuariosComboBox.addItems([usuario[0] for usuario in self.usuariosCadastrados])
        self.usuariosComboBox.currentIndexChanged.connect(self.atualizarDadosUsuario)
        
        # Campo para digitar e cadastrar novo usuário
        novoUsuarioLabel = QtWidgets.QLabel("Novo Usuário:", self.window)
        novoUsuarioLabel.setGeometry(20, 90, 200, 20)
        self.novoUsuarioEdit = QLineEdit("", self.window)
        self.novoUsuarioEdit.setGeometry(20, 110, 400, 40)
        self.cadastrarUsuarioButton = QPushButton("Cadastrar Usuário", self.window)
        self.cadastrarUsuarioButton.setGeometry(440, 110, 100, 40)
        self.cadastrarUsuarioButton.clicked.connect(self.cadastrarUsuario)
        
        listaContatosLabel = QtWidgets.QLabel("Arquivo excel:", self.window)
        listaContatosLabel.setGeometry(20, 160, 200, 20)
        self.listaContatosEdit = QLineEdit("", self.window)
        self.listaContatosEdit.setGeometry(20, 180, 400, 40)
        self.listaContatosButton = QPushButton("Select File", self.window)
        self.listaContatosButton.setGeometry(440, 180, 100, 40)
        self.listaContatosButton.clicked.connect(lambda: self.open_file_dialog(self.listaContatosEdit, "Excel Files (*.xlsx)"))

        buttonClearCtt = QPushButton("Definir lista do excel", self.window)
        buttonClearCtt.setGeometry(20, 230, 120, 30)
        buttonClearCtt.clicked.connect(self.definirLista)

        cttNomeLabel = QtWidgets.QLabel("NOME DO CTT/GP:", self.window)
        cttNomeLabel.setGeometry(20, 270, 200, 20)
        self.cttNomeEdit = QLineEdit("", self.window)
        self.cttNomeEdit.setGeometry(20, 290, 400, 40)

        self.checkboxXl = QCheckBox("Usar caminho do Excel", self.window)
        self.checkboxXl.setGeometry(20, 340, 300, 30)

        self.checkboxGp = QCheckBox("Extrair contatos", self.window)
        self.checkboxGp.setGeometry(20, 370, 300, 30)

        button = QPushButton("MODIFICAR", self.window)
        button.setGeometry(20, 410, 120, 30)
        button.clicked.connect(self.abrirTela2)

        buttonDisparar = QPushButton("DISPARAR", self.window)
        buttonDisparar.setGeometry(150, 410, 120, 30)
        buttonDisparar.clicked.connect(lambda: self.UserDatadb(self.usuariosComboBox.currentText()))

        if self.armazenado is not None:
            self.listaContatosEdit.setText(self.armazenado[3])
            self.cttNomeEdit.setText(self.armazenado[1])

        self.window.show()
    def atualizarDadosUsuario(self):
        usuario_selecionado = self.usuariosComboBox.currentText()

        cursor = conectar.cursor()
        cursor.execute('SELECT "group", listaCtts, caminhoXlsx FROM UserData WHERE user = ?', (usuario_selecionado,))
        dados_usuario = cursor.fetchone()
        cursor.close()

        if dados_usuario:
            self.cttNomeEdit.setText(dados_usuario[0])
            self.listaContatosEdit.setText(dados_usuario[2])
    def cadastrarUsuario(self):
        novo_usuario = self.novoUsuarioEdit.text()
        if novo_usuario:
            cursor = conectar.cursor()
            cursor.execute("INSERT INTO UserData (user) VALUES (?)", (novo_usuario,))
            conectar.commit()
            cursor.close()
            self.usuariosComboBox.addItem(novo_usuario)
            self.novoUsuarioEdit.clear()

    def open_file_dialog(self, line_edit, file_filter):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self.window, "Select File", "", file_filter)
        if file_path:
            normalized_path = os.path.normpath(file_path)
            line_edit.setText(normalized_path)

    
    def abrirTela2(self):
        tela2.show()
        self.window.close()

    def merge_cells(self, row):
        
        first_name = row[f'{resultado[8]}'] if pd.notna(row[f'{resultado[8]}']) and str(row[f'{resultado[8]}']).strip() != '' else ''
        middle_name = row[f'{resultado[9]}'] if pd.notna(row[f'{resultado[9]}']) and str(row[f'{resultado[9]}']).strip() != '' else ''
        last_name = row[f'{resultado[10]}'] if pd.notna(row[f'{resultado[10]}']) and str(row[f'{resultado[10]}']).strip() != '' else ''
        return f"{first_name} {middle_name} {last_name}"

    def definirLista(self):
        
        df = pd.read_excel(f'{self.listaContatosEdit.text()}')
        self.listaCompleta = df.apply(self.merge_cells, axis=1).tolist()
        

            

            

    def clearTextMsg(self):
        self.msg.clear()

class Tela2(QMainWindow):
    def __init__(self, tela1):
        bot.tela1()
        super().__init__()

        self.setWindowTitle("Segunda Tela")
        self.setGeometry(200, 100, 650, 800)

        cursor = conectar.cursor()

        cursor.close()

        newMessageLabel = QtWidgets.QLabel("(CSS) New Message:", self)
        newMessageLabel.setGeometry(20, 30, 200, 20)
        self.newMessageEdit = QLineEdit("", self)
        self.newMessageEdit.setGeometry(20, 50, 400, 20)

        drawerArrowLabel = QtWidgets.QLabel("(XPATH) Drawer Arrow:", self)
        drawerArrowLabel.setGeometry(20, 80, 200, 20)
        self.drawerArrowEdit = QLineEdit("", self)
        self.drawerArrowEdit.setGeometry(20, 100, 400, 20)

        forwardLabel = QtWidgets.QLabel("(XPATH) Forward:", self)
        forwardLabel.setGeometry(20, 130, 200, 20)
        self.forwardEdit = QLineEdit("", self)
        self.forwardEdit.setGeometry(20, 150, 400, 20)

        checkBoxesLabel = QtWidgets.QLabel("(CSS) Check Boxes:", self)
        checkBoxesLabel.setGeometry(20, 180, 200, 20)
        self.checkBoxesEdit = QLineEdit("", self)
        self.checkBoxesEdit.setGeometry(20, 200, 400, 20)

        toFowardArrowLabel = QtWidgets.QLabel("(XPATH) To Forward Arrow:", self)
        toFowardArrowLabel.setGeometry(20, 230, 200, 20)
        self.toFowardArrowEdit = QLineEdit("", self)
        self.toFowardArrowEdit.setGeometry(20, 250, 400, 20)

        contactSearchLabel = QtWidgets.QLabel("(XPATH) Contact Search:", self)
        contactSearchLabel.setGeometry(20, 280, 200, 20)
        self.contactSearchEdit = QLineEdit("", self)
        self.contactSearchEdit.setGeometry(20, 300, 400, 20)

        cancelSearchLabel = QtWidgets.QLabel("(XPATH) Cancel Search:", self)
        cancelSearchLabel.setGeometry(20, 330, 200, 20)
        self.cancelSearchEdit = QLineEdit("", self)
        self.cancelSearchEdit.setGeometry(20, 350, 400, 20)

        sendButtonLabel = QtWidgets.QLabel("(XPATH) Send Button:", self)
        sendButtonLabel.setGeometry(20, 380, 200, 20)
        self.sendButtonEdit = QLineEdit("", self)
        self.sendButtonEdit.setGeometry(20, 400, 400, 20)

        celula1Label = QtWidgets.QLabel("Célula 1:", self)
        celula1Label.setGeometry(20, 430, 200, 20)
        self.celula1 = QLineEdit("", self)
        self.celula1.setGeometry(20, 450, 400, 20)

        celula2Label = QtWidgets.QLabel("Célula 2:", self)
        celula2Label.setGeometry(20, 480, 200, 20)
        self.celula2 = QLineEdit("", self)
        self.celula2.setGeometry(20, 500, 400, 20)

        celula3Label = QtWidgets.QLabel("Célula 3:", self)
        celula3Label.setGeometry(20, 530, 200, 20)
        self.celula3 = QLineEdit("", self)
        self.celula3.setGeometry(20, 550, 400, 20)

        classGpLabel = QtWidgets.QLabel("(CSS) Classe GP:", self)
        classGpLabel.setGeometry(20, 580, 200, 20)
        self.classGpEdit = QLineEdit("", self)
        self.classGpEdit.setGeometry(20, 600, 400, 20)

        sideBarLabel = QtWidgets.QLabel("(XPATH) Side Bar:", self)
        sideBarLabel.setGeometry(20, 630, 200, 20)
        self.sideBarEdit = QLineEdit("", self)
        self.sideBarEdit.setGeometry(20, 650, 400, 20)

        if resultado is not None:
            self.newMessageEdit.setText(resultado[0])
            self.drawerArrowEdit.setText(resultado[1])
            self.forwardEdit.setText(resultado[2])
            self.checkBoxesEdit.setText(resultado[3])
            self.toFowardArrowEdit.setText(resultado[4])
            self.contactSearchEdit.setText(resultado[5])
            self.cancelSearchEdit.setText(resultado[6])
            self.sendButtonEdit.setText(resultado[7])
            self.celula1.setText(resultado[8])
            self.celula2.setText(resultado[9])
            self.celula3.setText(resultado[10])
            self.classGpEdit.setText(resultado[11])
            self.sideBarEdit.setText(resultado[12])

        buttonDefinir = QPushButton("SALVAR", self)
        buttonDefinir.setGeometry(150, 700, 120, 30)
        buttonDefinir.clicked.connect(bot.CaminhosHtmldb)

        buttonVoltar = QPushButton("Voltar", self)
        buttonVoltar.setGeometry(20, 700, 120, 30)
        buttonVoltar.clicked.connect(self.voltarParaTela1)



    def voltarParaTela1(self):
        self.close()
        bot.window.show()

bot=zapbot()
window2 = QMainWindow()  
tela2 = Tela2(window2)    
bot.tela1()
if __name__ == '__main__':

    bot.window.show()
    app.exec()