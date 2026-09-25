from common.validações_genericas import Validações
from repositories.tarefa_repository import TarefaRepository
from services.usuario_service import UsuarioService
from datetime import datetime

usuarioservice = UsuarioService()
validacoes = Validações()

_validar_id = validacoes._validar_id

class TarefaService:
 
    def __init__(self, repository=None): 
        self.repository = repository or TarefaRepository()

    def listar_por_usuario(self, usuario_id):

        usuario_id = _validar_id(usuario_id)
        

        try:
            usuarioservice.buscar_por_id(usuario_id)
        
        except ValueError as erro:
            raise ValueError(f"Falha no service usuario, buscar_por_id: {erro}")

        tarefas = self.repository.listar_por_usuario(usuario_id)

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

        id = _validar_id(id)


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

        id = _validar_id(id)


        if modo.casefold() not in {"none", "true", "false"}:
            raise ValueError("O modo deve ser True, False ou Vazio.")

        self.repository.alternar_concluido(id, modo)
    
    def criar_tarefa(self, usuario_id, tipo, titulo, descricao, prioridade, prazo=None): 

        # Regras de ID
        usuario_id = _validar_id(usuario_id)

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

        id = _validar_id(id)


        excluida = self.repository.excluir_por_id(id)

        if not excluida:
            raise ValueError("Tarefa não encontrada.")

        return True