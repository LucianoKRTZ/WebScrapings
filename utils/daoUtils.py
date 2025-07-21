import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd
from weasyprint import HTML
from pathlib import Path
from datetime import datetime
import os

pathAcessos = "C:\\__Programas__\\__config__\\acessos.xlsx"
pathOutput = "C:\\Macros\\Acoes"

data = datetime.today()

class DaoUtils:
    def obterAcessos(self, plataforma):
        excel = pd.read_excel(pathAcessos, sheet_name='acessos')
        for linha in excel.itertuples():
            if linha[1] == plataforma:
                usuario = linha[2]
                senha = linha[3]

        return usuario, senha
    
    def obterDestinatarioEmail(self, programa):
        excel = pd.read_excel(pathAcessos, sheet_name='destinatarios')
        destinatarios = []
        for linha in excel.itertuples():
            if linha[1] == programa:
                destinatarios.append(linha[3])
        return destinatarios

    def organizarPastaMacroAcoes(self):
        print(f"\n\n\n=> Organizando arquivos na pasta: {pathOutput}")

        for arq in os.listdir(pathOutput):
            pathArq = os.path.join(pathOutput, arq)
            if os.path.isfile(pathArq):
                print(f"    ->Organizando arquivo: {arq}")

                dataArq = arq.split('-')[-1].replace('.'+arq.split('.')[-1],'')
                dataArq = datetime.strptime(dataArq, '%d.%m.%Y')

                if dataArq.__format__('%d%m%Y') != data.__format__('%d%m%Y'):
                    pathDst = os.path.join(pathOutput, dataArq.strftime('%Y'), dataArq.strftime('%m'))
                    if not os.path.exists(pathDst):
                        os.makedirs(pathDst)
                    novoCaminho = os.path.join(pathDst, arq)
                    os.rename(pathArq, novoCaminho)

    def enviarEmail(self, destinatarios, assunto, mensagem):

        usuario, senha = self.obterAcessos("emailMacros")
        print(usuario, senha)

        smtp_server = "smtp.office365.com"
        smtp_port = 587

        msgEmail = f"""
Bom dia!

{mensagem}

Atenciosamente,
Robô do Luciano.
"""


        msg = MIMEMultipart()
        msg['From'] = usuario
        msg['To'] = destinatarios
        msg['Subject'] = assunto
        msg.attach(MIMEText(mensagem, 'plain'))

        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(usuario, senha)
            server.sendmail(usuario, destinatarios, msg.as_string())
            server.quit()
            print("E-mail enviado com sucesso!")
        except Exception as e:
            print(f"Falha ao enviar e-mail: {e}")

    def converterHTML2PDF(self, conteudoHTML, diretorioSaida, nomeArquivo):

        caminhoSaida = Path(diretorioSaida) / f"{nomeArquivo}.pdf"
        HTML(string=conteudoHTML).write_pdf(caminhoSaida)
        print(f"PDF gerado em: {caminhoSaida}")
        return caminhoSaida
    

    def editarPlanilhaAcoes(self):

        for arq in os.listdir(pathOutput):
            pathArq = os.path.join(pathOutput, arq)
            if os.path.isfile(pathArq) and arq.endswith('.xlsx') and \
            data.__format__("%d.%m.%Y") in arq:
                print(f"    ->Editando arquivo: {arq}")
                # Abrir a planilha
                xls = pd.ExcelFile(pathArq)
                abas = xls.sheet_names
                abas_origem = []
                if 'Ações' in abas:
                    abas_origem.append('Ações')
                if 'FII-Fiagro' in abas:
                    abas_origem.append('FII-Fiagro')
                df_list = []
                for aba in abas_origem:
                    df = pd.read_excel(pathArq, sheet_name=aba)
                    colunas_necessarias = ['Ticker', 'Segmento', 'Valor Atual', 'Média de Dividendos (24m)']
                    df = df[[col for col in colunas_necessarias if col in df.columns]]
                    df_list.append(df)
                if df_list:
                    import openpyxl
                    df_menu = pd.concat(df_list, ignore_index=True)
                    df_menu['Quantidade'] = 0
                    # Adiciona as colunas como fórmulas do Excel
                    df_menu['Valor Total'] = None  # Placeholder for formula
                    df_menu['Estimativa Dividendos'] = None  # Placeholder for formula
                    colunas_finais = ['Ticker', 'Segmento', 'Valor Atual', 'Média de Dividendos (24m)', 'Quantidade', 'Valor Total', 'Estimativa Dividendos']
                    df_menu = df_menu[[col for col in colunas_finais if col in df_menu.columns]]
                    with pd.ExcelWriter(pathArq, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                        df_menu.to_excel(writer, sheet_name='Menu-Compras', index=False)
                    # Aplicar fórmulas nas colunas 'Valor Total' e 'Estimativa Dividendos'
                    wb = openpyxl.load_workbook(pathArq)
                    ws = wb['Menu-Compras']
                    for row in range(2, ws.max_row + 1):
                        ws[f'F{row}'] = f'=C{row}*E{row}'  # Valor Total
                        ws[f'G{row}'] = f'=D{row}*E{row}'  # Estimativa Dividendos
                    # Adiciona resumo ao final da tabela
                    resumo_row = ws.max_row + 2
                    
                    ws[f'B{resumo_row}'] = 'Valor total'
                    ws[f'C{resumo_row}'] = f'=SUM(F2:F{ws.max_row-2})'
                    
                    ws[f'B{resumo_row+1}'] = 'Total de dividendos estimado'
                    ws[f'C{resumo_row+1}'] = f'=SUM(G2:G{ws.max_row-2})'
                    wb.save(pathArq)
                    print(f"    ->Aba 'Menu-Compras' criada/atualizada em: {arq}")
                print(f"    ->Arquivo editado: {arq}")