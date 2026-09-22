from repositories.usuario_repository import UsuarioRepository

class UsuarioService:
 
    def __init__(self, repository=None): 
        self.repository = repository or UsuarioRepository()

    def listar_usuarios(self): 
        usuarios = self.repository.listar()

        if usuarios == None:
            raise ValueError("Não foi possivel listar usuários.")

        usuarios_dict = {u.id: {'id': u.id, 'nome': u.nome, 'estilo': u.estilo_instrucao} for u in usuarios}

        return usuarios_dict

    def buscar_por_id(self, id):
        if id == None:
            raise ValueError("O id não pode ser vazio.")

        id = str(id)

        for i in list(id):
            if i not in {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9"}:
                raise ValueError("O id só pode conter números.")

        usuario = self.repository.buscar_por_id(id)

        if usuario == None:
            raise ValueError("Usuário não encontrado.")
        
        resultado = {
                "id": usuario.id,
                "nome": usuario.nome,
                "estilo_instrucao": usuario.estilo_instrucao,
                "criado_em": usuario.criado_em
            }

        return resultado
    
    def criar_usuario(self, nome, estilo_instrucao): 
        nome = nome.strip()

        if not nome: 
            raise ValueError("O nome não pode ficar vazio.")

        if estilo_instrucao not in {"direto", "detalhado"}:
            raise ValueError( 
            "O estilo deve ser 'direto' ou 'detalhado'." 
            )
        
        existente = self.repository.buscar_por_nome(nome)

        if existente is not None:                
            raise ValueError("Já existe um perfil com esse nome.")

        if len(nome) < 3: 
            raise ValueError( 
            "O nome precisa ter pelo menos 3 caracteres." 
            )

        if len(nome) > 100:
            raise ValueError(
                "O nome é pode ter no máximo 100 caracteres. Você ultrapassou o limite."
            )

        
        return self.repository.criar( 
            nome, 
            estilo_instrucao 
            )

    def excluir_por_id(self, id):
        if id == None:
            raise ValueError("O id não pode ser vazio.")

        id = str(id)

        for i in list(id):
            if i not in {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9"}:
                raise ValueError("O id só pode conter números.")

        excluido = self.repository.excluir_por_id(id)

        if not excluido:
            raise ValueError("Usuario não encontrado.")

        return True