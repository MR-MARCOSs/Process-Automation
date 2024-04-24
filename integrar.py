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
from PyQt6.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QMessageBox, QCheckBox, QVBoxLayout, QWidget, QLabel, QFileDialog

from PyQt6 import QtWidgets
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
hoje = datetime.datetime.now()
dataFormatada = hoje.strftime('%d_%m_%Y')
conectar = sqlite3.connect('banco.db')
cursor = conectar.cursor()
cursor.execute("CREATE TABLE if not exists UserData (listaCtts text, chat text, caminhoImg text, caminhoXlsx text)")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS CaminhosHtml (
        chatEdit TEXT,
        campoEscrever TEXT,
        clipCaminho TEXT,
        receberImg TEXT,
        botaoEnviar TEXT,
        cancelarPesq TEXT,
        celula1 TEXT,
        celula2 TEXT,
        celula3 TEXT,
        classGp TEXT,
        barraLateral TEXT
    )
""")
cursor.execute("SELECT chatEdit, campoEscrever, clipCaminho, receberImg, botaoEnviar, cancelarPesq, celula1, celula2, celula3, classGp, barraLateral FROM CaminhosHtml")
resultado = cursor.fetchone()
conectar.commit()
cursor.close()

app = QApplication([])

class zapbot:
    def UserDatadb(self):
        if self.checkboxXl.isChecked():
            bot.definirLista()
        if self.checkboxGp.isChecked():
            bot.abrirZap()
            time.sleep(15)
            titles_list = []

            # Encontrar a barra lateral uma vez
            sidebar = self.driver.find_element(By.XPATH, "//div[@id='pane-side']")

            # Execute JavaScript para rolar a barra lateral
            while True:
                # Rolar a barra lateral
                self.driver.execute_script("arguments[0].scrollTop += 1000;", sidebar)
                time.sleep(2)  # Espere um pouco após rolar para que a página carregue
                
                # Encontre todos os elementos com a classe "_ak8q" na página atual
                titles = self.driver.find_elements(By.CSS_SELECTOR, f"{resultado[9]}")

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
        cursor.execute("DELETE FROM UserData")


        cursor.execute("""INSERT INTO UserData VALUES (:listaCtts, :chat, :caminhoImg, :caminhoXlsx)""",
            {
                'listaCtts': (listaSerializada if (self.checkboxXl.isChecked() and not self.checkboxGp.isChecked())
                             else (listaGps if (self.checkboxGp.isChecked() and not self.checkboxXl.isChecked())
                                   else [listaSerializada, listaGps])),
                'chat':self.msg.toPlainText(),
                'caminhoImg':self.ImgCaminho.text(),
                'caminhoXlsx':self.listaContatosEdit.text(),# if self.checkboxXl.isChecked() else "",
            })

        cursor.execute("SELECT listaCtts FROM UserData")
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
                chatEdit, campoEscrever, clipCaminho, receberImg, botaoEnviar,
                cancelarPesq, celula1, celula2, celula3, classGp, barraLateral
            ) VALUES (
                :chatEdit, :campoEscrever, :clipCaminho, :receberImg, :botaoEnviar,
                :cancelarPesq, :celula1, :celula2, :celula3, :classGp, :barraLateral
            )
        """, {
            'chatEdit': tela2.chatEdit.text(),
            'campoEscrever': tela2.campoEscrever.text(),
            'clipCaminho': tela2.clipCaminho.text(),
            'receberImg': tela2.receberImg.text(),
            'botaoEnviar': tela2.botaoEnviar.text(),
            'cancelarPesq': tela2.cancelarPesq.text(),
            'celula1': tela2.celula1.text(),
            'celula2': tela2.celula2.text(),
            'celula3': tela2.celula3.text(),
            'classGp': tela2.classeCtt.text(),
            'barraLateral': self.lateral.text(), # Substitua isso pelo valor real da barra lateral
        })
        conectar.commit()
        cursor.close()

    def abrirZap(self):
        self.nomeArquivo = f'meu_arquivo_{dataFormatada}.txt'
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
    def disparar(self):
        time.sleep(25)



        erru=0
        while len(self.listaCtts) >= 1:
            try:
                WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, f'{resultado[0]}')))
                time.sleep(1)
                conv=self.driver.find_element(By.XPATH, f'{resultado[0]}')
                conv.click()
                time.sleep(1)
                ActionChains(self.driver).send_keys(self.listaCtts[0]).perform()
                time.sleep(1)
                contato = self.driver.find_element(By.XPATH, f'//span[@title="{self.listaCtts[0]}"]')
                time.sleep(1)
                contato.click()
                time.sleep(1)
                WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located((By.XPATH, f'{resultado[1]}')))
                chat = self.driver.find_element(By.XPATH, f'{resultado[1]}')
                time.sleep(1)
                chat.click()
                time.sleep(1)
                ActionChains(self.driver).send_keys(self.msg.toPlainText()).perform()
                time.sleep(5.5)
                ActionChains(self.driver).send_keys(Keys.RETURN).perform()
                #self.armazenado[4]+=1
                #bot.Continuar()
                if self.ImgCaminho.text()!="":
                    WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, f'{resultado[2]}')))
                    clip = self.driver.find_element(By.XPATH, f"{resultado[2]}")
                    clip.click()
                    WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, f"{resultado[3]}")))
                    time.sleep(1)
                    attach = self.driver.find_element(By.CSS_SELECTOR, f"{resultado[3]}")
                    time.sleep(1)
                    attach.send_keys(self.ImgCaminho.text())
                    time.sleep(2)
                    WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, f'{resultado[4]}')))
                    send = self.driver.find_element(By.XPATH, f'{resultado[4]}')
                    send.click()

                del self.listaCtts[0]
 
            except:               
                try:
                    with open(self.nomeArquivo, 'a', encoding='utf-8') as arquivo:
                        arquivo.write(f'{self.listaCtts[0]}\n')
                    time.sleep(1)
                    WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, f'{resultado[5]}')))
                    apaga=self.driver.find_element(By.XPATH, f'{resultado[5]}')
                    apaga.click()
                    erru=erru+1
                    del self.listaCtts[0]
                except:
                    erru=erru+1
                    del self.listaCtts[0]
        with open(self.nomeArquivo, 'a') as arquivo:
            arquivo.write(f'Total de erros: {erru}')

    def tela1(self):
        self.window = QtWidgets.QWidget()
        self.window.setGeometry(100, 100, 570, 500)
        self.window.setWindowTitle("Tela 1")

        cursor = conectar.cursor()
        cursor.execute("SELECT listaCtts, chat, caminhoImg, caminhoXlsx FROM UserData")
        self.armazenado = cursor.fetchone()
        cursor.close()
        #self.armazenado = list(self.armazenado)

        listaContatosLabel = QtWidgets.QLabel("Arquivo excel:", self.window)
        listaContatosLabel.setGeometry(20,20,200,20)
        self.listaContatosEdit = QtWidgets.QLineEdit("", self.window)
        self.listaContatosEdit.setGeometry(20, 40, 400, 40)
        self.listaContatosButton = QtWidgets.QPushButton("Select File", self.window)
        self.listaContatosButton.setGeometry(440, 40, 100, 40)
        self.listaContatosButton.clicked.connect(lambda: self.open_file_dialog(self.listaContatosEdit, "Excel Files (*.xlsx)"))


        buttonClearCtt = QPushButton("Definir lista do excel", self.window)
        buttonClearCtt.setGeometry(20, 100, 120, 30)
        buttonClearCtt.clicked.connect(self.definirLista)

        msgLabel = QtWidgets.QLabel("Mensagem desejada:", self.window)
        msgLabel.setGeometry(20,150,200,20)
        self.msg = QtWidgets.QTextEdit("", self.window)
        self.msg.setGeometry(20,170,400,60)

        buttonClearMsg = QPushButton("Limpar Msg", self.window)
        buttonClearMsg.setGeometry(20, 240, 120, 30)
        buttonClearMsg.clicked.connect(self.clearTextMsg)

        caminhoImgLabel = QtWidgets.QLabel("Caminho de imagem:", self.window)
        caminhoImgLabel.setGeometry(20,290,250,20)
        self.ImgCaminho = QtWidgets.QLineEdit("", self.window)
        self.ImgCaminho.setGeometry(20, 310, 400, 20)
        self.ImgCaminhoButton = QtWidgets.QPushButton("Select File", self.window)
        self.ImgCaminhoButton.setGeometry(440, 310, 100, 20)
        self.ImgCaminhoButton.clicked.connect(lambda: self.open_file_dialog(self.ImgCaminho, "Image Files (*.jpg *.jpeg *.png)"))


        if self.armazenado is not None:
            self.listaContatosEdit.setText(self.armazenado[3])
            self.msg.setText(self.armazenado[1])
            self.ImgCaminho.setText(self.armazenado[2])

        button = QPushButton("MODIFICAR", self.window)
        button.setGeometry(20, 410, 120, 30)
        button.clicked.connect(self.abrirTela2)

       

        #self.checkbox = QCheckBox("Continuar de onde parou", self.window)
       
        #self.checkbox.setGeometry(20, 380, 300, 30)
     
        self.checkboxXl = QCheckBox("Usar caminho do Excel", self.window)
        self.checkboxXl.setGeometry(20, 350, 300, 30)

        self.checkboxGp = QCheckBox("Extrair contatos", self.window)
        self.checkboxGp.setGeometry(20, 370, 300, 30)

        buttonDisparar = QPushButton("DISPARAR", self.window)
        buttonDisparar.setGeometry(150, 410, 120, 30)
        buttonDisparar.clicked.connect(self.UserDatadb)

    def open_file_dialog(self, line_edit, file_filter):
        file_path, _ = QFileDialog.getOpenFileName(self.window, "Select File", "", file_filter)
        if file_path:
            line_edit.setText(file_path)
    
    def abrirTela2(self):
        tela2.show()
        self.window.close()

    def merge_cells(self, row):
        
        first_name = row[f'{resultado[6]}'] if pd.notna(row[f'{resultado[6]}']) and str(row[f'{resultado[6]}']).strip() != '' else ''
        middle_name = row[f'{resultado[7]}'] if pd.notna(row[f'{resultado[7]}']) and str(row[f'{resultado[7]}']).strip() != '' else ''
        last_name = row[f'{resultado[8]}'] if pd.notna(row[f'{resultado[8]}']) and str(row[f'{resultado[8]}']).strip() != '' else ''
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
        self.setGeometry(200, 200, 650, 650)

        cursor = conectar.cursor()

        cursor.close()

        chatLabel = QtWidgets.QLabel("CHAT LIST CSS:", self)
        chatLabel.setGeometry(20,130,200,20)
        self.chatEdit = QLineEdit("", self)
        self.chatEdit.setGeometry(20,150, 400,20)

        escreverLabel = QtWidgets.QLabel("CAMPO ESCREVER CSS:", self)
        escreverLabel.setGeometry(20,180,200,20)
        self.campoEscrever = QLineEdit("", self)
        self.campoEscrever.setGeometry(20,200,400,20)

        clipLabel = QtWidgets.QLabel("CLIP ENVIAR CSS:", self)
        clipLabel.setGeometry(20,230,250,20)
        self.clipCaminho = QLineEdit("", self)
        self.clipCaminho.setGeometry(20,250,400,20)

        receberLabel = QtWidgets.QLabel("INPUT FILE CSS:", self)
        receberLabel.setGeometry(20,280,250,20)
        self.receberImg = QLineEdit("", self)
        self.receberImg.setGeometry(20,300,400,20)

        botaoEnviarLabel = QtWidgets.QLabel("BOTÃO ENVIAR XPATH:", self)
        botaoEnviarLabel.setGeometry(20,330,250,20)
        self.botaoEnviar = QLineEdit("", self)
        self.botaoEnviar.setGeometry(20,350,400,20)

        cancelarLabel = QtWidgets.QLabel("CANCELAR PESQUISA XPATH:", self)
        cancelarLabel.setGeometry(20,380,250,20)
        self.cancelarPesq = QLineEdit("", self)
        self.cancelarPesq.setGeometry(20,400,400,20)

        celula1Label = QtWidgets.QLabel("Célula 1:", self)
        celula1Label.setGeometry(20,450,250,20)
        self.celula1 = QLineEdit("", self)
        self.celula1.setGeometry(20,470,400,20)

        celula2Label = QtWidgets.QLabel("Célula 2:", self)
        celula2Label.setGeometry(20,500,250,20)
        self.celula2 = QLineEdit("", self)
        self.celula2.setGeometry(20,520,400,20)

        celula3Label = QtWidgets.QLabel("Célula 3:", self)
        celula3Label.setGeometry(20,550,250,20)
        self.celula3 = QLineEdit("", self)
        self.celula3.setGeometry(20,570,400,20)

        classeCttLabel = QtWidgets.QLabel("Classe contato CSS:", self)
        classeCttLabel.setGeometry(20,600,250,20)
        self.classeCtt = QLineEdit("", self)
        self.classeCtt.setGeometry(20,620,400,20)

        classeLateral = QtWidgets.QLabel("Barra lateral XPATH:", self)
        classeLateral.setGeometry(20,650,250,20)
        self.lateral = QLineEdit("", self)
        self.lateral.setGeometry(20,670,400,20)

        if resultado is not None:
            self.chatEdit.setText(resultado[0])
            self.campoEscrever.setText(resultado[1])
            self.clipCaminho.setText(resultado[2])
            self.receberImg.setText(resultado[3])
            self.botaoEnviar.setText(resultado[4])
            self.cancelarPesq.setText(resultado[5])
            self.celula1.setText(resultado[6])
            self.celula2.setText(resultado[7])
            self.celula3.setText(resultado[8])
            self.classeCtt.setText(resultado[9])



        buttonDefinir = QPushButton("SALVAR", self)
        buttonDefinir.setGeometry(150,650, 120, 30)
        buttonDefinir.clicked.connect(bot.CaminhosHtmldb)

        buttonVoltar = QPushButton("Voltar", self)
        buttonVoltar.setGeometry(20,650, 120, 30)
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