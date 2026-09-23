from repositories.passo_repository import PassoRepository
from controllers.tarefa_controller import TarefaController
from datetime import datetime

tarefacontroller = TarefaController()

class PassoService:
 
    def __init__(self, repository=None): 
        self.repository = repository or PassoRepository()

    def listar_por_tarefa(self, tarefa_id):
        tarefa_id = str(tarefa_id)

        if tarefa_id == None:
            raise ValueError("O id não pode ser vazio.")

        for i in list(tarefa_id):
            if i not in {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9"}:
                raise ValueError("O id só pode conter números.")

        tarefa = tarefacontroller.buscar_por_id(tarefa_id)
        
        if tarefa["sucesso"] != True:
            raise ValueError(tarefa['mensagem'])

        passos = self.repository.listar_por_tarefa(tarefa_id)

        if passos == None:
            raise ValueError("Passos não encontrados.")

        if not passos:
            raise ValueError("Tarefa ainda não possui passos")

        novos_passos = []

        for i in passos.values:
            passo = {
                "id": i.id,
                "tarefa_id": i.tarefa_id,
                "texto": i.texto,
                "concluida": i.concluida,
                "ordem": i.ordem
            }

            novos_passos.append(passo)

        return novos_passos

    def criar_passo(self, tarefa_id, texto, ordem):
        tarefa_id = str(tarefa_id)

        if tarefa_id == None:
            raise ValueError("O id não pode ser vazio.")

        for i in list(tarefa_id):
            if i not in {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9"}:
                raise ValueError("O id só pode conter números.")

        if texto == "":
            raise ValueError("Texto não pode ser vazio")

        if ordem <= 0:
            raise ValueError("A ordem precisa fazer sentido. 0 até da de engolir, mas -1 não")

        passo = self.repository.criar_passo(tarefa_id, texto, ordem)

        return {
            "tarefa_id": tarefa_id,
            "texto": texto,
            "ordem": ordem
        }

    def alternar_concluido(self, id, modo="None"):
        if id == None:
            raise ValueError("O id não pode ser vazio.")

        for i in list(str(id)):
            if i not in {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9"}:
                raise ValueError("O id só pode conter números.")

        if modo.casefold() not in {"none", "true", "false"}:
            raise ValueError("O modo deve ser True, False ou Vazio.")

        self.repository.alternar_concluido(id, modo)