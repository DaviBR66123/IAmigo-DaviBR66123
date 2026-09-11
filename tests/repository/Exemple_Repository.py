from repositories.usuario_repository import UsuarioRepository 
repo = UsuarioRepository() 
nome_teste = "EXEMPLO_REPOSITORY" 
repo.excluir_por_nome(nome_teste) 
usuario = repo.criar(nome_teste, "direto") 
print("CRIADO:", usuario) 
encontrado = repo.buscar_por_nome(nome_teste) 
print("ENCONTRADO:", encontrado) 
print("LISTA:") 
for item in repo.listar(): 
 print("-", item.nome) 
print("TESTE DE REPOSITORY CONCLUIDO")
