#!/usr/bin/env python3

import os
import sys
import re

import PyPDF2 as p2
from urllib.request import urlopen

EMAIL_PATTERN = r"([\w\.-]+)@([\w\.-]+)(\.[\w\.]+)"

class Extractor():
    def __init__(self, alvo, pattern):
        """
        Inicia o objeto com a variável de emails iniciamente vazia.
        """
        self.pattern = pattern
        self.alvo = alvo
        self.emails_obtidos = []

    def to_strings(self):
        """Converte uma tupla contendo nome, domínio e sulfixo de um email em uma
        string bonita.
        """
        l_convertida = []
        for email in self.emails_obtidos:
            nome, domínio, sulfixo = email
            l_convertida.append(f"{nome}@{domínio + sulfixo}")
        return l_convertida

    def _remove_duplicadas(self) -> list:
        """Remove itens duplicados, caso hajam."""
        sem_duplicatas = []
        for item in self.emails_obtidos:
            if not item in sem_duplicatas:
                sem_duplicatas.append(item)

        self.emails_obtidos = sem_duplicatas
        return sem_duplicatas

    def filtre(self) -> list:
        """Filtra a lista o máximo que possível."""
        l = self._remove_duplicadas()
        # Mais filtros em breve...
        return l

    def imprime_emails(self) -> None:
        """Imprime na tela do usuário os emails dados em lista de tuplas."""
        emails = self.to_strings()
        for possivel_email in emails:
            print(f"[*] Email encontrado: {possivel_email}")

class ExtractorFromWeb(Extractor):

    def extract(self) -> list:
        """
        Recebe um url em forma de string (incluso http/https://:) e retorna uma lista com os
        emails encontrados na forma:
        [
        (nome1, domínio1, sulfixo1),
        (nome2, domínio2, sulfixo2),
        (nome3, domínio3, sulfixo3),
        ...
        ]
        """
        with urlopen(self.alvo) as f:
            pagina = f.read().decode('utf-8')  # A página usa caracteres utf-8

        self.emails_obtidos += re.findall(self.pattern, pagina)
        print(f"[+] Extraindo  {self.alvo}", end='\n\n')

        num_pre_filtro = len(self.emails_obtidos)
        emails_filtrada = self.filtre()
        num_pos_filtro = len(self.emails_obtidos)
        self.imprime_emails()

        print(f"\n[+] Encontrados {num_pre_filtro} potenciais emails.")
        print(f"[+] Removidos {num_pre_filtro - num_pos_filtro} emails duplicados.")

        self.emails_obtidos = emails_filtrada
        return self.emails_obtidos

class ExtractorFromPDF(Extractor):
    def __init__(self, alvo, pattern):
        super().__init__(alvo, pattern)

        self._file = open(alvo, "rb")
        self.reader = p2.PdfFileReader(self._file)

    def pdf_to_string(self) -> str:
        """
        Tranforma o objeto reader em uma string.
        """

        txt = ''
        num_de_pgs = self.reader.getNumPages()
        for i in range(num_de_pgs):
            pg_atual = self.reader.getPage(i)
            txt += pg_atual.extractText()
        return txt

    def extract(self) -> list:
        """
        Recebe um arquivo .pdf para buscar por emais e retorna uma lista com os emails
        encontrados na forma:
        [
        (nome1, domínio1, sulfixo1),
        (nome2, domínio2, sulfixo2),
        (nome3, domínio3, sulfixo3),
        ...
        ]

        Obs.: Falha notada: Não encontra emails em hyperlinks!
        """
        file = open(self.alvo, "rb")

        # Texto legível
        conteudo = self.pdf_to_string()
        self.emails_obtidos += re.findall(self.pattern, conteudo)
        print(f"[+] Escavando o texto de {self.alvo}")

        # Infos do arquivo
        infos = self.reader.getDocumentInfo()
        print(f"[+] Escavando as propriedades de {self.alvo}")
        if infos:
            for item in infos.values():
                x = re.findall(self.pattern, item)
                if x:
                    self.emails_obtidos += x

        # Metadados
        metadata = self.reader.getXmpMetadata()
        print(f"[+] Escavando os metadados de {self.alvo}", end='\n\n')
        if metadata:
            pass

        num_pre_filtro = len( self.emails_obtidos )
        emails_filtrada = self.filtre()
        num_pos_filtro = len(self.emails_obtidos)
        self.imprime_emails()

        print(f"\n[+] Encontrados {num_pre_filtro} potenciais emails.")
        print(f"[+] Removidos {num_pre_filtro - num_pos_filtro} emails duplicados.")

        file.close()
        self.emails_obtidos = emails_filtrada
        return self.emails_obtidos