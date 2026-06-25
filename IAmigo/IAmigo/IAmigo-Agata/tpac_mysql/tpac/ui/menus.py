from language.language_manager import load_language, menu_frame
from ui.utils import exibir_cabecalho, exibir_barra_status
from data.data_manager import carregar_dados, salvar_dados
from configparser import ConfigParser
import core.ia_service as ia_service
import core.tarefas as core_tarefas
from pathlib import Path

strings = load_language()
strings = strings["menus.py"]

def criar_usuario_menu(dados: dict):
    exibir_cabecalho(strings["criar_usuario_menu"]["titulo"])
    nome = input(f"{strings["criar_usuario_menu"]["Q1"]} ").strip()
    if not nome:
        input(f"\n{strings['criar_usuario_menu']['if_error1']} ")
        return

    if nome in dados:
        input(f"\n{strings["criar_usuario_menu"]["if_error2"]} '{nome}'. {strings["criar_usuario_menu"]["if_error2.1"]} ")
        return

    print(f"\n{strings['criar_usuario_menu']['Q2']} ")
    print(strings['criar_usuario_menu']['Q2.1'])
    print(strings['\ncriar_usuario_menu']['opção1'])
    print(strings['criar_usuario_menu']['opção2'])
    pref = input(f"{strings['criar_usuario_menu']['msg']} ").strip()
    estilo = "direto" if pref == "1" else "detalhado"

    dados[nome] = {
        "preferencias": {"estilo_instrucao": estilo},
        "tarefas_diarias": [],
        "tarefas_educacionais": []
    }
    salvar_dados(dados)
    input(f"\n{strings['criar_usuario_menu']['msg1']}, [{nome}]! {strings['criar_usuario_menu']['msg1.1']}")

def gerenciar_tarefas_menu(dados: dict, usuario: str, chave: str, titulo: str):
    while True:
        exibir_cabecalho(titulo)
        tarefas = dados[usuario][chave]
        
        if not tarefas:
            print(strings["gerenciar_tarefas_menu"]["ifnot_tarefas"])
        else:
            for idx, t in enumerate(tarefas, 1):
                status = "[X]" if t["concluida"] else "[ ]"
                print(f"{idx}. {status} {t['titulo']}")
                for p in t.get("passos", []):
                    print(f"   ○ {p['texto']}")

        print("\n" + "-"*30)
        print(strings["gerenciar_tarefas_menu"]["opções"])
        opcao = input(f"\n{strings['gerenciar_tarefas_menu']['msg1']} ").strip()

        if opcao == "1":
            t_nome = input(f"{strings["gerenciar_tarefas_menu"]["opção1_child"]} ").strip()
            if t_nome: core_ref = core_tarefas.adicionar_tarefa(dados, usuario, chave, t_nome)
        elif opcao == "2" and tarefas:
            try:
                idx = int(input(f"{strings["gerenciar_tarefas_menu"]["opção2_child"]} ")) - 1
                core_tarefas.alternar_status_tarefa(dados, usuario, chave, idx)
            except ValueError: pass
        elif opcao == "3" and tarefas:
            try:
                idx = int(input(f"{strings["gerenciar_tarefas_menu"]["opção3_children"]["msg1"]} ")) - 1
                if 0 <= idx < len(tarefas):
                    passos = ia_service.gerar_passos_tarefa(tarefas[idx]["titulo"])
                    print(f"\n{strings['gerenciar_tarefas_menu']['opção3_children']['msg2']} ")
                    for i, p in enumerate(passos, 1): print(f"  {i}. {p}")
                    if input(f"\n{strings['gerenciar_tarefas_menu']['opção3_children']['msg3']} ").lower() == 's':
                        core_tarefas.injetar_passos_ia(dados, usuario, chave, idx, passos)
            except ValueError: pass
        elif opcao == "4":
            break

def painel_ia_menu(dados: dict, usuario: str):
    exibir_cabecalho(strings["painel_ia_menu"]["titulo"])
    print(strings["painel_ia_menu"]["msg1"])
    print(strings["painel_ia_menu"]["msg2"])
    estilo = dados[usuario]["preferencias"]["estilo_instrucao"]

    while True:
        pergunta = input(f"\n{strings['painel_ia_menu']['msg3']}: ").strip()
        if pergunta.lower() == 'exit': break
        if not pergunta: continue

        print(f"\n{strings['painel_ia_menu']['msg4']}")
        respostas = ia_service.obter_resposta_ia(pergunta, estilo)
        print(f"\n[{strings['painel_ia_menu']['msg5']} {estilo.upper()}]: ")
        for linha in respostas:
            print(f"- {linha}")
        print("-" * 30)

def painel_principal_menu(dados: dict, usuario: str):

    while True:
        exibir_cabecalho(strings["painel_principal_menu"]["titulo"])
        exibir_barra_status(usuario)

        menu_frame(list(strings["painel_principal_menu"]["opções"].values()), strings["painel_principal_menu"]["titulo1"])

        opcao = input(f"\n{strings['painel_principal_menu']['msg']} ").strip()
        if opcao == "1":
            print(f"\n{strings['painel_principal_menu']['opção1_children']['msg1']}")
            input(f"\n{strings['painel_principal_menu']['opção1_children']['msg2']}")
            gerenciar_tarefas_menu(dados, usuario, "tarefas_diarias", str(strings["painel_principal_menu"]["opção1_children"]["titulo"]))
        elif opcao == "2":
            print(f"\n{strings['painel_principal_menu']['opção2_children']['msg1']}")
            input(f"\n{strings['painel_principal_menu']['opção2_children']['msg2']}")
            gerenciar_tarefas_menu(dados, usuario, "tarefas_educacionais", str(strings["painel_principal_menu"]["opção2_children"]["titulo"]))
        elif opcao == "3":
            print(f"\n{strings['painel_principal_menu']['opção3_children']['msg1']}")
            input(f"\n{strings['painel_principal_menu']['opção3_children']['msg2']}")
            painel_ia_menu(dados, usuario)
        elif opcao == "4":
            print(f"\n{strings['painel_principal_menu']['opção4_children']['msg1']}")
            print(f"{strings['painel_principal_menu']['opção4_children']['msg2']}")
            break

def language_menu():
    #Obtendo o diretorio das configurações e pasta de linguas   
    config_path = Path(__file__).parent.parent / "data" / "config.ini"
    languages_path = Path(__file__).parent.parent / "language" / "language_xml"

    config = ConfigParser()
    config.read(config_path, encoding="utf-8")

    languages_list = [f.stem for f in languages_path.iterdir() if f.is_file() and f.suffix == '.xml']
    
    exibir_cabecalho(strings["language_menu"]["titulo"])
    menu_frame(languages_list, (strings["language_menu"]["msg1"]))
    select = int(input(f"{strings['language_menu']['msg2']} "))

    select = languages_list[(int(select) - 1)]
    select = select + ".xml"

    config.set("localization", "language", select)

    with open('meu_arquivo.ini', 'w') as configfile:
        config.write(configfile)
    
    print(strings["language_menu"]["msg3"])
