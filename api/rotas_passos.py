from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

from controllers.passo_controller import PassoController
from common.auth import verificar_token, verificar_admin, meu_recurso, teste_usuario_authenticado

router = APIRouter(
    prefix="/passos",
    tags=["passos"]
)

controller = PassoController()
security = HTTPBearer()

@router.get("/tarefa/{id}")
def listar_por_tarefa(id, credenciais: HTTPAuthCredentials = Depends(security)):
    payload = verificar_token(credenciais.credentials)

    meu_recurso(id, payload)

    resultado = controller.listar_por_tarefa(id)

    return resultado

@router.patch("/{id}/concluido")
def alternar_concluido(id, modo="None", credenciais: HTTPAuthCredentials = Depends(security)):
    payload = verificar_token(credenciais.credentials)

    meu_recurso(id, payload)

    resultado = controller.alternar_concluido(id, modo)

    return resultado

@router.post("", status_code=status.HTTP_201_CREATED)
def criar_passo(tarefa_id, credenciais: HTTPAuthCredentials = Depends(security)):
    payload = verificar_token(credenciais.credentials)

    meu_recurso(tarefa_id, payload)

    resultado = controller.criar_passo(tarefa_id)

    return resultado

@router.delete("")
def excluir_por_id(id, credenciais: HTTPAuthCredentials = Depends(security)):
    payload = verificar_token(credenciais.credentials)

    meu_recurso(id, payload)

    resultado = controller.excluir_por_id(id)

    return resultado