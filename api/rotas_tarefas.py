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

@router.get("")
def listar_por_usuario(id_usuario):
    resultado = controller.listar_por_usuario(id_usuario)

    return resultado

@router.post("/{id}", status_code=status.HTTP_201_CREATED)
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