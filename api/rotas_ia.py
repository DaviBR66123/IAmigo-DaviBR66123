from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

from controllers.ia_controller import IAController
from common.auth import verificar_token


router = APIRouter(
    prefix="/ia",
    tags=["ia"]
)

controller = IAController()
security = HTTPBearer()

@router.get("/call")
def enviar_prompt(entrada, credenciais: HTTPAuthCredentials = Depends(security)):
    payload = verificar_token(credenciais.credentials)

    resultado = controller.enviar_prompt(entrada)

    return resultado