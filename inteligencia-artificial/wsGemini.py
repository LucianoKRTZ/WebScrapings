import time
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'utils')))
from daoUtils import DaoUtils #type: ignore
daoUtils = DaoUtils()
#######################
## variaveis globais ##
#######################

pathDriver = 'C:\\__Programas__\\Drivers\\chromedriver\\chromedriver.exe'


class Gemini:
    def __init__(self):
        self.url = None
        self.driver = None
        self.wait03 = None
        self.wait15 = None

    def iniciarDriver(self, url):
        try:
            self.chrome_options = Options()
            self.chrome_options.add_argument("--incognito")
            self.chrome_options.add_argument("--disable-features=WelcomePage")
            self.chrome_options.add_argument("--disable-popup-blocking")
            self.chrome_options.add_argument("--disable-notifications")
            self.chrome_options.add_argument("--disable-infobars")
            self.chrome_options.add_argument("--disable-extensions")
            self.chrome_options.add_argument("--disable-save-password-bubble")
            self.chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            self.chrome_options.add_experimental_option("useAutomationExtension", False)
            self.service = Service(executable_path=pathDriver)  # ajuste conforme o local do seu chromedriver
            # self.chrome_options.add_argument("--headless")  # Se quiser headless, descomente
            # Inicializa o navegador com webdriver padrão
            self.driver = webdriver.Chrome(options=self.chrome_options, service=self.service)
            self.wait03 = WebDriverWait(self.driver, 3)
            self.wait05 = WebDriverWait(self.driver, 5)
            self.wait10 = WebDriverWait(self.driver, 10)
            self.wait15 = WebDriverWait(self.driver, 15)

            self.driver.get(url)
            # driver iniciado com sucesso
            return True
        except Exception as e:
            print(f"Erro ao iniciar driver: {e}")
            return False
        
    def login(self):
        usuario, senha = daoUtils.obterAcessos("gemini")

        self.wait03.until(EC.visibility_of_element_located((By.ID,'identifierId'))).send_keys(usuario)

        # btnAvancar
        self.driver.find_element(By.XPATH, '//button[.//span[text()="Avançar"]]').click()

        while True:
            try:
                inpSenha = self.wait05.until(EC.visibility_of_element_located((By.NAME,'Passwd')))

                time.sleep(2)
                inpSenha.send_keys(senha)
                self.driver.find_element(By.XPATH, '//button[.//span[text()="Avançar"]]').click()


                break
            except:
                time.sleep(1)
        
        time.sleep(3)

    def executarPrompt(self, prompt):
        if prompt in ["", None]:
            return "O prompt informado é invalido!"
        
        driverIniciado = self.iniciarDriver("https://accounts.google.com/v3/signin/identifier?continue=https%3A%2F%2Fgemini.google.com%2Fapp&ec=GAZAkgU&followup=https%3A%2F%2Fgemini.google.com%2Fapp&ifkv=AdBytiPdVBJROlebm20uWviF14oLIL9GszLFUdk9kTCyAqry4-Q7dAaaBa0ZPtzkzM2r33OZA3NMXw&passive=1209600&flowName=GlifWebSignIn&flowEntry=ServiceLogin&dsh=S-1657672176%3A1749568177419730")
        time.sleep(5)
        self.login()
        self.verificarSolicitacaoConfirmacao()

        try:
            self.wait05.until(EC.visibility_of_element_located((By.XPATH,'/html/body/chat-app/main/side-navigation-v2/mat-sidenav-container/mat-sidenav-content/div/div[2]/chat-window/div/input-container/condensed-tos-disclaimer/div/div[1]/button'))).click()
        except:
            try:
                self.wait05.until(EC.visibility_of_element_located((By.XPATH,'/html/body/div[7]/div[2]/div/mat-dialog-container/div/div/discovery-card-dialog/mat-dialog-actions/button[1]'))).click()
            except:
                pass

        try:
            self.wait05.until(EC.visibility_of_element_located((By.XPATH,'/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[2]/div/div/div/form/span/section[2]/div/div/section/div/div/div/ul/li[1]/div'))).click()
            input("Pressione Enter para continuar...")
        except:
            pass

        try:
            txtBoxLoginRapido = self.wait05.until(EC.visibility_of_element_located((By.XPATH,'/html/body/div/div[1]/div[2]/c-wiz/div/div[1]/div[2]/h1/span')))
            if txtBoxLoginRapido.text.lower() == 'login mais rápido':
                self.wait03.until(EC.visibility_of_element_located((By.XPATH,'/html/body/div/div[1]/div[2]/c-wiz/div/div[3]/div/div[2]/div/div/button'))).click()
        except:
            pass
        if driverIniciado:
            # Inserindo prompt na caixa de texto
            # try:
            #     campoInput = self.wait05.until(EC.visibility_of_element_located((By.XPATH,'/html/body/chat-app/main/side-navigation-v2/bard-sidenav-container/bard-sidenav-content/div[2]/div/div[2]/chat-window/div/input-container/div/input-area-v2/div/div/div[1]/div/div/rich-textarea/div[1]/p')))
            # except:
            #     try:
            campoInput = self.wait15.until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//div[@aria-label="Insira um comando aqui"]/p')
                )
            )
            #     except:
            #         return "Não foi possível localizar o campo de entrada do prompt."
            # campoInput = self.driver.find_element(By.XPATH,'/html/body/chat-app/main/side-navigation-v2/mat-sidenav-container/mat-sidenav-content/div/div[2]/chat-window/div/input-container/div/input-area-v2/div/div/div[2]/div/div/rich-textarea/div[1]/p')
            # Limpa o campo antes de enviar (Ctrl+A e Backspace para <p>)
            campoInput.send_keys(Keys.CONTROL, 'a')
            campoInput.send_keys(Keys.BACKSPACE)
            time.sleep(2)


            self.driver.execute_script("arguments[0].innerText = arguments[1];", campoInput, prompt)
            # campoInput.send_keys(prompt)
            while prompt.replace("\n","") not in campoInput.text:
                campoInput = self.driver.find_element(By.XPATH,'/html/body/chat-app/main/side-navigation-v2/mat-sidenav-container/mat-sidenav-content/div/div[2]/chat-window/div/input-container/div/input-area-v2/div/div/div[1]/div/div/rich-textarea/div[1]/p')
                time.sleep(1)
            time.sleep(5)  # delay para garantir que o prompt foi inserido corretamente
            # Botao de "enviar" prompt
            btnEnviar = self.wait15.until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//button[@aria-label="Enviar mensagem"]')
                )
            )
            btnEnviar.click()
            time.sleep(35)  # delay para evitar duplo envio e espera para resposta do Gemini

            # Extraindo texto retornado do prompt
            try:
                # Aguarda o elemento com a classe markdown aparecer
                self.wait15.until(
                    EC.visibility_of_element_located(
                        (By.XPATH, '//div[contains(@class, "markdown-main-panel")]')
                    )
                )
                resposta = ''
                tentativas = 0
                while len(resposta) < 500 and tentativas < 6:
                    time.sleep(10)
                    # Extrai o texto do elemento markdown principal
                    resposta = self.driver.find_element(
                        By.XPATH, '//div[contains(@class, "markdown-main-panel")]'
                    ).text
                    tentativas += 1
            except Exception as e:
                resposta = f"Não foi possível obter uma resposta válida do Gemini. Erro: {e}"

            self.fecharDriver()
            return resposta
    
    def verificarSolicitacaoConfirmacao(self):
        try:
            identificadorSpan = '//h1[.//span[text()="Confirme que é você"]]'
            self.wait10.until(EC.visibility_of_element_located((By.XPATH, identificadorSpan)))
            isVisible = self.driver.find_element(By.XPATH, identificadorSpan).is_displayed()
            while isVisible:
                print("    -> Solicitação de confirmação detectada. Aguardando confirmação...")
                time.sleep(5)
                isVisible = self.driver.find_element(By.XPATH, identificadorSpan).is_displayed()
        except:
            print(f"    -> Sem tela de confirmação de acesso!")
            print(f"    -> Acesso liberado!")

    def fecharDriver(self):
        if self.driver:
            self.driver.quit()