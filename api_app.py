from fastapi import FastAPI

from api.rotas_usuarios import router as usuarios_router

app = FastAPI(
    title="TPaC API",
    description="Primeira API do TPaC",
    version="1.0.0"
)


@app.get("/")
def inicio():
    return {
        "sistema": "TPaC",
        "api": "funcionando"
    }

app.include_router(usuarios_router)


@app.get("/")
def inicio():
    return {
        "sistema": "TPaC",
        "api": "funcionando"
    }