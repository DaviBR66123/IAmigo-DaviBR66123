from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from controllers.tarefa_controller import TarefaController

router = APIRouter(
    prefix="/usuarios",
    tags=["usuarios"]
)

controller = TarefaController()

class NovaTarefa(BaseModel):
    usuario_id: str
    tipo: str
    titulo: str 
    descricao: str | None = None
    prioridade: str = "media"
    prazo: str | None = None

@router.post("", status_code=status.HTTP_201_CREATED)
def criar_tarefa(id, dados: NovaTarefa)
    resposta = controller.criar_tarefa(
        id,
        dados.tipo,
        dados.titulo
    )