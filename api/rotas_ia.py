from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from controllers.ia_controller import IAController

router = APIRouter(
    prefix="/ia",
    tags=["ia"]
)

controller = IAController()

@router.get("/call")
def enviar_prompt(entrada):
    resultado = controller.enviar_prompt(entrada)

    return resultado