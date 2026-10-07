import os
from dotenv import load_dotenv
from google import genai
from google.genai._gaos.lib.compat_errors import RateLimitError
from configparser import ConfigParser
from pathlib import Path
from services.tarefa_service import TarefaService
from repositories.passo_repository import Passo
from common.validações_genericas import Validações
from integrations.ia.formatador_prompt import gerar_prompt_gemini, desmenbriar_resposta_gemini, TipoDeTarefa, EstiloInstrucao, Prioridade

load_dotenv()
tarefaservice = TarefaService()
validacoes = Validações()

class IAClient:

    def __init__(self, client=None): 
        self.client = client or genai.Client(api_key=os.getenv("IA_API_KEY"))

    def enviar_prompt(self, prompt):
        try:
            interaction = self.client.interactions.create(
                model=os.getenv("IA_MODEL"),
                input=prompt
            )
            return interaction.output_text
        except RateLimitError as erro:
            raise ValueError("Não foi possivel criar passos, a demanda está muito alta")
        

    def criar_passo(self, tarefa_id):

        tarefa_id = validacoes._validar_id(tarefa_id)

        caminho = Path(__file__).parent.parent.parent
        caminho = caminho / "config" / "config.ini"
        config = ConfigParser()
        config.read(caminho)
        usuario_estilo = config['Usuario']['estilo_instrucao']

        tarefa = tarefaservice.buscar_por_id(tarefa_id)


        if tarefa['prioridade'] == 'baixa':
            prioridade = Prioridade.BAIXA

        elif tarefa['prioridade'] == 'alta':
            prioridade = Prioridade.ALTA

        else:
            prioridade = Prioridade.MEDIA


        if usuario_estilo == 'detalhado':
            usuario_estilo = EstiloInstrucao.DETALHADO

        else:
            usuario_estilo = EstiloInstrucao.DIRETO


        prompt = gerar_prompt_gemini(
            titulo=tarefa['titulo'],
            descricao=tarefa['descricao'],
            tipo=TipoDeTarefa.TAREFAS_DIARIAS if tarefa['tipo'] == 'tarefas_diarias' else TipoDeTarefa.TAREFAS_EDUCACIONAIS,
            prazo=tarefa['prazo'],
            criado_em=tarefa['criado_em'],
            prioridade=prioridade,
            estilo_instrucao=usuario_estilo,
            )

        resultado = self.enviar_prompt(prompt)

        resultado = desmenbriar_resposta_gemini(resultado.output_text)

        return resultado
    
    