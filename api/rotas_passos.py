from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from controllers.passo_controller import PassosController

router = APIRouter(
    prefix="/passos",
    tags=["passos"]
)

controller = PassosController()

class NovoPasso(BaseModel):
    tarefa_id: int
    texto: str 
    concluido: bool | None = False
    ordem: int | None = 1

