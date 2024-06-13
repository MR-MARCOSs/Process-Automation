from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import traceback
from selenium.webdriver.common.action_chains import ActionChains
import time
import bs4
# Configure o WebDriver (neste caso, utilizando o ChromeDriver)

driver = webdriver.Chrome()

# Acesse o WhatsApp Web
driver.get("https://web.whatsapp.com")

# Espera até que o QR code seja escaneado e a página principal seja carregada
#WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-testid="chat-list-search"]')))
input("das")
titles_list = []

            # Encontrar a barra lateral uma vez
sidebar = driver.find_element(By.XPATH, f"//div[@id='pane-side']")

# Execute JavaScript para rolar a barra lateral
'''
while True:
    # Rolar a barra lateral
    driver.execute_script("arguments[0].scrollTop += 1000;", sidebar)
    time.sleep(2)  # Espere um pouco após rolar para que a página carregue
    
    # Encontre todos os elementos com a classe "_ak8q" na página atual
    titles = driver.find_elements(By.CSS_SELECTOR, f"._ak8q")

    # Extraia e imprima o texto desses elementos
    for title in titles:
        html = title.get_attribute("outerHTML")
        soup = bs4.BeautifulSoup(html, "html.parser")
        element = soup.find('span', class_='x1iyjqo2')
        if element:
            title_with_emojis = element['title']
            print(title_with_emojis)
            titles_list.append(title_with_emojis)

    # Verifique se chegou ao final da lista rolando
    end_of_list = driver.execute_script("return arguments[0].scrollHeight - arguments[0].scrollTop === arguments[0].clientHeight;", sidebar)
    if end_of_list:
        break

# Remova duplicatas e ordene a lista de títulos
lista_sem_repeticao = list(set(titles_list))
lista_sem_repeticao.sort()
'''
chat_name = "COMANDOS - JS"
chat = driver.find_element(By.XPATH, f"//span[@title='{chat_name}']")
chat.click()

# Espera até que o chat específico seja carregado
#WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-testid="conversation-info-header"]')))

# Encontra todas as mensagens que contêm o <span>===</span>
messages = driver.find_elements(By.CSS_SELECTOR, 'div.copyable-text span')
print(messages)

# Encontrar o índice da última mensagem contendo "==="
last_index = -1
for index, message in enumerate(messages):
    if '===' in message.get_attribute('innerHTML'):
        last_index = index

# Verificar se encontramos alguma mensagem com "==="
if last_index == -1:
    print("Nenhuma mensagem contendo '===' foi encontrada.")
else:
    # Processar mensagens após a última mensagem contendo "==="
    for message in messages[last_index+1:]:
        try:
            time.sleep(1.5)
            # Encontrar o elemento pai relevante
            parent_message = message.find_element(By.XPATH, './ancestor::div[contains(@class, "message-in") or contains(@class, "message-out")]')

            # Verificar se o ícone 'forward-chat' está presente
            forward_icon = parent_message.find_element(By.XPATH, './/span[@data-icon="forward-chat"]/..')
            #forward_icon = parent_message.find_element(By.XPATH, './/span[@aria-label="Menu de contexto"]/..')
            time.sleep(1.5)
            # Clicar no ícone 'forward-chat'
            forward_icon.click()
            
            # Espera até que a tela "encaminhar mensagem para" seja exibid
            for i in range[1:2]:
                time.sleep(1.5)
            # Seleciona os contatos a partir do segundo contato com class="_ak8q"
                caixa_pesquisa=driver.find_element(By.XPATH, 'div[aria-label="Caixa de texto de pesquisa"]')
                time.sleep(1.5)
                caixa_pesquisa.click()
                chat_name2 = "Testes"
                time.sleep(1.5)
                chat2 = driver.find_element(By.XPATH, f"//span[@title='{chat_name2}']")
                chat2.click()
                ActionChains(driver).send_keys('{chat_name}')
                time.sleep(1.5)
                chat2.click()
                chat_name2="Brilhuss Administrativo"
                


            # Clica no botão "Enviar"
            send_button = driver.find_element(By.CSS_SELECTOR, 'div[aria-label="Enviar"]')
            send_button.click()
        except Exception as e:
            print(f"Erro ao processar a mensagem: {e}")
            traceback.print_exc()