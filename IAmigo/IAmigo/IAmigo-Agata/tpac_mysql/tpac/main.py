import random
from data.data_manager import carregar_dados
from ui.menus import criar_usuario_menu, painel_principal_menu, language_menu
from ui.utils import exibir_cabecalho
from language.language_manager import load_language, menu_frame

strings = load_language()
strings = strings["main.py"]

def exibir_logo():
    print("""
    ╔══════════════════════════════════════════════════╗
    ║                                                  ║
    ║   ██╗ █████╗ ███╗   ███╗██╗ ██████╗  ██████╗     ║
    ║   ██║██╔══██╗████╗ ████║██║██╔════╝ ██╔═══██╗    ║
    ║   ██║███████║██╔████╔██║██║██║  ███╗██║   ██║    ║
    ║   ██║██╔══██║██║╚██╔╝██║██║██║   ██║██║   ██║    ║
    ║   ██║██║  ██║██║ ╚═╝ ██║██║╚██████╔╝╚██████╔╝    ║
    ║   ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝ ╚═════╝  ╚═════╝     ║
    ║                                                  ║
    ║   Seu amigo para organizar tarefas e estudos     ║
    ║                                                  ║
    ║       Desenvolvido para auxiliar pessoas         ║
    ║            com dificuldades de foco              ║
    ║                                                  ║
    ╚══════════════════════════════════════════════════╝
    """)


def exibir_frase():
    frases = list(strings["frases"].values())

    print(f"\n{random.choice(frases)}\n")


def executar_sistema():
    while True:
        dados = carregar_dados()

        exibir_logo()
        print(strings["saudação"])
        exibir_frase()

        menu_frame(list(strings["menu2_entrada"]["opções"].values()), strings["menu2_entrada"]["titulo"])
        
        opcao = input(f"\n{strings['menu2_entrada']['msg']} ").strip()
        
        if opcao == "1":
            if not dados:
                input(f"\n{strings['menu2_entrada']['opção1_children']['if_error1']}")
                continue

            menu_frame(dados, strings["menu2_entrada"]["opção1_children"]["titulo"])
            nome = input(f"\n{strings['menu2_entrada']['opção1_children']['msg']} ").strip()
                
            if nome in dados:
                painel_principal_menu(dados, nome)
            else:
                input(f"\n{strings['menu2_entrada']['opção1_children']["if_error2"]}")
        
        elif opcao == "2":
            criar_usuario_menu(dados)

        elif opcao == "3":
            language_menu()
            
        elif opcao == "4":
            print(f"\n{strings['menu2_entrada']['opção3_children']["msg"]}")
            break  # Agora o break está alinhado corretamente dentro da opção 4


if __name__ == "__main__":
    executar_sistema()