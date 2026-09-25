import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

class IAProvedor:

    def __init__(self, client=None): 
        self.client = client or genai.Client(api_key=os.getenv("IA_API_KEY"))

    def enviar_prompt(self, prompt):
        interaction = self.client.interactions.create(
            model=os.getenv("IA_MODEL"),
            input=prompt
        )
        return interaction

    def criar_passos(self, dados_tarefa, dados_usuario):
        titulo = dados_tarefa["titulo"]
        descricao = dados_tarefa.get("descricao", "Nenhuma descrição fornecida")
        tipo = dados_tarefa.get("tipo", "tarefas_diarias")
        prazo = dados_tarefa.get("prazo", "Não informado")
        criado_em = dados_tarefa.get("criado_em", "Não informado")
        prioridade = dados_tarefa.get("prioridade", "media")
        estilo_instrucao = dados_usuario.get("estilo_instrucao", "direto")

        if tipo == "tarefas_educacionais":
            contexto_tipo = """
    Esta é uma tarefa educacional. Explique os conceitos necessários de forma
    simples e inclua exemplos práticos quando isso ajudar no entendimento.
    """
        else:
            contexto_tipo = """
    Esta é uma tarefa diária. Priorize ações práticas, objetivas e fáceis de executar.
    """

        if estilo_instrucao == "detalhado":
            estilo = """
    Use explicações detalhadas, mas organize o conteúdo em partes curtas.
    Explique o motivo de cada etapa e inclua exemplos quando forem úteis.
    """
        else:
            estilo = """
    Seja direto e objetivo. Use frases curtas e evite explicações desnecessárias.
    """

        prompt = f"""
    Você é um assistente especializado em ajudar pessoas com TDAH a organizar
    e concluir tarefas.

    Sua função é transformar a tarefa abaixo em um plano de execução simples,
    realista e fácil de acompanhar.

    DADOS DA TAREFA:
    - Título: {titulo}
    - Descrição: {descricao}
    - Tipo: {tipo}
    - Prazo: {prazo}
    - Data de criação: {criado_em}
    - Prioridade: {prioridade}

    PREFERÊNCIAS DO USUÁRIO:
    - Estilo de instrução: {estilo_instrucao}

    {contexto_tipo}
    {estilo}

    Crie uma resposta seguindo exatamente esta estrutura:

    1. Objetivo da tarefa
    Explique em uma frase o que precisa ser alcançado.

    2. Preparação
    Liste o que a pessoa precisa separar, abrir ou organizar antes de começar.
    Se não for necessário, escreva "Nenhuma preparação específica".

    3. Passo a passo
    Crie uma lista numerada de etapas pequenas e concretas.
    Cada etapa deve conter apenas uma ação principal.
    Evite juntar várias ações complexas na mesma etapa.

    4. Primeiro passo
    Diga qual é a menor ação que a pessoa pode fazer imediatamente para começar.

    5. Divisão em blocos
    Divida a tarefa em blocos de trabalho curtos. Sempre que fizer sentido,
    sugira blocos de 15 a 25 minutos com pequenas pausas entre eles.

    6. Verificação final
    Crie uma lista curta para confirmar se a tarefa foi concluída.

    7. Dificuldades comuns
    Liste até três possíveis dificuldades e uma solução prática para cada uma.

    REGRAS IMPORTANTES:
    - Considere a prioridade "{prioridade}" ao sugerir a ordem de execução.
    - Considere o prazo "{prazo}" ao montar o plano.
    - Não invente informações que não estejam nos dados.
    - Se faltarem informações importantes, informe quais são e faça uma sugestão
    provisória sem impedir que a pessoa comece.
    - Não use linguagem de culpa, cobrança ou julgamento.
    - Evite parágrafos longos.
    - Destaque ações usando verbos no imperativo, como "Abra", "Separe", "Escreva"
    e "Revise".
    - O resultado deve ser prático e executável.
    """

        return prompt