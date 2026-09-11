from services.usuario_service import UsuarioService


class UsuarioController:
    def __init__(self, service=None):
        self.service = service or UsuarioService()

    def criar_perfil(self, nome, estilo_instrucao):
        try:
            usuario = self.service.criar_usuario(nome, estilo_instrucao)
            return {
                "sucesso": True,
                "tipo": "SUCESSO",
                "mensagem": f"Perfil {usuario.nome} criado."
            }
        except ValueError as erro:
            return {
                "sucesso": False,
                "tipo": "REGRA_NEGOCIO",
                "mensagem": str(erro)
            }
        except Exception:
            return {
                "sucesso": False,
                "tipo": "FALHA_TECNICA",
                "mensagem": "Não foi possível concluir a operação."
            }

    def buscar_por_id(self, id):
        try:
            usuario = self.service.buscar_por_id(id)
            return {
                "sucesso": True,
                "tipo": "SUCESSO",
                "mensagem": f"Perfil de id {id} encontrado.",
                "dados": {
                    "id": usuario.id,
                    "nome": usuario.nome,
                    "estilo_instrucao": usuario.estilo_instrucao,
                    "criado_em": usuario.criado_em
                }
            }
        except ValueError as erro:
            return {
                "sucesso": False,
                "tipo": "REGRA_NEGOCIO",
                "mensagem": str(erro)
            }
        except Exception:
            return {
                "sucesso": False,
                "tipo": "FALHA_TECNICA",
                "mensagem": "Não foi possível concluir a operação."
            }