import re
from typing import TypedDict
from enum import Enum


class TipoDeTarefa(str, Enum):
    TAREFAS_DIARIAS = "tarefas_diarias"
    TAREFAS_EDUCACIONAIS = "tarefas_educacionais"


class EstiloInstrucao(str, Enum):
    DIRETO = "direto"
    DETALHADO = "detalhado"


class Prioridade(str, Enum):
    BAIXA = "baixa"
    MEDIA = "media"
    ALTA = "alta"


class RespostaPasso(TypedDict):
    numero: int
    titulo: str
    descricao: str
    tempo_estimado: str


class RespostaGemini(TypedDict):
    resumo: str
    passos: list[RespostaPasso]
    dicas: list[str]
    tempo_total: str


def gerar_prompt_gemini(
    titulo: str,
    descricao: str,
    tipo: TipoDeTarefa,
    prazo: str,
    criado_em: str,
    prioridade: Prioridade,
    estilo_instrucao: EstiloInstrucao,
) -> str:
    """
    Gera um prompt dinâmico para o Gemini baseado nos dados da tarefa do usuário com TDAH.
    """
    
    estilo_detalhes = (
        "Ser muito detalhado, explicar cada passo com contexto e por que fazer aquilo. "
        "Usar exemplos práticos e quebrar em sub-passos menores."
        if estilo_instrucao == EstiloInstrucao.DETALHADO
        else "Ser direto e conciso, sem muita enrolação. Ir direto ao ponto em cada passo."
    )
    
    contexto_tipo = (
        "Esta é uma tarefa do dia a dia, portanto considere rotina, hábitos e praticidade."
        if tipo == TipoDeTarefa.TAREFAS_DIARIAS
        else "Esta é uma tarefa educacional, portanto foque em aprendizado, compreensão e retenção."
    )
    
    urgencia = ""
    if prioridade == Prioridade.ALTA:
        urgencia = "Esta é uma tarefa de ALTA prioridade e com prazo próximo (prazo: {prazo}). Considere urgência."
    elif prioridade == Prioridade.MEDIA:
        urgencia = "Esta é uma tarefa de MÉDIA prioridade com prazo em {prazo}."
    else:
        urgencia = "Esta é uma tarefa de BAIXA prioridade, então pode ser mais flexível."
    
    prompt = f"""Você é um assistente especializado em ajudar pessoas com TDAH a organizar e executar tarefas.

📋 INFORMAÇÕES DA TAREFA:
- Título: {titulo}
- Descrição: {descricao}
- Tipo: {tipo.value}
- Prazo: {prazo}
- Criado em: {criado_em}
- Prioridade: {prioridade.value.upper()}

🎯 CONTEXTO:
{contexto_tipo}
{urgencia}

📝 INSTRUÇÕES ESPECIAIS:
{estilo_detalhes}

⚠️ CONSIDERAÇÕES PARA TDAH:
- Use linguagem simples e clara
- Divida em passos pequenos e manejáveis
- Inclua pausas e intervalos se necessário
- Seja motivador e prático
- Evite informações desnecessárias

🔧 FORMATO DE RESPOSTA:
Estruture sua resposta EXATAMENTE assim:

---RESUMO---
[Um parágrafo resumindo a tarefa e abordagem]

---PASSOS---
1. [Título do Passo]
   Descrição: [Descrição detalhada do passo]
   Tempo: [Tempo estimado, ex: 5 minutos]

2. [Título do Passo]
   Descrição: [Descrição detalhada do passo]
   Tempo: [Tempo estimado]

[Continue com mais passos...]

---DICAS---
- [Dica 1]
- [Dica 2]
- [Dica 3]
[Continue com mais dicas...]

---TEMPO_TOTAL---
[Tempo total estimado para completar a tarefa]

Agora, crie um plano passo a passo para essa tarefa!"""
    
    return prompt


def desmenbriar_resposta_gemini(resposta_texto: str) -> RespostaGemini:
    """
    Desmenbia a resposta do Gemini em estrutura formatada.
    Processa o texto seguindo os marcadores ---SEÇÃO---.
    """
    
    # Dividir por seções
    secoes = {}
    partes = re.split(r'---([A-Z_]+)---', resposta_texto)
    
    # Reconstruir as seções em um dicionário
    for i in range(1, len(partes), 2):
        chave = partes[i].lower()
        valor = partes[i + 1].strip() if i + 1 < len(partes) else ""
        secoes[chave] = valor
    
    # Extrair resumo
    resumo = secoes.get('resumo', '').strip()
    
    # Extrair e processar passos
    passos = _extrair_passos(secoes.get('passos', ''))
    
    # Extrair dicas
    dicas = _extrair_dicas(secoes.get('dicas', ''))
    
    # Extrair tempo total
    tempo_total = secoes.get('tempo_total', '').strip()
    
    return {
        'resumo': resumo,
        'passos': passos,
        'dicas': dicas,
        'tempo_total': tempo_total,
    }


def _extrair_passos(texto_passos: str) -> list[RespostaPasso]:
    """
    Extrai os passos do texto formatado.
    Formato esperado:
    1. [Título]
       Descrição: [texto]
       Tempo: [tempo]
    """
    passos = []
    
    # Dividir por número de passo (1., 2., etc)
    blocos = re.split(r'\n(\d+)\.\s+', texto_passos)
    
    # blocos[0] será vazio, então começamos do índice 1
    for i in range(1, len(blocos), 2):
        numero = int(blocos[i])
        conteudo = blocos[i + 1] if i + 1 < len(blocos) else ""
        
        # Extrair título (primeira linha)
        linhas = conteudo.split('\n')
        titulo = linhas[0].strip()
        
        # Extrair descrição e tempo
        descricao = ""
        tempo_estimado = ""
        
        for linha in linhas[1:]:
            linha_limpa = linha.strip()
            if linha_limpa.startswith('Descrição:'):
                descricao = linha_limpa.replace('Descrição:', '').strip()
            elif linha_limpa.startswith('Tempo:'):
                tempo_estimado = linha_limpa.replace('Tempo:', '').strip()
        
        passos.append({
            'numero': numero,
            'titulo': titulo,
            'descricao': descricao,
            'tempo_estimado': tempo_estimado,
        })
    
    return passos


def _extrair_dicas(texto_dicas: str) -> list[str]:
    """
    Extrai as dicas do texto formatado.
    Esperado:
    - Dica 1
    - Dica 2
    """
    dicas = []
    
    for linha in texto_dicas.split('\n'):
        linha_limpa = linha.strip()
        if linha_limpa.startswith('-'):
            dica = linha_limpa.lstrip('- ').strip()
            if dica:
                dicas.append(dica)
    
    return dicas


# Exemplo de uso
if __name__ == "__main__":
    # Exemplo 1: Tarefa diária com estilo detalhado
    prompt = gerar_prompt_gemini(
        titulo="Organizar a mesa do escritório",
        descricao="Limpar a bagunça, organizar documentos e preparar para trabalhar amanhã",
        tipo=TipoDeTarefa.TAREFAS_DIARIAS,
        prazo="Hoje à noite",
        criado_em="28/09/2026",
        prioridade=Prioridade.MEDIA,
        estilo_instrucao=EstiloInstrucao.DETALHADO,
    )
    
    print("=" * 80)
    print("PROMPT GERADO PARA GEMINI:")
    print("=" * 80)
    print(prompt)
    print("\n" + "=" * 80 + "\n")
    
    # Exemplo de resposta (simulada)
    resposta_exemplo = """---RESUMO---
Você precisa organizar sua mesa de trabalho para criar um ambiente produtivo. Isso envolve remover itens desnecessários, agrupar documentos similares e preparar tudo para o próximo dia.

---PASSOS---
1. Remover o óbvio
   Descrição: Comece pegando todos os itens que não pertencem à mesa (copos, pratos, etc) e coloque em um local apropriado. Não se preocupe em organizar agora, apenas remova.
   Tempo: 5 minutos

2. Criar pilhas por categoria
   Descrição: Agrupe todos os documentos em categorias (contas, trabalho, pessoal). Isso facilita encontrar depois.
   Tempo: 10 minutos

3. Limpar a superfície
   Descrição: Use um pano úmido para limpar a mesa e deixá-la sem poeira.
   Tempo: 5 minutos

4. Organizar em ordem
   Descrição: Coloque os itens essenciais em locais acessíveis. Use gavetas ou organizadores.
   Tempo: 10 minutos

---DICAS---
- Se ficar cansado, faça uma pausa de 2 minutos
- Use a técnica Pomodoro (25 min trabalho, 5 min pausa)
- Coloque uma música motivadora para tornar mais agradável

---TEMPO_TOTAL---
Aproximadamente 30 minutos"""
    
    print("RESPOSTA SIMULADA DO GEMINI:")
    print("=" * 80)
    print(resposta_exemplo)
    print("\n" + "=" * 80 + "\n")
    
    # Desmenbriar resposta
    resultado = desmenbriar_resposta_gemini(resposta_exemplo)
    
    print("RESPOSTA PROCESSADA EM ESTRUTURA:")
    print("=" * 80)
    print(f"\n📝 RESUMO:\n{resultado['resumo']}\n")
    
    print("📋 PASSOS:")
    for passo in resultado['passos']:
        print(f"\n  Passo {passo['numero']}: {passo['titulo']}")
        print(f"  └─ Descrição: {passo['descricao']}")
        print(f"  └─ Tempo: {passo['tempo_estimado']}")
    
    print(f"\n💡 DICAS:")
    for i, dica in enumerate(resultado['dicas'], 1):
        print(f"  {i}. {dica}")
    
    print(f"\n⏱️  TEMPO TOTAL: {resultado['tempo_total']}")