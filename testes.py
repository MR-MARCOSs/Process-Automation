from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# Configuração do webdriver
driver = webdriver.Chrome()
driver.get('https://web.whatsapp.com')

# Tempo para escanear o QR Code e abrir o WhatsApp Web
print("Por favor, escaneie o QR Code do WhatsApp Web.")
WebDriverWait(driver, 60).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "canvas[aria-label='Scan me!']"))
)

# Espera até que a página seja carregada completamente
WebDriverWait(driver, 60).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-testid='chat-list']"))
)

# Seleciona o contato desejado
contact_name = "Nome do Contato"  # Substitua pelo nome do contato
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
            EC.presence_of_element_located((By.XPATH, ".//span[@data-testid='menu']"))
        )
        context_menu_button.click()

        # Seleciona a opção 'Encaminhar'
        forward_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Encaminhar']"))
        )
        forward_option.click()

        # Marca todas as checkboxes
        checkboxes = driver.find_elements(By.XPATH, "//input[@type='checkbox' and @aria-label='teste']")
        for checkbox in checkboxes:
            checkbox.click()
        
        print("Mensagens encaminhadas com sucesso")
        break
    except Exception as e:
        print("Erro:", e)
        break

# Fecha o driver após a execução
driver.quit()
