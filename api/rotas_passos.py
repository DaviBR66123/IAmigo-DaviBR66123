from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from controllers.passo_controller import PassoController

router = APIRouter(
    prefix="/passos",
    tags=["passos"]
)

controller = PassoController()

class NovoPasso(BaseModel):
    tarefa_id: int
    texto: str

@router.get("/tarefa/{id}")
def listar_por_tarefa(tarefa_id):
    resultado = controller.listar_por_tarefa(tarefa_id)

    return resultado

@router.patch("/{id}/concluido")
def alternar_concluido(id, modo="None"):
    resultado = controller.alternar_concluido(id, modo)

    return resultado

@router.post("", status_code=status.HTTP_201_CREATED)
def criar_passo(dados:NovoPasso):
    resultado = controller.criar_passo(dados.tarefa_id, dados.texto)

    return resultado

@router.delete("")
def excluir_por_id(id):
    resultado = controller.excluir_por_id(id)

    return resultado