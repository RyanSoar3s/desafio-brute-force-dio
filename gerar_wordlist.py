#!/usr/bin/env python3
"""
gerar_wordlists.py

Script para gerar wordlists simples de usuarios e senhas, para uso em
testes de forca bruta/password spraying em AMBIENTE CONTROLADO E ISOLADO
(Kali Linux + Metasploitable 2 + DVWA, rede host-only).

Uso educacional. Nao utilizar contra sistemas sem autorizacao explicita.

Uso:
    python3 gerar_wordlists.py
    python3 gerar_wordlists.py --saida ./wordlists --extra-usuarios joao,maria
    python3 gerar_wordlists.py --sem-variacoes

Saida (por padrao, na pasta "wordlists/"):
    usuarios.txt
    senhas.txt
"""

import argparse
import os


# ---------------------------------------------------------------------------
# Bases de dados simples: usuarios e senhas comuns relevantes para o
# cenario do desafio (Metasploitable 2, DVWA, SMB).
# ---------------------------------------------------------------------------

USUARIOS_METASPLOITABLE = [
    "msfadmin",
    "user",
    "postgres",
    "service",
    "sys",
    "klog",
    "root",
    "admin",
    "guest",
]

USUARIOS_SMB_COMUNS = [
    "administrator",
    "admin",
    "guest",
    "backup",
    "operator",
    "ftp",
]

USUARIOS_DVWA = [
    "admin",
    "gordonb",
    "1337",
    "pablo",
    "smithy",
]

SENHAS_FRACAS_COMUNS = [
    "123456",
    "password",
    "12345678",
    "qwerty",
    "abc123",
    "letmein",
    "admin",
    "welcome",
    "senha",
    "senha123",
    "changeme",
]

SENHAS_PADRAO_METASPLOITABLE = [
    "msfadmin",
    "user",
    "postgres",
    "service",
    "batman",
    "toor",
    "123456789",
]

SENHAS_PADRAO_DVWA = [
    "password",
    "abc123",
    "charley",
    "letmein",
    "password1",
    "qwerty",
]


def gerar_variacoes(base_list):
    """
    Gera variacoes simples (maiuscula inicial, ano no final, leet speak
    basico) a partir de uma lista base. Mantem a wordlist pequena e
    realista para fins didaticos, sem explodir em milhares de linhas.
    """
    variacoes = set()
    anos = ["2023", "2024", "2025"]
    leet_map = str.maketrans({"a": "@", "o": "0", "e": "3", "i": "1", "s": "$"})

    for palavra in base_list:
        variacoes.add(palavra)
        variacoes.add(palavra.capitalize())
        variacoes.add(palavra.translate(leet_map))
        for ano in anos:
            variacoes.add(f"{palavra}{ano}")
            variacoes.add(f"{palavra.capitalize()}{ano}")
        variacoes.add(f"{palavra}!")
        variacoes.add(f"{palavra}123")

    return sorted(variacoes)


def montar_lista_usuarios(extra_usuarios=None):
    usuarios = set()
    usuarios.update(USUARIOS_METASPLOITABLE)
    usuarios.update(USUARIOS_SMB_COMUNS)
    usuarios.update(USUARIOS_DVWA)

    if extra_usuarios:
        usuarios.update(u.strip() for u in extra_usuarios if u.strip())

    return sorted(usuarios)


def montar_lista_senhas(com_variacoes=True, extra_senhas=None):
    senhas_base = set()
    senhas_base.update(SENHAS_FRACAS_COMUNS)
    senhas_base.update(SENHAS_PADRAO_METASPLOITABLE)
    senhas_base.update(SENHAS_PADRAO_DVWA)

    if extra_senhas:
        senhas_base.update(s.strip() for s in extra_senhas if s.strip())

    if com_variacoes:
        senhas_final = set(senhas_base)
        senhas_final.update(gerar_variacoes(senhas_base))
        return sorted(senhas_final)

    return sorted(senhas_base)


def escrever_arquivo(caminho, linhas):
    with open(caminho, "w", encoding="utf-8") as f:
        for linha in linhas:
            f.write(linha + "\n")
    print(f"[OK] {caminho} gerado com {len(linhas)} linhas.")


def main():
    parser = argparse.ArgumentParser(
        description="Gera wordlists simples de usuarios e senhas para o "
        "desafio de forca bruta (DIO - Kali + Medusa/Hydra)."
    )
    parser.add_argument(
        "--saida",
        default="wordlists",
        help="Pasta de saida para os arquivos gerados (padrao: ./wordlists)",
    )
    parser.add_argument(
        "--extra-usuarios",
        default="",
        help="Usuarios adicionais separados por virgula, ex: joao,maria",
    )
    parser.add_argument(
        "--extra-senhas",
        default="",
        help="Senhas adicionais separadas por virgula, ex: minhaSenha,Teste#1",
    )
    parser.add_argument(
        "--sem-variacoes",
        action="store_true",
        help="Nao gerar variacoes (ano, leet speak, maiuscula) das senhas",
    )

    args = parser.parse_args()

    os.makedirs(args.saida, exist_ok=True)

    extra_usuarios = args.extra_usuarios.split(",") if args.extra_usuarios else []
    extra_senhas = args.extra_senhas.split(",") if args.extra_senhas else []

    usuarios = montar_lista_usuarios(extra_usuarios)
    senhas = montar_lista_senhas(
        com_variacoes=not args.sem_variacoes, extra_senhas=extra_senhas
    )

    escrever_arquivo(os.path.join(args.saida, "usuarios.txt"), usuarios)
    escrever_arquivo(os.path.join(args.saida, "senhas.txt"), senhas)

    print(
        "\nLembre-se: use essas listas apenas em ambiente controlado e "
        "isolado (host-only), nunca contra sistemas reais sem autorizacao."
    )


if __name__ == "__main__":
    main()
