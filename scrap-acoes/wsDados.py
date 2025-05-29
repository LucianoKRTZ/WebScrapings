import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys


def run_scraper():
    # Configurações do Chrome
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Executa em modo headless (sem abrir janela)

    # Caminho para o driver do Chrome (ajuste conforme necessário)
    service = Service(executable_path="/usr/local/bin/chromedriver")  # ajuste conforme o local do seu chromedriver

    # Inicializa o navegador
    driver = webdriver.Chrome(service=service, options=chrome_options)
    wait30 = WebDriverWait(driver, 30)


    try:
        # Exemplo de acesso a uma página
        #url = "https://statusinvest.com.br/"
        urlFii = "https://statusinvest.com.br/fundos-imobiliarios/hglg11"
        urlAcoes = "https://statusinvest.com.br/acoes/bbas3"
        driver.get(urlFii)
        try:
            wait30.until((EC.visibility_of_element_located((By.XPATH, "/html/body/div[19]/div/div/div[1]/button")))).click()
        except:
            pass
        # Exemplo de busca por elemento
        titulo = driver.find_element(By.TAG_NAME, "h1").text
        print("Título da página:", titulo)
    finally:
        time.sleep(30000)
        # Encerra o navegador
        driver.quit()

if __name__ == "__main__":
    run_scraper()