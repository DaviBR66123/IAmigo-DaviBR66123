import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

class IAClient:

    def __init__(self, client=None): 
        self.client = client or genai.Client(api_key=os.getenv("IA_API_KEY"))

    def enviar_prompt(self, prompt):
        interaction = self.client.interactions.create(
            model=os.getenv("IA_MODEL"),
            input=prompt
        )
        return interaction

    def criar_passos(self, dados_tarefa, dados_usuario):
        