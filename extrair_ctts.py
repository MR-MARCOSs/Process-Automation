# coding=utf8
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Inicialize o WebDriver
driver = webdriver.Chrome()  # Ou o navegador de sua escolha

# Abra o WhatsApp Web
driver.get("https://web.whatsapp.com/")
time.sleep(10)
input("Pressione Enter depois de fazer login manualmente")

# Lista para armazenar os títulos encontrados
titles_list = []

# Encontrar a barra lateral uma vez
sidebar = driver.find_element(By.XPATH, "//div[@id='pane-side']")

# Execute JavaScript para rolar a barra lateral
while True:
    # Rolar a barra lateral
    driver.execute_script("arguments[0].scrollTop += 1000;", sidebar)
    time.sleep(2)  # Espere um pouco após rolar para que a página carregue
    
    # Encontre todos os elementos com a classe "_ak8q" na página atual
    titles = driver.find_elements(By.CSS_SELECTOR, "._ak8q")

    # Extraia e imprima o texto desses elementos
    for title in titles:
        #print(title.text)
        titles_list.append(title.text)
    
    # Verifique se chegou ao final da lista rolando
    end_of_list = driver.execute_script("return arguments[0].scrollHeight - arguments[0].scrollTop === arguments[0].clientHeight;", sidebar)
    if end_of_list:

        break

lista_sem_repeticao = list(set(titles_list))
# Imprima os títulos encontrados
for title in titles_list:
    print(title)

def contar_elementos_repetidos(lista):
    contador = {}
    for elemento in lista_sem_repeticao:
        if elemento in contador:
            contador[elemento] += 1
        else:
            contador[elemento] = 1
    repetidos = {chave: valor for chave, valor in contador.items() if valor > 1}
    return repetidos


elementos_repetidos = contar_elementos_repetidos(lista_sem_repeticao)
print("Elementos repetidos na lista e suas contagens:")
for elemento, contagem in elementos_repetidos.items():
    print(f"{elemento}: {contagem}")

print("\n\n\n")
print(lista_sem_repeticao)
# Feche o navegador
driver.quit()
    # Encontre todos os elementos com a classe "_ak8q" na página atual