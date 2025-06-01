import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from tabulate import tabulate  # <-- Adicionado

#######################
## variaveis globais ##
#######################
urlFii = "https://statusinvest.com.br/fundos-imobiliarios/"
urlFiagros = "https://statusinvest.com.br/fiagros/"
urlAcoes = "https://statusinvest.com.br/acoes/"

# Configurações do Chrome
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Executa em modo headless (sem abrir janela)
# Caminho para o driver do Chrome (ajuste conforme necessário)
service = Service(executable_path="/usr/local/bin/chromedriver")  # ajuste conforme o local do seu chromedriver
# Inicializa o navegador
driver = webdriver.Chrome(service=service, options=chrome_options)
wait03 = WebDriverWait(driver, 3)
wait15 = WebDriverWait(driver, 15)

def verificarPropaganda():
    for i in range(4):
        try:
            WebDriverWait(driver,0.5).until((EC.visibility_of_element_located((By.XPATH, "/html/body/header/nav/div"))))
            break
        except:
            wait03.until((EC.visibility_of_element_located((By.XPATH, "/html/body/div[19]/div/div/div[1]/button")))).click()

def rasparDados(url):
    acao = {
        "ticker":url.split("/")[-1].upper(), #Ticker da acao ou FII consultado
        "valorAtual":"0.0", #Valor atual de comercializacao da acao
        "MenorValor":"0.0", #Menor valor de comercializacao da acao
        "MaiorValor":"0.0", #Maior valor de comercializacao da acao
        "pvp":"0.0", #Preco sobre valor do patrimonio
        "rmm":"0.0", #Rendimento mensal medio (dividendos)
        "segmento":"Não encontrado", #Segmento da acao ou FII
    }
    try:
        driver.get(url)
        verificarPropaganda()
        if 'acoes' in url:
            acao["valorAtual"] = driver.find_element(By.XPATH,'/html/body/main/div[2]/div/div[1]/div/div[1]/div/div[1]/strong').text
            acao["MenorValor"] = driver.find_element(By.XPATH,'/html/body/main/div[2]/div/div[1]/div/div[2]/div/div[1]/strong').text
            acao["MaiorValor"] = driver.find_element(By.XPATH,'/html/body/main/div[2]/div/div[1]/div/div[3]/div/div[1]/strong').text
            acao["pvp"] = driver.find_element(By.XPATH,'/html/body/main/div[2]/div/div[8]/div[2]/div/div[1]/div/div[4]/div/div/strong').text
            acao["rmm"] = driver.find_element(By.XPATH,'/html/body/main/div[3]/div/div[1]/div[2]/div[7]/div/div[1]/div[2]/div/div/strong').text                
            acao["segmento"] = driver.find_element(By.XPATH,'/html/body/main/div[5]/div[1]/div/div[3]/div/div[3]/div/div/div/a/strong').text
            if acao['rmm'] == '0,00':
                acao["rmm"] = driver.find_element(By.XPATH,'/html/body/main/div[3]/div/div[1]/div[2]/div[7]/div/div[1]/div[1]/div/div/strong').text

        else:
            acao["valorAtual"] = driver.find_element(By.XPATH,'/html/body/main/div[2]/div[1]/div[1]/div/div[1]/strong').text
            acao["MenorValor"] = driver.find_element(By.XPATH,'/html/body/main/div[2]/div[1]/div[2]/div/div[1]/strong').text
            acao["MaiorValor"] = driver.find_element(By.XPATH,'/html/body/main/div[2]/div[1]/div[3]/div/div[1]/strong').text
            
            if '/fundos-imobiliarios/' in url:
                acao["pvp"] = driver.find_element(By.XPATH,'/html/body/main/div[2]/div[5]/div/div[2]/div/div[1]/strong').text
                acao["rmm"] = driver.find_element(By.XPATH,'/html/body/main/div[2]/div[6]/div/div/div[1]/div/div/strong').text
                acao["segmento"] = driver.find_element(By.XPATH,'/html/body/main/div[3]/div/div/div[2]/div/div[6]/div/div/strong').text
            elif '/fiagros/' in url:
                # Caso seja Fiagro o XPATH eh diferente para alguns campos
                acao["pvp"] = driver.find_element(By.XPATH,'/html/body/main/div[2]/div[4]/div/div[2]/div/div[1]/strong').text
                acao["rmm"] = driver.find_element(By.XPATH,'/html/body/main/div[2]/div[5]/div/div/div[1]/div/div/strong').text
                acao["segmento"] = driver.find_element(By.XPATH,'/html/body/main/div[4]/div/div/div[2]/div/div[6]/div/div/strong').text
    finally:
        return acao
    
def verificarPaginaFii(url):
    """
    Verifica se a página carregada eh a correta do FII ou se eh Fiagro.
    Retorna True se a pagina for do FII consultado e False se for Fiagro ou a pagina for inexistente.
    """
    driver.get(url)
    try:
        headerTicker = wait03.until((EC.visibility_of_element_located((By.XPATH, "/html/body/main/header/div[2]/div/div[1]/h1")))) # verifica se a pagina carregada eh do FII ou eh Fiagro
        if url.lower().endswith(headerTicker.text.split(" ")[0].lower()):
            return True
        else:
            return False
    except:
        #Header do ticker inexistente (pagina de ticker nao localizado)
        return False
    
if __name__ == "__main__":
    dadosRaspados = []
    # inpTickers = input("\n\nDigite os tickers das ações e FIIs separados por vírgulas: ")
    inpTickers = 'hglg11, snag11, mxrf11, bbas3, bbse3, taee4, alup3' # dados mocados para fins de teste
    tickers = [ticker.lower().replace(' ','') for ticker in inpTickers.split(",")]
    for ticker in tickers:
        if len(ticker) > 6 or len(ticker) < 5:
            print(f"Ticker inválido: {ticker}. Deve ter entre 5 e 6 caracteres.")
            continue
        if ticker.endswith('11'):
            url = urlFii + ticker
            if not verificarPaginaFii(url):
                url = urlFiagros + ticker
            
            dadosRaspados.append(rasparDados(url))
        else:
            url = urlAcoes + ticker
            dadosRaspados.append(rasparDados(url))
        time.sleep(1)
    driver.quit()

    # --- Formato de Tabela (tabulate) ---
    print("\n\n--- Formato de Tabela ---")

    # Defina os cabeçalhos das colunas de acordo com as chaves dos seus dicionários
    headers = ["ticker", "valorAtual", "MenorValor", "MaiorValor", "pvp", "rmm", "segmento"]

    # Preparar os dados para a tabela
    tabela_dados = []
    for item in dadosRaspados:
        linha = []
        for header in headers:
            valor = item.get(header, "")
            linha.append(valor)
        tabela_dados.append(linha)

    # Imprimir a tabela
    print(tabulate(tabela_dados, headers=headers, tablefmt="grid"))