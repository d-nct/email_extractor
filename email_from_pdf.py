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
# Rodamos o programa passando o arquivo a ser vasculhado como argumento.
# Exemplo: python3 email_from_pdf.py path/to/file.pdf

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
def main(paths: list, pattern=EMAIL_PATTERN) -> None:
    print(flag)

    for path in paths:
        try:
            obj = ex.ExtractorFromPDF(path, pattern)
        except FileNotFoundError:
            print(f"Arquivo não existe: {path}!!")
            continue

        print(f"TRABALHANDO EM > {path} <", end='\n\n')
        try:
            obj.extract()
        except:
            print(f"Erro em {path}!!")
        finally:
            print(f"\n{'=+'*20}=\n")


if __name__ == '__main__':
    if sys.argv != ['']:
        _, *PATHS = sys.argv  # recebendo externamente
    else:
        PATHS = [
            "file.pdf"
                 ]

    main(PATHS)