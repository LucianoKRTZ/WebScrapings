import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd
from weasyprint import HTML
from pathlib import Path
from datetime import datetime
import os

pathAcessos = "C:\\__Programas__\\__config__\\acessos.xlsx"
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
        pathOutput = "C:\\Macros\\Acoes"
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