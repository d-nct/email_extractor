#!/usr/bin/env python3
flag = """
          ______                                __                  __
         / ____/_____________ __   ______ _____/ /___  _____   ____/ /__
        / __/ / ___/ ___/ __ `/ | / / __ `/ __  / __ \/ ___/  / __  / _ \\
       / /___(__  ) /__/ /_/ /| |/ / /_/ / /_/ / /_/ / /     / /_/ /  __/
      /_____/____/\___/\__,_/ |___/\__,_/\__,_/\____/_/      \__,_/\___/

                           ______                _ __
                          / ____/___ ___  ____ _(_) /____
                         / __/ / __ `__ \/ __ `/ / / ___/
                        / /___/ / / / / / /_/ / / (__  )
                       /_____/_/ /_/ /_/\__,_/_/_/____/

"""
# Rodamos o programa passando o url a ser vasculhado como argumento.
# Exemplo: python3 email_from_web.py http://www.his.puc-rio.br/corpo-docente/

# Sessão de Importações
# ---------------------
import sys
import os
import extractor as ex

# Constantes
# ----------
EMAIL_PATTERN = r"([\w\.-]+)@([\w\.-]+)(\.[\w\.]+)"

# MAIN
# ----
def main(urls: list, pattern=EMAIL_PATTERN) -> None:
    print(flag)

    for url in urls:
        try:
            obj = ex.ExtractorFromWeb(url, pattern)
        except FileNotFoundError:
            print(f"Arquivo não existe: {url}!!")
            continue

        print(f"TRABALHANDO EM > {url} <", end='\n\n')
        try:
            obj.extract()
        except:
            print(f"Erro em {url}!!")
        finally:
            print(f"\n{'=+'*20}=\n")


if __name__ == '__main__':
    EMAIL_PATTERN = r"([\w\.-]+)@([\w\.-]+)(\.[\w\.]+)"

    if sys.argv != ['']:
        _, *URLS = sys.argv  # recebendo externamente
    else:
        URLS = [
            "https://github.com/",
            "https://www.youtube.com"
                 ]

    main(URLS)