from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from controllers.usuario_controller import UsuarioController

router = APIRouter(
    prefix="/usuarios",
    tags=["usuarios"]
)

controller = UsuarioController()


class NovoUsuario(BaseModel):
    nome: str
    estilo_instrucao: str = "direto"


@router.get("")
def listar_usuarios():
    return {
        "dados": controller.listar_usuarios()
    }

@router.get("/{id}")
def buscar_por_id(id):
    resultado = controller.buscar_por_id(id)

    return resultado

@router.post("", status_code=status.HTTP_201_CREATED)
def criar_usuario(dados: NovoUsuario):
    resposta = controller.criar_perfil(
        dados.nome,
        dados.estilo_instrucao
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