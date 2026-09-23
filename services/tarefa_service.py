from repositories.tarefa_repository import TarefaRepository
from controllers.usuario_controller import UsuarioController
from datetime import datetime

usuariocontroller = UsuarioController()

class TarefaService:
 
    def __init__(self, repository=None): 
        self.repository = repository or TarefaRepository()

    def listar_por_usuario(self, usuario_id):
        usuario_id = str(usuario_id)

        if usuario_id == None:
            raise ValueError("O id não pode ser vazio.")

        for i in list(usuario_id):
            if i not in {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9"}:
                raise ValueError("O id só pode conter números.")

        usuario = usuariocontroller.buscar_por_id(usuario_id)
        
        if usuario["sucesso"] != True:
            raise ValueError(usuario['mensagem'])

        tarefas = self.repository.listar_por_usuario(usuario_id)

        if tarefas == None:
            raise ValueError("Tarefas não encontradas.")

        if not tarefas:
            raise ValueError("Usuário ainda não possui tarefas")

        novas_tarefas = []

        for i in tarefas:
            prazo = str(i.prazo)
            prazo = f"{prazo[8: 10]}/{prazo[5:7]}/{prazo[0:4]}"

            tarefa = {
                "id": i.id,
                "usuario_id": i.usuario_id,
                "tipo": i.tipo,
                "titulo": i.titulo,
                "descricao": i.descricao,
                "prioridade": i.prioridade,
                "prazo": prazo,
                "concluida": i.concluida
            }

            novas_tarefas.append(tarefa)

        return novas_tarefas

    def buscar_por_id(self, id):
        if id == None:
            raise ValueError("O id não pode ser vazio.")

        for i in list(str(id)):
            if i not in {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9"}:
                raise ValueError("O id só pode conter números.")

        tarefa = self.repository.buscar_por_id(id)

        if tarefa == None:
            raise ValueError("Tarefa não encontrada.")

        resultado = {
            "usuario_id": tarefa.usuario_id,
            "tipo": tarefa.tipo,
            "titulo": tarefa.titulo,
            "descricao": tarefa.descricao,
            "prioridade": tarefa.prioridade,
            "prazo": tarefa.prazo
        }
        return resultado
    
    def alternar_concluido(self, id, modo="None"):
        if id == None:
            raise ValueError("O id não pode ser vazio.")

        for i in list(str(id)):
            if i not in {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9"}:
                raise ValueError("O id só pode conter números.")

        if modo.casefold() not in {"none", "true", "false"}:
            raise ValueError("O modo deve ser True, False ou Vazio.")

        self.repository.alternar_concluido(id, modo)
    
    def criar_tarefa(self, usuario_id, tipo, titulo, descricao, prioridade, prazo=None): 

        # Regras de ID
        if not usuario_id: 
            raise ValueError("O nome não pode ficar vazio.")

        if type(usuario_id) != str:
            usuario_id = str(usuario_id)

        for i in list(usuario_id):
            if i not in {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9"}:
                raise ValueError("O id só pode conter números.")

        # Regras de Tipo
        if not tipo:
            raise ValueError("Tipo não pode ficar vazio")

        if tipo not in {"tarefas_diarias", "tarefas_educacionais"}:
            raise ValueError("Tipo deve ser tarefas_diarias ou tarefas_educacionais")

        # Regras de Titulo
        if not titulo:
            raise ValueError("O titulo não pode ficar vazio")

        if len(list(titulo)) > 200:
            raise ValueError("O titulo deve possuir no máximo 200 caracteres")
 
        # Regras de descrição
        # Não necessária

        # Regras de prioridade
        if not prioridade:
            raise ValueError("Prioridade não pode ficar vazia")

        if prioridade not in {'baixa', 'media', 'alta'}:
            raise ValueError("A prioridade deve ser baixa, média ou alta")

        # Regras de prazo
        if prazo:
            try:
                prazo = datetime.strptime(prazo, "%d/%m/%Y").date()
            except ValueError:
                raise ValueError("O formato da data é inválido. A data deve estar no formato Dia/Mês/Ano")

        else:
            prazo = None

        return self.repository.criar_tarefa(
            usuario_id=usuario_id,
            tipo=tipo,
            titulo=titulo,
            descricao=descricao,
            prioridade=prioridade,
            prazo=prazo
        )

    def excluir_por_id(self, id):
        if id == None:
            raise ValueError("O id não pode ser vazio.")

        for i in list(str(id)):
            if i not in {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9"}:
                raise ValueError("O id só pode conter números.")

        excluida = self.repository.excluir_por_id(id)

        if not excluida:
            raise ValueError("Tarefa não encontrada.")

        return True