from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from controllers.tarefa_controller import TarefaController

router = APIRouter(
    prefix="/tarefas",
    tags=["tarefas"]
)

controller = TarefaController()

class NovaTarefa(BaseModel):
    usuario_id: str
    tipo: str # 'tarefas_diarias' ou 'tarefas_educacionais'
    titulo: str 
    descricao: str | None = None
    prioridade: str = "media" # 'baixa', 'media' ou 'alta'
    prazo: str | None = None

@router.get("/usuario/{id_usuario}")
def listar_por_usuario(id_usuario):
    resultado = controller.listar_por_usuario(id_usuario)

    return resultado

@router.get("/{id}")
def buscar_por_id(id):
    resultado = controller.buscar_por_id(id)

    return resultado

@router.patch("/{id}/concluido")
def alternar_concluido(id, modo="None"):
    resultado = controller.alternar_concluido(id, modo)

    return resultado

@router.post("", status_code=status.HTTP_201_CREATED)
def criar_tarefa(dados: NovaTarefa):
    resposta = controller.criar_tarefa(
        dados.usuario_id,
        dados.tipo,
        dados.titulo,
        dados.descricao,
        dados.prioridade,
        dados.prazo
    )

    if not resposta["sucesso"]:
        raise HTTPException(
            status_code=422,
            detail=resposta["mensagem"]
        )

    return resposta

@router.delete("")
def excluir_por_id(id):
    resultado = controller.excluir_por_id(id)

    return resultado