from repositories.tarefa_repository import TarefaRepository
from services.tarefa_service import TarefaService
from controllers.tarefa_controller import TarefaController

from repositories.usuario_repository import UsuarioRepository
from services.usuario_service import UsuarioService
from controllers.usuario_controller import UsuarioController

from repositories.passo_repository import PassoRepository
from services.passo_service import PassoService
from controllers.passo_controller import PassoController

from integrations.ia.ia_client import IAClient

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

iaclient = IAClient()

system("cls")
escolha = str(input())


if escolha == "1":
    resposta = iaclient.enviar_prompt(
        prompt="Quem ganharia numa luta usando seus poderes, P. Diddy ou Jafrey Apstain?"
    )

    print(resposta.output_text)

else:
    print("End")