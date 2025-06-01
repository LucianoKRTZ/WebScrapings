import time
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium import webdriver

#######################
## variaveis globais ##
#######################
class Gemini:
    def __init__(self):
        self.url = None
        self.driver = None
        self.wait03 = None
        self.wait15 = None

    def iniciarDriver(self, url):
        try:
            self.chrome_options = Options()
            self.service = Service(executable_path="/usr/local/bin/chromedriver")  # ajuste conforme o local do seu chromedriver
            # self.chrome_options.add_argument("--headless")  # Se quiser headless, descomente
            # Inicializa o navegador com webdriver padrão
            self.driver = webdriver.Chrome(options=self.chrome_options, service=self.service)
            self.wait03 = WebDriverWait(self.driver, 3)
            self.wait15 = WebDriverWait(self.driver, 15)

            self.driver.get(url)
            # driver iniciado com sucesso
            return True
        except Exception as e:
            print(f"Erro ao iniciar driver: {e}")
            return False

    def executarPrompt(self, prompt):
        if prompt in ["", None]:
            return "O prompt informado é invalido!"
        
        driverIniciado = self.iniciarDriver("https://gemini.google.com/app")
        if driverIniciado:
            # Inserindo prompt na caixa de texto
            try:
                campoInput = self.wait15.until(EC.visibility_of_element_located((By.XPATH,'/html/body/chat-app/main/side-navigation-v2/bard-sidenav-container/bard-sidenav-content/div[2]/div/div[2]/chat-window/div/input-container/div/input-area-v2/div/div/div[1]/div/div/rich-textarea/div[1]/p')))
            except:
                try:
                    campoInput = self.wait15.until(EC.visibility_of_element_located((By.XPATH,'/html/body/chat-app/main/side-navigation-v2/mat-sidenav-container/mat-sidenav-content/div/div[2]/chat-window/div/input-container/div/input-area-v2/div/div/div[2]/div/div/rich-textarea/div[1]/p')))
                except:
                    return "Não foi possível localizar o campo de entrada do prompt."
            # campoInput = self.driver.find_element(By.XPATH,'/html/body/chat-app/main/side-navigation-v2/bard-sidenav-container/bard-sidenav-content/div[2]/div/div[2]/chat-window/div/input-container/div/input-area-v2/div/div/div[1]/div/div/rich-textarea/div[1]/p')
            # Limpa o campo antes de enviar (Ctrl+A e Backspace para <p>)
            # campoInput.send_keys(Keys.CONTROL, 'a')
            # campoInput.send_keys(Keys.BACKSPACE)
            time.sleep(2)
            self.driver.execute_script("arguments[0].innerText = arguments[1];", campoInput, prompt)
            # campoInput.send_keys(prompt)
            time.sleep(2)
            
            # Botao de "enviar" prompt
            self.driver.find_element(By.XPATH,'/html/body/chat-app/main/side-navigation-v2/mat-sidenav-container/mat-sidenav-content/div/div[2]/chat-window/div/input-container/div/input-area-v2/div/div/div[3]/div/div[2]/button').click()
            time.sleep(1)  # Pequeno delay para evitar duplo envio

            # Extraindo texto retornado do prompt
            try:
                self.wait15.until(EC.visibility_of_element_located((By.XPATH,'/html/body/chat-app/main/side-navigation-v2/mat-sidenav-container/mat-sidenav-content/div/div[2]/chat-window/div/chat-window-content/div[1]/infinite-scroller/div/model-response/div/response-container/div/div[2]/div/div/message-content')))
                time.sleep(30)
                resposta = self.driver.find_element(By.XPATH,'/html/body/chat-app/main/side-navigation-v2/mat-sidenav-container/mat-sidenav-content/div/div[2]/chat-window/div/chat-window-content/div[1]/infinite-scroller/div/model-response/div/response-container/div/div[2]/div/div/message-content').text
            except Exception as e:
                resposta = f"Não foi possível obter uma resposta válida do Gemini. Erro: {e}"

            self.fecharDriver()
            return resposta
    
    def fecharDriver(self):
        if self.driver:
            self.driver.quit()