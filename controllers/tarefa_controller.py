from services.tarefa_service import TarefaService


class TarefaController:
    def __init__(self, service=None):
        self.service = service or TarefaService()

    def listar_por_usuario(self, id):
        try:
            resultado = self.service.listar_por_usuario(id)

            return {
                "sucesso": True,
                "tipo": "SUCESSO",
                "Mensagem": f"Tarefa de id {id} encontrada",
                "dados": resultado
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
    def criar_tarefa(self, usuario_id, tipo, titulo, descricao, prioridade, prazo=None):
        try:
            resultado = self.service.criar_tarefa(
                usuario_id=usuario_id,
                tipo=tipo,
                titulo=titulo,
                descricao=descricao,
                prioridade=prioridade,
                prazo=prazo
            )
            return {
                "sucesso": True,
                "tipo": "SUCESSO",
                "mensagem": f"Tarefa '{resultado.titulo}' criada."
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