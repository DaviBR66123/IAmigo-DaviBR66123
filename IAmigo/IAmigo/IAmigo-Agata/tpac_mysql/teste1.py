from pathlib import Path
import configparser
import xmltodict

def load_language():
    #Pegando as configurações
    config_path = Path(__file__).parent.parent / "data" / "config.ini"
    config = configparser.ConfigParser()
    config.read(str(config_path), "utf-8")
    print(config["localization"]["language"])

    #Pegando o arquivo xml
    xml_path = Path(__file__).parent / "language_xml" / config["localization"]["language"]
    print(str(xml_path))

    #Lendo o xml
    with open(xml_path, 'r', encoding='utf-8') as xml_file:
        xml_content = xml_file.read()

    #Exportando variavel com o xml
    strings = xmltodict.parse(xml_content)
    strings = strings["IAmigo"]
    return strings

def menu_frame(opcoes, titulo="MENU"):
    linhas = [f"{i+1}. {opt}" for i, opt in enumerate(opcoes)]
    
    # Calcular largura máxima (incluindo o título e as linhas formatadas)
    todas_linhas = [titulo] + linhas
    largura_max = max(len(linha) for linha in todas_linhas) + 4
    
    # Construir e imprimir caixa
    print("╔" + "═" * (largura_max - 2) + "╗")
    print(f"║ {titulo.center(largura_max - 4)} ║")
    print("╠" + "═" * (largura_max - 2) + "╣")
    
    for linha in linhas:
        print(f"║ {linha.ljust(largura_max - 4)} ║")
    
    print("╚" + "═" * (largura_max - 2) + "╝")

menu_frame(["Batata", "Banana", "Abacaxi"], "FRUTAS")
print()
menu_frame(["Opção Curta", "Esta é uma opção muito mais longa"], "MENU")
print()
menu_frame(["A", "B", "C"], "MENU PRINCIPAL COM TÍTULO LONGO")