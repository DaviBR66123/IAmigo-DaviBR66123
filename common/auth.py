import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException
from os import getenv

from common.validações_genericas import Validações

validacoes = Validações()
_validar_id = validacoes._validar_id

SECRET_KEY = getenv("SECRET_KEY", "dev-secret-key-change-in-production")
ALGORITHM = getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))


def criar_token_acesso(dados: dict):
    """
    Cria um JWT com os dados fornecidos.
    
    Args:
        dados: dict com informações do usuário (ex: {"id": 5, "gmail": "user@gmail.com"})
    
    Returns:
        str: token JWT codificado
    """
    # Cópia dos dados para não modificar o original
    dados_token = dados.copy()
    
    # Define expiração
    expiracao = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    dados_token.update({"exp": expiracao})
    
    # Codifica e retorna o token
    token = jwt.encode(dados_token, SECRET_KEY, algorithm=ALGORITHM)
    
    return token

def verificar_token(token: str):
    """
    Valida o JWT e retorna os dados decodificados.
    Lança HTTPException 401 se inválido ou expirado.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token expirado."
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Token inválido."
        )

def verificar_admin(payload: dict):
    role = payload.get("role")

    if role != "admin":
        raise ValueError("Negado. Você não é autorizado")

    return True

def meu_recurso(id, payload: dict):
    usuario_id = payload.get("id")
    role = payload.get("role")

    if usuario_id != id and role != "admin":
        raise ValueError("Esse recurso não te pertence")

    return True

def teste_usuario_authenticado(payload):
    payload = jwt.decode(payload, SECRET_KEY, algorithms=[ALGORITHM])

    return payload