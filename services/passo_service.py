from common.validações_genericas import Validações
from repositories.passo_repository import PassoRepository
from services.tarefa_service import TarefaService
from datetime import datetime

validacoes = Validações()

_validar_id = validacoes._validar_id

tarefaservice = TarefaService()

class PassoService:
 
    def __init__(self, repository=None): 
        self.repository = repository or PassoRepository()

    def listar_por_tarefa(self, tarefa_id):

        tarefa_id = _validar_id(tarefa_id)

        try:
            tarefaservice.buscar_por_id(tarefa_id)
        
        except ValueError as erro:
            raise ValueError(f"Falha no service tarefas, listar_por_id: {erro}")


        passos = self.repository.listar_por_tarefa(tarefa_id)

        if not passos:
            raise ValueError("Tarefa ainda não possui passos")

        novos_passos = []

        for i in passos:
            passo = {
                "id": i.id,
                "tarefa_id": i.tarefa_id,
                "texto": i.texto,
                "concluida": i.concluido,
                "ordem": i.ordem
            }

            novos_passos.append(passo)

        return novos_passos

    def criar_passo(self, tarefa_id, texto):

        tarefa_id = _validar_id(tarefa_id)

        if texto == "":
            raise ValueError("Texto não pode ser vazio")

        tarefa_passos = self.listar_por_tarefa(tarefa_id)


        ordem = tarefa_passos[-1]["ordem"]
        ordem += 1

        self.repository.criar_passo(tarefa_id, texto, ordem)

        return {
            "tarefa_id": tarefa_id,
            "texto": texto,
            "ordem": ordem
        }

    def alternar_concluido(self, id, modo="None"):

        id = _validar_id(id)

        if modo.casefold() not in {"none", "true", "false"}:
            raise ValueError("O modo deve ser True, False ou Vazio.")

        self.repository.alternar_concluido(id, modo)

    def excluir_por_id(self, id):

        id = _validar_id(id)

        resultado = self.repository.excluir_por_id(id)

        if resultado == False:
            raise ValueError("Passo não encontrado")