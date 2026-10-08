from common.validações_genericas import Validações
from repositories.usuario_repository import UsuarioRepository
from common.auth import criar_token_acesso

validacoes = Validações()

_validar_id = validacoes._validar_id

class UsuarioService:
 
    def __init__(self, repository=None): 
        self.repository = repository or UsuarioRepository()

    def listar_usuarios(self): 
        usuarios = self.repository.listar()

        if usuarios == None:
            raise ValueError("Não foi possivel listar usuários.")

        usuarios_dict = {u.id: {'id': u.id, 'nome': u.nome, 'estilo': u.estilo_instrucao, 'role': u.role, 'gmail': u.gmail, 'senha': u.senha, 'criado_em': u.criado_em} for u in usuarios}

        return usuarios_dict

    def buscar_por_id(self, id):

        id = _validar_id(id)

        usuario = self.repository.buscar_por_id(id)

        if usuario == None:
            raise ValueError("Usuário não encontrado.")
        
        resultado = {
                "id": usuario.id,
                "nome": usuario.nome,
                "estilo_instrucao": usuario.estilo_instrucao,
                "role": usuario.role,
                "gmail": usuario.gmail,
                "senha": usuario.senha,
                "criado_em": usuario.criado_em
            }

        return resultado
    
    def criar_usuario(self, nome, estilo_instrucao, gmail, senha): 
        nome = nome.strip()

        if not nome: 
            raise ValueError("O nome não pode ficar vazio.")

        if estilo_instrucao not in {"direto", "detalhado"}:
            raise ValueError( 
            "O estilo deve ser 'direto' ou 'detalhado'." 
            )

        if not gmail:
            raise ValueError("Gmail não pode ficar vazio")

        if not senha: 
            raise ValueError("Senha não pode ficar vazia")
        
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
            estilo_instrucao,
            gmail,
            senha
            )

    def atualizar_usuario(self, id, nome=None, estilo_instrucao=None, gmail=None, senha=None):
        
        # Validar ID
        id = _validar_id(id)

        # Validar Nome
        nome = nome.strip()

        if not nome: 
            raise ValueError("O nome não pode ficar vazio.")

        if len(nome) < 3: 
            raise ValueError("O nome precisa ter pelo menos 3 caracteres.")

        if len(nome) > 100:
            raise ValueError("O nome pode ter no máximo 100 caracteres. Você ultrapassou o limite.")

        # Validar Estilo
        if estilo_instrucao not in {"direto", "detalhado"}:
            raise ValueError("O estilo deve ser 'direto' ou 'detalhado'.")

        # Verificar se usuário existe
        usuario_atual = self.repository.buscar_por_id(id)
        if usuario_atual is None:
            raise ValueError("Usuário não encontrado.")

        # Verificar se há mudanças
        if nome == usuario_atual.nome and estilo_instrucao == usuario_atual.estilo_instrucao and gmail == usuario_atual.gmail and senha == usuario_atual.senha:
            raise ValueError("Não há mudanças")

        # Verificar se novo nome já existe (mas não é o nome atual)
        existente = self.repository.buscar_por_nome(nome)
        if existente is not None and existente.id != id:
            raise ValueError("Já existe um perfil com esse nome.")

        if nome == None:
            nome = usuario_atual.nome
        if estilo_instrucao == None:
            estilo_instrucao = usuario_atual.estilo_instrucao
        if gmail == None:
            gmail = usuario_atual.gmail
        if senha == None:
            senha = usuario_atual.senha

        return self.repository.atualizar(id, nome, estilo_instrucao, gmail, senha)

    def excluir_por_id(self, id):

        id = _validar_id(id)

        excluido = self.repository.excluir_por_id(id)

        if not excluido:
            raise ValueError("Usuario não encontrado.")

        return True

    def fazer_login(self, gmail, senha):
        """
        Valida credenciais e retorna o usuário se forem corretas.
        Lança ValueError se inválidas.
        """
        # Validar entrada
        gmail = gmail.strip()
        senha = senha.strip()
        
        if not gmail or not senha:
            raise ValueError("Email e senha são obrigatórios.")
        
        # Buscar usuário por email
        usuario = self.repository.buscar_por_gmail(gmail)
        
        if usuario is None:
            raise ValueError("Credenciais inválidas.")
        
        # ⚠️ IMPORTANTE: Comparação em TEXTO PLANO
        # Na Aula 09 vamos usar HASH (passlib)
        if usuario.senha != senha:
            raise ValueError("Credenciais inválidas.")

        dados_token = {
        "id": usuario.id,
        "role": usuario.role
        }
    
        # Gera o token
        token = criar_token_acesso(dados_token)
        
        # Sucesso: retornar dados do usuário (sem a senha)
        return {
            "access_token": token,
            "token_type": "bearer"
        }

    def permissoes(self, id, role):

        id = _validar_id(id)

        if role not in {"user", "admin"}:
            raise ValueError("Cargo invalido para promossão")

        resultado = self.repository.permissoes(id, role)

        return resultado.role