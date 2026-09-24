from services.passo_service import PassoService


class PassoController:

    def __init__(self, service=None):
        self.service = service or PassoService()

    def listar_por_tarefa(self, tarefa_id):
        try:
            resultado = self.service.listar_por_tarefa(tarefa_id)

            return {
                "sucesso": True,
                "tipo": "SUCESSO",
                "Mensagem": f"Passos da tarefa de id {tarefa_id} encontrada",
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

    def criar_passo(self, tarefa_id, texto):
        try:
            resultado = self.service.criar_passo(tarefa_id, texto)

            return {
                "sucesso": True,
                "tipo": "SUCESSO",
                "Mensagem": f"Passos da tarefa de id {tarefa_id} criado",
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

    def alternar_concluido(self, id, modo="None"):
        try:
            resultado = self.service.alternar_concluido(id, modo)

            if modo.casefold() == "true":
                msg = " para concluido"

            elif modo.casefold() == "false":
                msg = " para não concluido"

            else:
                msg = ""

            return {
                "sucesso": True,
                "tipo": "SUCESSO",
                "Mensagem": f"Status do passo de {id} alternado{msg}."
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

    def excluir_por_id(self, id):
        try:
            self.service.excluir_por_id(id)

            return {
                "sucesso": True,
                "tipo": "SUCESSO",
                "Mensagem": f"Passo excluido com sucesso."
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
