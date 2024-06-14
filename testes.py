from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# Configuração do webdriver
driver = webdriver.Firefox()
driver.get('https://web.whatsapp.com')

# Tempo para escanear o QR Code e abrir o WhatsApp Web
input("asd")

# Espera até que a página seja carregada completamente

# Seleciona o contato desejado
contact_name = "COMANDOS - JS"  # Substitua pelo nome do contato
contact = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((By.XPATH, f"//span[@title='{contact_name}']"))
)
contact.click()

# Espera e monitorar por mensagens novas
while True:
    try:
        # Espera até que uma nova mensagem apareça
        new_message = WebDriverWait(driver, 600).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.copyable-text[data-pre-plain-text]"))
        )
        print("Nova mensagem recebida")

        # Move o mouse para a mensagem para exibir o menu de contexto
        ActionChains(driver).move_to_element(new_message).perform()

        # Espera até que o botão do menu de contexto esteja presente
        context_menu_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, ".//div[@aria-label='Menu de contexto']"))
        )
        context_menu_button.click()

        # Seleciona a opção 'Encaminhar'
        forward_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Encaminhar']"))
        )
        forward_option.click()

        checkboxes = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input[type='checkbox']"))
        )

        # Marca todas as checkboxes não marcadas
        for checkbox in checkboxes:
            if not checkbox.is_selected():
                driver.execute_script("arguments[0].scrollIntoView();", checkbox)
                driver.execute_script("arguments[0].click();", checkbox)

        print("Mensagens encaminhadas com sucesso")
        break
    except Exception as e:
        print("Erro:", e)
        break