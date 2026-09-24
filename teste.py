from repositories.tarefa_repository import TarefaRepository
from services.tarefa_service import TarefaService
from controllers.tarefa_controller import TarefaController

from repositories.usuario_repository import UsuarioRepository
from services.usuario_service import UsuarioService
from controllers.usuario_controller import UsuarioController

from repositories.passo_repository import PassoRepository
from services.passo_service import PassoService
from controllers.passo_controller import PassoController

from os import system

Trepository = TarefaRepository()
Tservice = TarefaService()
Tcontroller = TarefaController()

Urepository = UsuarioRepository()
Uservice = UsuarioService()
Ucontroller = UsuarioController()

Prepository = PassoRepository()
Pservice = PassoService()
Pcontroller = PassoController()

system("cls")
escolha = str(input())


if escolha == "1":
    resultado = Pservice.criar_passo(
        10,
        "O homem é o lobo do homem"
    )

    print(resultado)

elif escolha == "2":
    resultado = Pservice.listar_por_tarefa(10)
    '''
    for tarefa in resultado:
        print("---- Passo ----")

        for chave, valor in tarefa.items():
            print(f"{chave}: {valor}")
    '''
    print(resultado)
    
elif escolha == "3":
    resultado = Pservice.alternar_concluido(7)

    print(resultado)

else:
    print("End")