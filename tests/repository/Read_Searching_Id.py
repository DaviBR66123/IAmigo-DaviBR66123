from repositories.usuario_repository import UsuarioRepository 
repo = UsuarioRepository()

entrada = int(input("Digite o ID de Usuário para procura-lo: "))

pesquisado = repo.buscar_por_id(entrada)

if pesquisado == None:
    print("Usuário não encontrado")

else:
    print(f"Nome: {pesquisado.nome}")
    print(f"ID: {pesquisado.id}")
    print(f"Estilo: {pesquisado.estilo_instrucao}")