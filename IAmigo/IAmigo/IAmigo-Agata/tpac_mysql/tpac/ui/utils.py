import os
from language.language_manager import load_language

strings = load_language()
strings = strings["utils.py"]

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def exibir_cabecalho(titulo: str):
    limpar_tela()
    print("=" * 60)
    print(f"{titulo.center(60)}")
    print("=" * 60 + "\n")
    
def exibir_barra_status(usuario):
    print(" ╔══════════════════════════════════════════════════════╗")
    print(f" ║ {strings['exibir_barra_status']['msg1']} {usuario:<15}   {strings['exibir_barra_status']['msg2']}       ║")
    print(" ╚══════════════════════════════════════════════════════╝")