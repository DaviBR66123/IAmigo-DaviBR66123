def menu_frame(opcoes, titulo="MENU"):
    linhas = [f"{i+1}. {opt}" for i, opt in enumerate(opcoes)]
    
    # Calcular largura máxima considerando título e todas as opções
    todas_linhas = [titulo] + linhas
    largura_conteudo = max(len(linha) for linha in todas_linhas)
    
    # Adicionar espaço de padding (2 espaços de cada lado = 4 total)
    largura_max = largura_conteudo + 4
    
    # Construir e imprimir caixa
    print("╔" + "═" * (largura_max - 2) + "╗")
    print(f"║ {titulo.center(largura_max - 4)} ║")
    print("╠" + "═" * (largura_max - 2) + "╣")
    
    for linha in linhas:
        print(f"║ {linha.ljust(largura_max - 4)} ║")
    
    print("╚" + "═" * (largura_max - 2) + "╝")

# Testes
menu_frame(["Batata", "Banana", "Abacaxi"], "FRUTAS")
print()
menu_frame(["Opção Curta", "Esta é uma opção muito mais longa"], "MENU")
print()
menu_frame(["A", "B", "C"], "MENU PRINCIPAL COM TÍTULO LONGO")