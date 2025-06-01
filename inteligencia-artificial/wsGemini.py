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
            campoInput.send_keys(Keys.CONTROL, 'a')
            campoInput.send_keys(Keys.BACKSPACE)
            time.sleep(0.5)
            self.driver.execute_script("arguments[0].innerText = arguments[1];", campoInput, prompt)
            # campoInput.send_keys(prompt)
            time.sleep(0.5)
            
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
            return resposta
    
    def fecharDriver(self):
        if self.driver:
            self.driver.quit()

if __name__ == "__main__":
    gemini = Gemini()
    prompt = """
Você é um especialista em análise de investimentos e mercado financeiro. Sua tarefa é analisar os dados de ações fornecidos, buscar informações complementares no site Status Invest (statusinvest.com.br) para o contexto geral do mercado e para ações similares, e, com base nisso, fornecer uma recomendação de investimento clara e um resumo da análise.
**Dados de Ações para Análise:**
Considere a seguinte tabela de dados de ações:
+----------+--------------+--------------+--------------+-------+------------+------------------+
| ticker   | valorAtual   | MenorValor   | MaiorValor   | pvp   | rmm        | segmento         |
+==========+==============+==============+==============+=======+============+==================+
| HGLG11   | 161,21       | 137,76       | 161,21       | 0,99  | 1,10000000 | Logística        |
+----------+--------------+--------------+--------------+-------+------------+------------------+
| SNAG11   | 9,70         | 8,13         | 9,70         | 0,95  | 0,10675000 | Híbrido          |
+----------+--------------+--------------+--------------+-------+------------+------------------+
| MXRF11   | 9,57         | 8,41         | 9,63         | 1,02  | 0,10142857 | Híbrido          |
+----------+--------------+--------------+--------------+-------+------------+------------------+
| BBAS3    | 23,40        | 22,79        | 29,76        | 0,74  | 0,6404     | Bancos           |
+----------+--------------+--------------+--------------+-------+------------+------------------+
| BBSE3    | 37,74        | 29,19        | 42,77        | 6,47  | 2,3202     | Seguradoras      |
+----------+--------------+--------------+--------------+-------+------------+------------------+
| TAEE4    | 11,90        | 10,36        | 12,15        | 1,69  | 0,4739     | Energia Elétrica |
+----------+--------------+--------------+--------------+-------+------------+------------------+
| ALUP3    | 11,05        | 8,34         | 11,05        | 1,28  | 0,1500     | Energia Elétrica |
+----------+--------------+--------------+--------------+-------+------------+------------------+
Sendo MenorValor e MaiorValor os valores de negociação mais baixo e mais alto do ativo nas ultimas 52 semanas, respectivamente, e rmm a remuneração (dividendos) médios mensais.
**Instruções para a IA:**
1.  **Análise dos Dados Fornecidos:**
    * Avalie cada ativo (ticker) com base nos dados presentes na tabela (`valorAtual`, `MenorValor`, `MaiorValor`, `pvp`, `rmm`, `segmento`).
    * Interprete o `pvp` (Preço sobre Valor Patrimonial) para identificar se o ativo está sendo negociado acima ou abaixo do seu valor patrimonial.
    * Interprete o `rmm` (não especificado, mas assumido como um indicador de rentabilidade ou risco) para cada ativo. Se `rmm` for um cálculo ou abreviação interna, a IA pode inferir seu significado com base no contexto ou indicar uma suposição.
    * Considere a variação entre `MenorValor` e `MaiorValor` para entender a volatilidade e o histórico de preços.
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
**1. Resumo Geral da Análise:**
   [Breve parágrafo ou dois, resumindo as principais descobertas sobre as ações analisadas e o cenário de mercado, incluindo comparações com ações similares.]
**2. Recomendação de Investimento:**
   * **HGLG11:** [Recomendação: Comprar/Vender/Manter] - [Justificativa concisa baseada na análise.]
   * **SNAG11:** [Recomendação: Comprar/Vender/Manter] - [Justificativa concisa baseada na análise.]
   * **MXRF11:** [Recomendação: Comprar/Vender/Manter] - [Justificativa concisa baseada na análise.]
   * **BBAS3:** [Recomendação: Comprar/Vender/Manter] - [Justificativa concisa baseada na análise.]
   * **BBSE3:** [Recomendação: Comprar/Vender/Manter] - [Justificativa concisa baseada na análise.]
   * **TAEE4:** [Recomendação: Comprar/Vender/Manter] - [Justificativa concisa baseada na análise.]
   * **ALUP3:** [Recomendação: Comprar/Vender/Manter] - [Justificativa concisa baseada na análise.]
"""
    resposta = gemini.executarPrompt(prompt)
    print(resposta)
    gemini.fecharDriver()