import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from tabulate import tabulate  # <-- Adicionado
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'inteligencia-artificial')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'utils')))
from utils import Utils
from wsGemini import Gemini  # <-- Importando o módulo wsDados
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
        "Ticker":url.split("/")[-1].upper(), #Ticker da acao ou FII consultado
        "Valor Atual":"0.0", #Valor atual de comercializacao da acao
        "Menor Valor":"0.0", #Menor valor de comercializacao da acao
        "Maior Valor":"0.0", #Maior valor de comercializacao da acao
        "P/VP":"0.0", #Preco sobre valor do patrimonio
        "Média de Dividendos (24m)":"0.0", #Rendimento mensal medio (dividendos)
        "segmento":"Não encontrado", #Segmento da acao ou FII
    }
    try:
        driver.get(url)
        verificarPropaganda()
        if 'acoes' in url:
            acao["Valor Atual"] = 'R$'+driver.find_element(By.XPATH,'/html/body/main/div[2]/div/div[1]/div/div[1]/div/div[1]/strong').text
            acao["Menor Valor"] = 'R$'+driver.find_element(By.XPATH,'/html/body/main/div[2]/div/div[1]/div/div[2]/div/div[1]/strong').text
            acao["Maior Valor"] = 'R$'+driver.find_element(By.XPATH,'/html/body/main/div[2]/div/div[1]/div/div[3]/div/div[1]/strong').text
            acao["P/VP"] = driver.find_element(By.XPATH,'/html/body/main/div[2]/div/div[8]/div[2]/div/div[1]/div/div[4]/div/div/strong').text
            acao["Média de Dividendos (24m)"] = 'R$'+driver.find_element(By.XPATH,'/html/body/main/div[3]/div/div[1]/div[2]/div[7]/div/div[1]/div[2]/div/div/strong').text                
            acao["segmento"] = driver.find_element(By.XPATH,'/html/body/main/div[5]/div[1]/div/div[3]/div/div[3]/div/div/div/a/strong').text
            if acao['Média de Dividendos (24m)'] == 'R$0,00':
                acao["Média de Dividendos (24m)"] = 'R$'+driver.find_element(By.XPATH,'/html/body/main/div[3]/div/div[1]/div[2]/div[7]/div/div[1]/div[1]/div/div/strong').text

        else:
            acao["Valor Atual"] = 'R$'+driver.find_element(By.XPATH,'/html/body/main/div[2]/div[1]/div[1]/div/div[1]/strong').text
            acao["Menor Valor"] = 'R$'+driver.find_element(By.XPATH,'/html/body/main/div[2]/div[1]/div[2]/div/div[1]/strong').text
            acao["Maior Valor"] = 'R$'+driver.find_element(By.XPATH,'/html/body/main/div[2]/div[1]/div[3]/div/div[1]/strong').text
            
            if '/fundos-imobiliarios/' in url:
                acao["P/VP"] = driver.find_element(By.XPATH,'/html/body/main/div[2]/div[5]/div/div[2]/div/div[1]/strong').text
                acao["Média de Dividendos (24m)"] = 'R$'+driver.find_element(By.XPATH,'/html/body/main/div[2]/div[6]/div/div/div[1]/div/div/strong').text
                acao["segmento"] = driver.find_element(By.XPATH,'/html/body/main/div[3]/div/div/div[2]/div/div[6]/div/div/strong').text
            elif '/fiagros/' in url:
                # Caso seja Fiagro o XPATH eh diferente para alguns campos
                acao["P/VP"] = driver.find_element(By.XPATH,'/html/body/main/div[2]/div[4]/div/div[2]/div/div[1]/strong').text
                acao["Média de Dividendos (24m)"] = 'R$'+driver.find_element(By.XPATH,'/html/body/main/div[2]/div[5]/div/div/div[1]/div/div/strong').text
                acao["segmento"] = driver.find_element(By.XPATH,'/html/body/main/div[4]/div/div/div[2]/div/div[6]/div/div/strong').text
    finally:
        try:
            acao['Média de Dividendos (24m)'] = 'R$'+str(round(float(acao['Média de Dividendos (24m)'].replace(',','.').replace('R$','')),2)).replace('.',',')
        except:
            pass
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
    instrucaoRecomendada = ''
    instrucaoDetalhada = ''
    
    for ticker in tickers:
        if len(ticker) > 6 or len(ticker) < 5:
            print(f"Ticker inválido: {ticker}. Deve ter entre 5 e 6 caracteres.")
            continue

        instrucaoRecomendada += f"   * **{ticker.upper()}:** [Recomendação: Comprar/Vender/Manter]\n"
        instrucaoDetalhada += f"   * **{ticker.upper()}:** [Recomendação: Comprar/Vender/Manter] - [Justificativa concisa baseada na análise.]\n"

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

    # Defina os cabeçalhos das colunas de acordo com as chaves dos seus dicionários
    headers = ["Ticker", "Valor Atual", "Menor Valor", "Maior Valor", "P/VP", "Média de Dividendos (24m)", "segmento"]

    # Preparar os dados para a tabela
    tabela_dados = []
    for item in dadosRaspados:
        linha = []
        for header in headers:
            valor = item.get(header, "")
            linha.append(valor)
        tabela_dados.append(linha)

    # Imprimir a tabela
    tabelaDados = tabulate(tabela_dados, headers=headers, tablefmt="html") 
    prompt = f"""
Você é um especialista em análise de investimentos e mercado financeiro. Sua tarefa é analisar os dados de ações fornecidos, buscar informações complementares no site Status Invest (statusinvest.com.br) para o contexto geral do mercado e para ações similares, e, com base nisso, fornecer uma recomendação de investimento clara e um resumo da análise.
**Dados de Ações para Análise:**
Considere a seguinte tabela de dados de ações:
{tabelaDados}
**Instruções para a IA:**
1.  **Análise dos Dados Fornecidos:**
    * Avalie cada ativo (ticker) com base nos dados presentes na tabela (`Valor Atual`, `Menor Valor`, `Maior Valor`, `P/VP`, `Média de Dividendos (24m)`, `segmento`).
    * Interprete o `P/VP` (Preço sobre Valor Patrimonial) para identificar se o ativo está sendo negociado acima ou abaixo do seu valor patrimonial.
    * Interprete o `Média de Dividendos (24m)` (Rendimento médio mensal 'dividendos') para cada ativo. Se `Média de Dividendos (24m)` for um cálculo ou abreviação interna, a IA pode inferir seu significado com base no contexto ou indicar uma suposição.
    * Considere a variação entre `Menor Valor` e `Maior Valor` para entender a volatilidade e o histórico de preços nas últimas 52 semanas.
2.  **Consulta e Análise de Dados Gerais do Status Invest:**
    * Para cada ticker listado, e para o contexto de cada segmento, consulte o site Status Invest para obter dados adicionais relevantes como:
        * Dividend Yield (DY).
        * Endividamento (Dívida Líquida/EBITDA).
        * Crescimento de Receita/Lucro.
        * Liquidez diária.
        * Notícias recentes e eventos relevantes.
    * Identifique e analise ações similares (do mesmo segmento ou com características de mercado semelhantes) às solicitadas no Status Invest. Compare os indicadores e o desempenho dessas ações com os da tabela fornecida.
3.  **Geração da Recomendação de Investimento:**
    * Com base na análise dos dados fornecidos e das informações complementares do Status Invest, forneça uma recomendação de investimento para o usuário.
    * A recomendação deve ser clara, concisa e orientada para o usuário final, indicando se é uma boa oportunidade de compra, venda ou manutenção, e por quê.
4.  **Resumo Geral da Análise:**
    * Crie um breve resumo que sintetize os principais pontos da análise, cobrindo tanto as ações solicitadas quanto as ações similares.
    * Destaque as conclusões mais importantes e os fatores-chave que influenciaram a recomendação.
**Formato da Resposta:**
Sua resposta deve ser estruturada da seguinte forma:
**1. Recomendação de Investimento:**
{instrucaoRecomendada}
**2. Resumo Geral da Análise:**
   [Breve parágrafo ou dois, resumindo as principais descobertas sobre as ações analisadas e o cenário de mercado, incluindo comparações com ações similares.]
**3. Detalhamento da recomendação de Investimento:**
{instrucaoDetalhada}
---
"""
    
    gemini = Gemini()
    utils = Utils()

    relatorioGemini = gemini.executarPrompt(prompt)
    
    print(prompt)
    print("\n\n\n")
    print(tabelaDados)
    print("\n\n\n")
    print(relatorioGemini)

    for ticker in tickers:
        relatorioGemini = relatorioGemini.replace(ticker.upper(), f"<b>{ticker.upper()}</b>")
        relatorioGemini = relatorioGemini.replace(ticker.lower(), f"<b>{ticker.upper()}</b>")
    
    relatorioGemini = relatorioGemini.replace("1. Recomendação de Investimento:","<br><h3>1. Recomendação de Investimento:</h3>").replace("2. Resumo Geral da Análise:","<br><h3>2. Resumo Geral da Análise:</h3>").replace("3. Detalhamento da recomendação de Investimento:","<br><h3>3. Detalhamento da recomendação de Investimento:</h3>").replace("3. Detalhamento da Recomendação de Investimento:","<br><h3>3. Detalhamento da Recomendação de Investimento:</h3>")

    relatorioEmail = f"""
<h2>Relatório gerado na data {time.strftime('%d/%m/%Y %H:%M:%S')}</h2>
<h3>
Esta é uma análise feita por IA, portanto pode conter erros.<br>
É recomendado que você verifique os fatos antes de qualquer movimentação financeira.<br>
Tendo consciência disso, o desenvolvedor do programa não se responsabiliza por qualquer erro ou prejuízo causado por este relatório.<br><br>
Boa leitura!
</h3>

<h2> → Dados extraídos do Status Invest:</h2>
{tabelaDados}


<h2> → Relatório gerado por IA (Gemini) com base nos dados extraídos:</h2>
{relatorioGemini.replace('\n','<br>')}

<h2> → Prompt utilizado para gerar o relatório</h2>
{prompt.replace('\n','<br>')}
"""
    utils.converterHTML2PDF(relatorioEmail,'/home/luciano/Área de trabalho/Relatorios/Acoes', f'Relatorio-IA-Acoes-{time.strftime("%d.%m.%Y")}')