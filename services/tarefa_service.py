from repositories.tarefa_repository import TarefaRepository
from datetime import datetime

class TarefaService:
 
    def __init__(self, repository=None): 
        self.repository = repository or TarefaRepository()

    def listar_por_usuario(self, usuario):
        print("a")

    def buscar_por_id(self, id):
        id = str(id)

        if id == None:
            raise ValueError("O id não pode ser vazio.")

        for i in list(id):
            if i not in {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9"}:
                raise ValueError("O id só pode conter números.")

        tarefa = self.repository.buscar_por_id(id)

        if tarefa == None:
            raise ValueError("Tarefa não encontrada.")

        prazo = tuple(str(tarefa.prazo))
        prazo = f"{prazo[8, 9]}/{prazo[5, 6]}/{prazo[0, 3]}"

        tarefa = {
            "id": tarefa.id,
            "usuario_id": tarefa.usuario_id,
            "tipo": tarefa.tipo,
            "titulo": tarefa.titulo,
            "descricao": tarefa.descricao,
            "prioridade": tarefa.prioridade,
            "prazo": str(tarefa.prazo),
            "concluida": tarefa.concluida
        }

        return tarefa
    
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
        print("a")