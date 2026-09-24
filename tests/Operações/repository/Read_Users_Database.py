from repositories.usuario_repository import UsuarioRepository 
repo = UsuarioRepository()

print("LISTA:") 
for item in repo.listar(): 
    print("-", item.nome) 