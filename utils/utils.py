import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd
from weasyprint import HTML
from pathlib import Path


class Utils:
    def obterAcessos(self, plataforma):
        excel = pd.read_excel('/home/luciano/Documentos/acessos.xlsx', sheet_name='acessos')
        for linha in excel.itertuples():
            if linha[1] == plataforma:
                usuario = linha[2]
                senha = linha[3]

        return usuario, senha
    
    def obterDestinatarioEmail(self, programa):
        excel = pd.read_excel('/home/luciano/Documentos/acessos.xlsx', sheet_name='destinatarios')
        destinatarios = []
        for linha in excel.itertuples():
            if linha[1] == programa:
                destinatarios.append(linha[3])
        return destinatarios



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