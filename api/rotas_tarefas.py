from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

from controllers.tarefa_controller import TarefaController
from common.auth import verificar_token, verificar_admin, meu_recurso

router = APIRouter(
    prefix="/tarefas",
    tags=["tarefas"]
)

controller = TarefaController()
security = HTTPBearer()

class NovaTarefa(BaseModel):
    tipo: str # 'tarefas_diarias' ou 'tarefas_educacionais'
    titulo: str 
    descricao: str | None = None
    prioridade: str = "media" # 'baixa', 'media' ou 'alta'
    prazo: str | None = None
    criado_em: str

class AtualizarTarefa(BaseModel):
    tipo: str
    titulo: str
    descricao: str | None = None
    prioridade: str = "media"
    prazo: str | None = None

@router.get("/usuario/{id}")
def listar_por_usuario(id, credenciais: HTTPAuthCredentials = Depends(security)):
    payload = verificar_token(credenciais.credentials)

    meu_recurso(id, payload)

    resultado = controller.listar_por_usuario(id)

    return resultado

@router.get("/{id}")
def buscar_por_id(id, credenciais: HTTPAuthCredentials = Depends(security)):
    payload = verificar_token(credenciais.credentials)

    meu_recurso(id,payload)

    resultado = controller.buscar_por_id(id)

    return resultado

@router.patch("/{id}/concluido")
def alternar_concluido(id, modo="None", credenciais: HTTPAuthCredentials = Depends(security)):
    payload = verificar_token(credenciais.credentials)

    meu_recurso(id, payload)

    resultado = controller.alternar_concluido(id, modo)

    return resultado

@router.post("", status_code=status.HTTP_201_CREATED)
def criar_tarefa(id, dados: NovaTarefa, credenciais: HTTPAuthCredentials = Depends(security)):
    payload = verificar_token(credenciais.credentials)

    meu_recurso(id, payload)

    resposta = controller.criar_tarefa(
        id,
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

@router.put("/{id}")
def atualizar_tarefa(id, dados: AtualizarTarefa, credenciais: HTTPAuthCredentials = Depends(security)):
    payload = verificar_token(credenciais.credentials)

    meu_recurso(id, payload)

    resposta = controller.atualizar_tarefa(
        id,
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
def excluir_por_id(id, credenciais: HTTPAuthCredentials = Depends(security)):
    payload = verificar_token(credenciais.credentials)

    meu_recurso(id, payload)

    resultado = controller.excluir_por_id(id)

    return resultado