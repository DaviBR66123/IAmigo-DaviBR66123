from controllers.usuario_controller import UsuarioController
import os

controller = UsuarioController()
os.system("cls" if os.name == "nt" else "clear")

while True: 
    print("\n=== EXEMPLO AULA 02 ===") 
    print("1. Listar perfis")
    print("2. Buscar usuario por id") 
    print("3. Criar perfil") 
    print("4. Sair")

    opcao = input("Escolha: ").strip() 

    if opcao == "1": 
        perfis = controller.listar_perfis() 

        print("\nPerfis:") 
        for nome in perfis: 
            print("-", nome) 

    elif opcao == "2":
        usuario = input("buscar Usuario de id: ")
        controller = UsuarioController()
        usuario = controller.buscar_por_id(usuario)

        print(usuario['mensagem'])

        if usuario['sucesso'] == True:
            print(f"Nome: {usuario['dados']['nome']}")
            print(f"Id: {usuario['dados']['id']}")
            print(f"Estilo: {usuario['dados']['estilo_instrucao']}")
            print(f"Criado em: {usuario['dados']['criado_em']}")

    elif opcao == "3": 
        nome = input("Nome: ").strip() 

        print("1. Direto") 
        print("2. Detalhado") 
        escolha = input("Estilo: ").strip() 

        estilo = ( 
        "detalhado" 
        if escolha == "2" 
        else "direto" )

        resposta = controller.criar_perfil( 
        nome, 
        estilo
        )

        print(resposta["mensagem"])

    elif opcao == "4": 
        break

    else: 
        print("Opção inválida.")