from integrations.ia.ia_client import IAClient


class IAController:
    def __init__(self, client=None):
        self.client = client or IAClient()

    def enviar_prompt(self, prompt):
        try:
            resultado = self.client.enviar_prompt(prompt)

            return {
                "sucesso": True,
                "tipo": "SUCESSO",
                "Mensagem": f"Resposta obtida com sucesso",
                "dados": prompt
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