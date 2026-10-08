from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from enum import Enum

from controllers.usuario_controller import UsuarioController
from common.auth import verificar_token, verificar_admin, meu_recurso, teste_usuario_authenticado

router = APIRouter(
    prefix="/usuarios",
    tags=["usuarios"]
)

controller = UsuarioController()
security = HTTPBearer()

class NovoUsuario(BaseModel):
    nome: str
    estilo_instrucao: str = "direto"
    gmail: str
    senha: str

class Roles(str, Enum):
    USER = "user"
    ADMIN = "admin"

class Credenciais(BaseModel):
    gmail: str
    senha: str

@router.get("")
def listar_usuarios(credenciais: HTTPAuthCredentials = Depends(security)):
    payload = verificar_token(credenciais)

    verificar_admin(payload)    
    
    return {
        "dados": controller.listar_usuarios()
    }

@router.get("/{id}")
def buscar_por_id(id, credenciais: HTTPAuthCredentials = Depends(security)):
    payload = verificar_token(credenciais.credentials)

    meu_recurso(id, payload)

    resultado = controller.buscar_por_id(id)

    return resultado


@router.post("", status_code=status.HTTP_201_CREATED)
def criar_usuario(dados: NovoUsuario, credenciais: HTTPAuthCredentials = Depends(security)):
    payload = verificar_token(credenciais.credentials)

    resposta = controller.criar_perfil(
        dados.nome,
        dados.estilo_instrucao,
        dados.gmail,
        dados.senha
    )

    if not resposta["sucesso"]:
        raise HTTPException(
            status_code=422,
            detail=resposta["mensagem"]
        )

    return resposta

@router.put("/{id}")
def atualizar_usuario(id, dados: NovoUsuario, credenciais: HTTPAuthCredentials = Depends(security)):
    payload = verificar_token(credenciais.credentials)

    meu_recurso(id, payload)

    resposta = controller.atualizar_perfil(
        id,
        dados.nome,
        dados.estilo_instrucao,
        dados.gmail,
        dados.senha
    )

    if not resposta["sucesso"]:
        raise HTTPException(
            status_code=422,
            detail=resposta["mensagem"]
        )

    return resposta

@router.delete("")
def excluir_por_id(id, credenciais: HTTPAuthCredentials = Depends(security)):
    payload = verificar_token(credenciais.credentials)

    meu_recurso(id, payload)

    resultado = controller.excluir_por_id(id)

    return resultado

@router.post("/login", status_code=status.HTTP_200_OK)
def login(credenciais: Credenciais):
    resposta = controller.fazer_login(
        credenciais.gmail,
        credenciais.senha
    )
    
    if not resposta["sucesso"]:
        raise HTTPException(
            status_code=401,
            detail=resposta["mensagem"]
        )
    
    return resposta

@router.patch("/permissoes")
def permissoes(id, dados: Roles, credenciais: HTTPAuthCredentials = Depends(security)):
    payload = verificar_token(credenciais.credentials)

    verificar_admin(payload)

    resultado = permissoes(id, dados)

    return resultado