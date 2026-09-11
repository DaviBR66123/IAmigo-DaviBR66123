import unittest

from services.usuario_service import UsuarioService



class UsuarioFake: 
    def __init__(self, nome, estilo_instrucao="direto"): 
        self.id = 1 
        self.nome = nome 
        self.estilo_instrucao = estilo_instrucao



class UsuarioRepositoryFake: 
    def __init__(self): 
        self.usuarios = {}

    def listar(self): 
        return list(self.usuarios.values())
     
    def buscar_por_nome(self, nome): 
        return self.usuarios.get(nome)
     
    def criar(self, nome, estilo_instrucao): 
        usuario = UsuarioFake( 
        nome, 
        estilo_instrucao 
        ) 
        self.usuarios[nome] = usuario 
        return usuario


     
class TestUsuarioService(unittest.TestCase): 
    def setUp(self): 
        self.repo = UsuarioRepositoryFake() 
        self.service = UsuarioService(self.repo) 

    def test_cria_usuario_valido(self): 
        usuario = self.service.criar_usuario( 
        "Anada", 
        "direto"
        )
        self.assertEqual(usuario.nome, "Anada")

    def test_nao_aceita_nome_vazio(self): 
        with self.assertRaises(ValueError): 
            self.service.criar_usuario( 
            " ", 
            "direto" 
            )

    def test_nao_aceita_usuario_duplicado(self): 
        self.service.criar_usuario( 
        "Leonardo", 
        "direto" 
        ) 

        with self.assertRaises(ValueError): 
            self.service.criar_usuario( 
            "Leonardo", 
            "direto" 
            )

    def test_nao_aceita_estilo_invalido(self): 
        with self.assertRaises(ValueError): 
            self.service.criar_usuario( 
            "Bia", 
            "gigante" 
            )

    def test_nao_aceita_nome_muito_curto(self): 
        with self.assertRaises(ValueError): 
            self.service.criar_usuario( 
            "Al", 
            "direto" 
            )

    def test_rejeita_nome_com_menos_de_3_caracteres(self):
        with self.assertRaisesRegex(ValueError, "pelo menos 3 caracteres"):
            self.service.criar_usuario("Al", "direto")



if __name__ == "__main__": 
    unittest.main()
